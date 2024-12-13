### 结构
1.ABC和abstractmethod的作用
- 定义一个可以被继承的基础类,保证子继承类必须得有相同的变量和函数
- 写法
```python 
from abc import ABC,abstractmethod
```
- 使用场景：在有多个不同场景下运用相同的api，但是具体实现方式是不同的情况下。


### python内置函数
1. **filter**
- 可以初步筛选出 list 里面符合条件的元素
```python
has_placeholder = False
for slot in filter(lambda s: isinstance(s, str), slots):
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

### asyncio和thread
1. 协程和多线程可以同时启用
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

