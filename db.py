import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def db():
    return await asyncpg.connect()
