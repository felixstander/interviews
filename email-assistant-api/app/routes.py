from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.config import Config

from .crud import crud_email_log
from .database import get_session
from .schemas import EmailRequest, EmailResponse

current_file_dir = Path(__file__).resolve()
env_path = current_file_dir / ".env"


config = Config(env_path)


OPENAI_API_KEY = config("OPENAI_API_KEY")
open_ai_client = OpenAI(api_key=OPENAI_API_KEY)

"""
为电子邮件终端节点创建一个路由器,并实际为电子邮件创建终端节点:
- 创建一个系统提示符,使输出适应我们想要的结果
- 创建一个基本提示,用于格式化传递的信息
- 将此信息传递给OpenAI客户端;
- 最后将在数据库中创建一个日志条目并返回生成的电子邮件
"""


# --------email--------
email_router = APIRouter()
@email_router.post("/",response_model=EmailResponse)
async def generate_email(request:EmailRequest,db:AsyncSession=Depends(get_session)):
    try



