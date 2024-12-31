### 结构
1.ABC和abstractmethod的作用
- 定义一个可以被继承的基础类,保证子继承类必须得有相同的变量和函数
- 写法
```python 
from abc import ABC,abstractmethod

class BaseEngine(ABC):
    r"""
    Base class for inference engine of chat models.

    Must implements async methods: chat(), stream_chat().
    """

    model: Union["PreTrainedModel", "AsyncLLMEngine"]
    tokenizer: "PreTrainedTokenizer"
    template: "Template"
    generating_args: Dict[str, Any]

    @abstractmethod
    def __init__(
        self,
        model_args: "ModelArguments",
        data_args: "DataArguments",
    ) -> None:
        r"""
        Initializes an inference engine.
        """
        ...

    @abstractmethod
    async def chat(
        self,
        messages: Sequence[Dict[str, str]],
        system: Optional[str] = None,
        **input_kwargs,
    ) -> List["Response"]:
        r"""
        Gets a list of responses of the chat model.
        """
        ...

    @abstractmethod
    async def stream_chat(
        self,
        messages: Sequence[Dict[str, str]],
        system: Optional[str] = None,
        **input_kwargs,
    ) -> AsyncGenerator[str, None]:
        r"""
        Gets the response token-by-token of the chat model.
        """
        ...
```
- 使用场景：在有多个不同场景下运用相同的api，但是具体实现方式是不同的情况下。


### python内置函数
1. **filter**
- 可以初步筛选出 list 里面符合条件的元素
```python
has_placeholder = False
for slot in filter(lambda s: isinstance(s, str), slots):
    #这里是去找{xxx}
    if re.search(r"\{\{[a-zA-Z_][a-zA-Z0-9_]*\}\}", slot):
        has_placeholder = True
```
2. **defaultdict**
- defaultdict可以在创建字典前就指定 value 类型
- 无需判断key是否存在于字典中，可以直接进行添加并赋值
```python
from collections import defaultdict
dic = defaultdict(int)
for c in s:
    dic[c]+=1
```
### Typing
1. **Callable**
- 定义某个函数的入参和出参
```python
from typing import Callable
func = Callable[...,None] #这里不指定入参类型，输出为 None
func = Callable[[str,int],None] #指定入参的第一参数为str,第二参数为int
```
- callble也可以用来定义简单的lambda类型
```python
#这里在lambda里面的n,text无法用typing去指定类型，但是可以用callable去指定
multiply:Callable[[int,str],str] = lambda n,text:n*text
print(multiply(10,'1'))
```
### asyncio和thread
1. 协程和多线程可以同时启用

- [单核处理器为什么需要线程](https://www.bilibili.com/list/watchlater?oid=113567089035565&bvid=BV1eCz6YVEAb&spm_id_from=333.1245.top_right_bar_window_view_later.content.click)
```python
import asyncio
def _start_background_loop(loop: "asyncio.AbstractEventLoop") -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

self._loop = asyncio.new_event_loop()
self._thread = Thread(target=_start_background_loop, args=(self._loop,), daemon=True)
self._thread.start()

#llama_factory src/llamafactory/chat/chat_model/74 lines
def chat(...):
    task = asyncio.run_coroutine_threadsafe(
        self.achat(messages, system, tools, images, videos, **input_kwargs), self._loop
    )
    return task.result()
```


### Generator和yield
1. 当内存不足，或者不需要把整个数据load进内存的时候使用
```python
def generator(path):
    with open(path,'r') as f:
        for line in f:
            yield line.strip()
for line in generator(file_path)
    pass
```
2. asyn generator，协程生成器
- vllm的generate是生成一个迭代器而分直接的结果，可以通过迭代器再去判断是否需要流式。
```python
# src/llamafactory/chat/vllm_engine/VllmEngine
from vllm import (AsyncEngineArgs, AsyncLLMEngine, RequestOutput,SamplingParams)

engine_args = {
    "model": model_args.model_name_or_path,
    "trust_remote_code": True,
    "download_dir": model_args.cache_dir,
    "dtype": model_args.infer_dtype,
    "max_model_len": model_args.vllm_maxlen,
    "tensor_parallel_size": get_device_count() or 1,
    "gpu_memory_utilization": model_args.vllm_gpu_util,
    "disable_log_stats": True,
    "disable_log_requests": True,
    "enforce_eager": model_args.vllm_enforce_eager,
    "enable_lora": model_args.adapter_name_or_path is not None,
    "max_lora_rank": model_args.vllm_max_lora_rank,
}

model = AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**engine_args))

async def _generate(messages:Sequence[Dict[str,str]],system:Optional[str]):
    result_generator = self.model.generate(
        {"prompt_token_ids": prompt_ids, "muenchti_modal_data": multi_modal_data},
        sampling_params=sampling_params,
        request_id=request_id,
        lora_request=self.lora_request,
    )
    return result_generator
async def chat(messages:Sequence[Dict[str,str]],system:Optional[str]):
    final_output = None
    generator = await _generate(messages,system)

    aysnc for request_output in generator:
        final_output = request_output

    results = []
    for output in final_output.outputs:
        results.append(
            Response(response_text=output.text)
        )
```


### Test相关

1. 命名格式
- 建立tests文件夹
- 每个test文件必须以test_xxx.py命名，不然unittest识别不了
- 每个class得以TestXxx命名
- 每个method得以test_xxx命名

2. 启动形式
```python
#在最外层文件夹进行shell命令
python -m unittest
```


3. mock and patch 

- patch可以用于模拟API调用, ***定义***: patch装饰器或上下文管理器是特别常用的，用于模拟和替换外部模块或者函数行为，在测试哪些依赖外部服务(如API)的代码时非常实用。