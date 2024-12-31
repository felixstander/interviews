### Playground


1. Agents



2. api_app
- 可用or来表示有其他空值时用某种类型的空值表示，比如说空list
```python
#比如说输入是空string("")时,用空list表示
valid_cors = cors_origin_list or []
```


3. router
```python
from fastapi.routing import APIRouter
#构造某个大模块的router
playground_router = APIRouter(prefix="/playground", tags=["Playground"])
#该大模块下的子块
@playground_router.get("/status")
def playground_status():
    return {"playground": "available"}
```
