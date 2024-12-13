from database import create_db_and_tables
from fastapi import FastAPI


async def lifespan(app):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
