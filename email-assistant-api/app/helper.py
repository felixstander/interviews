
from datetime import UTC, datetime, timedelta
from pathlib import Path
from re import L
from typing import Annotated, Any

import bcrypt
from crud import crud_user
from database import get_session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from starlette.config import Config

current_file_dir = Path(__file__).resolve()
env_path = current_file_dir / ".env"


config = Config(env_path)


SECRET_KEY = config("SECRET_KEY")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



class Token(SQLModel):
    access_token:str
    token_type:str

class TokenData(SQLModel):
    username_or_email:str


# Utility functions
async def verify_password(plain_password: str, hashed_password: str) -> bool:    
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def create_access_token(data: dict[str, Any],expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta    
    else:
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=15)    

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

async def verify_token(token: str, db: AsyncSession) -> TokenData | None:    
    """Verify a JWT token and extract the user data."""    
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])        
        username_or_email: str = payload.get("sub")        
        if username_or_email is None:            
            return None        
        return TokenData(username_or_email=username_or_email)    

    except JWTError:
        return None


async def authenticate_user(username_or_email: str, password: str, db: AsyncSession):    
    if "@" in username_or_email:        
        db_user: dict | None = await crud_user.get(db=db, email=username_or_email, is_deleted=False)    
    else:        
        db_user = await crud_user.get(db=db, username=username_or_email, is_deleted=False)    
    if not db_user:        
        return False    
    elif not await verify_password(password, db_user["hashed_password"]):
        return False    

    return db_user



#Dependency 
async def get_current_user(token:Annotated[str,Depends(oauth_scheme)],
                           db:Annotated[AsyncSession,Depends(get_session)]) -> dict[str,Any]|None:
    "get the current authenticated user"

    token_data = await verify_token(token,db)
    if token_data is None:
        raise HTTPException(status_code=404,detail="User not authenticated.")

    if "@" in token_data.username_or_email:
        user = await crud_user.get(
            db=db, email=token_data.username_or_email,is_deleted=False
        )
    else:
        user = await crud_user.get(
            db=db, username=token_data.username_or_email,is_deleted=False
        )
    if user:
        return user
    raise HTTPException(status_code=401,detail="User not authenticated.")



