from collections import defaultdict
from enum import Enum
from typing import Dict, Optional, OrderedDict


class DownloadSource(str, Enum):
    DEFAULT = "hf"
    MODELSCOPE = "ms"
    OPENMIND = "om"

SUPPOERTED_MODELS = OrderedDict()

DEFAULT_TEMPLATE = defaultdict(str)
VISION_MODELS = set()


def register_model_group(
    models:Dict[str,Dict[DownloadSource,str]],
    tempalte:Optional[str]=None,
    vision:bool = False
):
    for name,path in models.items():
        SUPPOERTED_MODELS[name] = path
        if tempalte is not None and any(suffix in name for suffix in ("-Chat","-Instruct")):
            DEFAULT_TEMPLATE[name] = tempalte
        if vision:
            VISION_MODELS.add(name)
            



register_model_group(
        models = {
            "Baichuan-7B-Base":{DownloadSource.DEFAULT:"baichuan-inc/Baichuan-7B-Base",
                                DownloadSource.MODELSCOPE:"baichuan-inc/Baichuan-7B-Base",
                                DownloadSource.OPENMIND:"baichuan-inc/Baichuan-7B-Base",
                                },
        })


if __name__ == "__main__":
    print(SUPPOERTED_MODELS)
    print(DEFAULT_TEMPLATE)
    print(VISION_MODELS)
