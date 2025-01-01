
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

from .inference_args import GeneratingArguments


def parse_args() -> Optional[GeneratingArguments]:

    if len(sys.argv) == 2 and (sys.argv[1].endswith(".yaml") or sys.argv[1].endswith(".yml")):
        with open(Path(sys.argv[1]).absolute(),'r') as file:
            yaml_content = yaml.safe_load(file)
        if "infer" in sys.argv[1].lower():
            args = GeneratingArguments(**yaml_content)
        elif "train" in sys.argv[1].lower():
            #TODO:添加train args
            args = None
        else:
            raise ValueError(f"yaml文件名{sys.argv[1]}并不包含在可选性中，请重新修改文件名")

        return args
    return 


