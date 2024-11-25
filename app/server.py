from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.connect()
    yield
    await pool.disconnect()


app = FastAPI(lifespan=lifespan)
