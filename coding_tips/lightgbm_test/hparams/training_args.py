
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, validator


class TraningArguments(BaseModel):
    boosting_type:str = Field(default='gbdt')
    objective:str = Field(default='binary')
    metric:str = Field(default='binary_logloss')
    num_leaves:int =Field(default=31)
    learning_rate:float =  Field(default=0.05)
    #通过设置 feature_fraction 来使用特征子抽样
    feature_fraction:float = Field(default=0.9)
    bagging_fraction:float = Field(default=0.8)
    bagging_freq:int = Field(default=5)
    verbose:int = Field(default=0)
    num_boost_round:int =Field(default=10)
    #dataset
    test_size :float = Field(default=0.2)
    random_state:int = Field(default=2025)


