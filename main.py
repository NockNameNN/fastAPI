from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables
from router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


