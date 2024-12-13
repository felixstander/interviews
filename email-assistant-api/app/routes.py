from os import openpty
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.config import Config

from .crud import crud_email_log
from .database import get_session
from .schemas import EmailLogCreated, EmailRequest, EmailResponse

current_file_dir = Path(__file__).resolve()
env_path = current_file_dir / ".env"


config = Config(env_path)


OPENAI_API_KEY = config("OPENAI_API_KEY")
open_ai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

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

    try:        
        system_prompt = f"""
        You are a helpful email assistant.
        You get a prompt to write an email,
        you reply with the email and nothing else.
        """
        prompt = f"""
        Write an email based on the following input:
        - User Input: {request.user_input}
        - Reply To: {request.reply_to if request.reply_to else 'N/A'}
        - Context: {request.context if request.context else 'N/A'}
        - Length: {request.length if request.length else 'N/A'} characters
        - Tone: {request.tone if request.tone else 'N/A'}
        """

        response = await open_ai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":prompt}
            ],
            max_tokens=request.length
        )
        generated_email = response.choices[0].message['content'].strip()
        log_entry = EmailLogCreated(user_id=request.user_id,
                                   user_input=request.user_input,            
                                   reply_to=request.reply_to,            
                                   context=request.context,            
                                   length=request.length,            
                                   tone=request.tone,            
                                   generated_email=generated_email,        
                                   )        
        await crud_email_log.create(db, log_entry)

        return EmailResponse(generated_email=generated_email)

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))






