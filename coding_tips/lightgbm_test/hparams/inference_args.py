from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, validator


class GeneratingArguments(BaseModel):
    data_dir:str = Field(description="数据文件夹名称")
    dataset:str = Field(description="数据文件名")
    label_name:str = Field(description="预测列名称")
    drop_col:Optional[str] = Field(description="数据里不想要的字段")
    model_dir:str = Field(description="存放模型权重的文件夹名称")
    model_name:str = Field(description="模型文件名称")
    use_url:bool = Field(default=False,description="用模型参数进行预测")
    use_model:bool = Field(default=False,description="用server api进行预测")
    model_config = ConfigDict(protected_namespaces=())


    @validator("drop_col")
    def change_drop_col_type(cls,drop_col:Optional[str]=None)->List:
        if drop_col is not None:
            return drop_col.split(",")
        return []
            


