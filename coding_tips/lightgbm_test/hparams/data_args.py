
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


@dataclass
class DataArguments:
    data_dir:str = Field(description="数据文件夹名称")
    train_dataset:str = Field(description="训练数据文件名")
    label_name:str = Field(description="预测列名称")
    drop_col:Optional[str] = Field(description="数据里不想要的字段")
    eval_dataset:Optional[str] = Field(description="测试数据文件名")
    #train_test_split params
    test_size :float = Field(default=0.2)
    random_state:int = Field(default=2025)
