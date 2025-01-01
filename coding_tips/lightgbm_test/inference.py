from pathlib import Path
from typing import Any, Dict, Optional, cast

import lightgbm as lgb
import numpy as np
import pandas as pd
from hparams.inference_args import GeneratingArguments
from hparams.parser import parse_args
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score)


class Inference:
    def __init__(self,infer_args:GeneratingArguments) -> None:

        
        self.infer_args = infer_args

        #数据
        data_path = Path(__file__).absolute().parent / self.infer_args.data_dir/ f"{self.infer_args.dataset}.csv"
        df = self.read_data(str(data_path))
        label_name = self.infer_args.label_name
        self.label = df.loc[:,label_name]
        drop_col = self.infer_args.drop_col + [label_name] #type:ignore
        self.feature = df.drop(drop_col,axis=1)



        #模型
        model_path = Path(__file__).absolute().parent / self.infer_args.model_dir/ f"{self.infer_args.model_name}" / "model.txt"
        self.model = lgb.Booster(model_file=model_path)


    @staticmethod
    def read_data(data_path:str)->pd.DataFrame:

        df= pd.read_csv(data_path)
        return df
        
    def predict(self)->np.ndarray:

        assert self.infer_args.use_model or self.infer_args.use_url,"确保用模型或者api其中一个进行预测"
        y_pred = np.ndarray([])

        if self.infer_args.use_model:
            y_pred = cast(np.ndarray,self._predict_by_model(self.feature))
        elif self.infer_args.use_url:
            pass

        return y_pred


    def _predict_by_model(self,x_test:pd.DataFrame)->np.ndarray:

        #这里是概率
        y_pred = self.model.predict(x_test)
        return cast(np.ndarray,y_pred)
        

    def _predict_by_url(self,infer_url:str):
        pass

    def calculate_auc_score(self,y_pred:np.ndarray):
        
        auc_pickled_model = roc_auc_score(self.label, y_pred)
        print(f"The ROC AUC of pickled model's prediction is: {auc_pickled_model:.2f}")

        return auc_pickled_model
    def calculate_accuracy(self,y_pred:np.ndarray):
        
        "计算分类正确率"

        y_pred = (y_pred>0.5).astype(int) #把大于0.5的值转化为1
        accuracy_rate = accuracy_score(self.label,y_pred,normalize=True)
        print(f"The Accuracy of pickled model's prediction is: {accuracy_rate:.2f}")
        return accuracy_rate

    
        
if __name__ == "__main__":
    infer_args = parse_args()

    if infer_args is None:
        raise ValueError("推理参数为空，请检查输入的参数")
    infer = Inference(infer_args)
    y_pred = infer.predict()
    auc_score = infer.calculate_auc_score(y_pred)
    accuracy_score = infer.calculate_accuracy(y_pred)
    
