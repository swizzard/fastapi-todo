import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def db() -> asyncpg.Connection:
    return await asyncpg.connect()


class Pool:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool()

    async def disconnect(self):
        self.pool.close()

    async def acquire(self):
        if not self.pool:
            await self.connect()
        return await self.pool.acquire()


pool = Pool()
