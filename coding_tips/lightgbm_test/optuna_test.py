# coding: utf-8
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split

import optuna

print("Loading data...")
# load or create your dataset
example_dir = Path(__file__).absolute().parent
df = pd.read_csv(example_dir / "data/high_diamond/data.csv")


y = df['blueWins']
X = df.drop(['gameId',"blueWins"],axis=1)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=2025)


def objective(trial):


    # specify your configurations as a dict
    params = {
        "boosting_type": "gbdt",
        "objective": "binary",
        "metric": "auc",
        "verbose": -1,
        "n_estimators":trial.suggest_categorical("n_estimators",[10000]),
        "learning_rate":trial.suggest_float("learning_rate",0.01,0.3),
        "lambda_l1":trial.suggest_float("lambda_l1",1e-8,10.0,log=True),
        "lambda_l2":trial.suggest_float("lambda_l2",1e-8,10.0,log=True),
        "num_leaves":trial.suggest_int("num_leaves",2,256) ,
        "max_depth":trial.suggest_int("max_depth",3,12) ,
        "min_data_in_leaf":trial.suggest_int("min_data_in_leaf",200,1000,step=100) ,
        "min_gain_to_split":trial.suggest_float("min_gain_to_split",0,15),
        "feature_fraction": trial.suggest_float("feature_fraction",0.4,1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction",0.4,1.0),
        "bagging_freq": trial.suggest_int("bagging_freq",1,7),
        "min_child_samples":trial.suggest_int("min_child_samples",5,100)
    }

    pruning_callback = optuna.integration.LightGBMPruningCallback(trial,"auc")

    cv_scores =np,np.empty(5)

    lgb_eval = lgb.Dataset(X_test, y_test, free_raw_data=False)

    cv = StratifiedKFold(n_splits=5,shuffle=True,random_state=2025)

    for idx,(train_idx,test_idx) in enumerate(cv.split(X_train,y_train)):
        X_train_fold,X_test_fold = X_train.iloc[train_idx],X_train.iloc[test_idx]
        y_train_fold,y_test_fold = y_train[train_idx],y_train[test_idx]

        lgb_train_fold = lgb.Dataset(X_train_fold,label=y_train_fold)
        lgb_test_fold = lgb.Dataset(X_test_fold,label=y_test_fold)


        print("Starting training...")
        # feature_name and categorical_feature
        gbm = lgb.train(
            params,
            lgb_train_fold,
            valid_sets=[lgb_test_fold], 
            callbacks=[pruning_callback]
        )

        y_prds = gbm.predict(X_test_fold)
        cv_scores[idx] = roc_auc_score(y_test_fold,y_prds)

    return np.mean(cv_scores)

if __name__ == "__main__":
    study = optuna.create_study(
        pruner=optuna.pruners.MedianPruner(n_warmup_steps=10),direction="maximize"
    )

    study.optimize(objective,n_trials=100)
    print("Number of finished trials: {}".format(len(study.trials)))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: {}".format(trial.value))

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))

