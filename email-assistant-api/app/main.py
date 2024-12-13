from database import create_db_and_tables
from fastapi import FastAPI
from routes import email_router


async def lifespan(app):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(email_router,prefix='/generate',tags=["Email"])
