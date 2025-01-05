
from pathlib import Path

import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split

from .hparams.data_args import DataArguments
from .hparams.training_args import TraningArguments


class Trainer:

    def __init__(self,train_args:TraningArguments,data_args:DataArguments) -> None:
        
        self.train_args = train_args
        self.data_args = data_args


    def train(self):

        params = {
            "boosting_type": self.train_args.boosting_type,
            "objective": self.train_args.objective,
            "metric": self.train_args.metric,
            "num_leaves": self.train_args.num_leaves,
            "learning_rate": self.train_args.learning_rate,
            "feature_fraction": self.train_args.feature_fraction,
            "bagging_fraction": self.train_args.bagging_fraction,
            "bagging_freq": self.train_args.bagging_freq,
            "verbose": self.train_args.verbose,
        }

        gbm = lgb.train(
            params,
            lgb_train,
            num_boost_round=self.train_args.num_boost_round,
            valid_sets=lgb_train,  # eval training data
        )

    def __call__(self) -> None:
        #实例化时就把数字准备好
        self._prepare_data(self.data_args)
        
    def _prepare_data(self,data_args:DataArguments):

        binary_example_dir = Path(__file__).absolute().parents[1] / "binary_classification"
        df_train = pd.read_csv(str(binary_example_dir / "binary.train"), header=None, sep="\t")

        y_train = df_train[0]
        X_train = df_train.drop(0, axis=1)

        if not data_args.eval_dataset:
            #无验证集就需split
            X_train,X_test,y_train,y_test = train_test_split(X_train,
                                                             y_train,
                                                             test_size=data_args.test_size,
                                                             random_state=data_args.random_state)

        else:
            df_test = pd.read_csv(str(binary_example_dir / "binary.test"), header=None, sep="\t")

            y_test = df_test[0]
            X_test = df_test.drop(0, axis=1)

        num_train, num_feature = X_train.shape

        # generate feature names
        feature_name = [f"feature_{col}" for col in range(num_feature)]
        lgb_train = lgb.Dataset(
            X_train, y_train, feature_name=feature_name, categorical_feature=[21], free_raw_data=False
        )
        lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train, free_raw_data=False)


