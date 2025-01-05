
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml
from transformers import HfArgumentParser

from .data_args import DataArguments
from .inference_args import GeneratingArguments
from .training_args import TraningArguments


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

_TRAIN_ARGS = [TraningArguments,DataArguments]

def _parse_args(parser: HfArgumentParser, args: Optional[Dict[str, Any]] = None) -> Tuple[Any]:

    if args is not None:
        return parser.parse_dict(args)

    if len(sys.argv) == 2 and (sys.argv[1].endswith(".yaml") or sys.argv[1].endswith(".yml")):
        return parser.parse_yaml_file(Path(sys.argv[1]).absolute())


    (*parsed_args, unknown_args) = parser.parse_args_into_dataclasses(return_remaining_strings=True)

    if unknown_args:
        print(parser.format_help())
        print(f"Got unknown args, potentially deprecated arguments: {unknown_args}")
        raise ValueError(f"Some specified arguments are not used by the HfArgumentParser: {unknown_args}")

    return (*parsed_args,)

def _parse_train_args(args: Optional[Dict[str, Any]] = None):
    parser = HfArgumentParser(_TRAIN_ARGS)
    return _parse_args(parser, args)


if __name__ == "__main__":
    training_args,data_args = _parse_train_args()
    
