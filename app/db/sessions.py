from datetime import datetime
from pydantic import BaseModel
from .db import pool


class Session(BaseModel):
    id: str
    user_id: str
    valid_until: datetime


async def create_session(user_id: str) -> Session:
    query = '''
        INSERT INTO sessions (user_id) VALUES ($1)
        RETURNING id, user_id, valid_until
    '''
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, user_id)
    return Session(id=str(res['id']), user_id=res['user_id'],
                   valid_until=res['valid_until'])


async def get_valid_session(session_id: str, user_id: str):
    query = '''
       SELECT s.valid_until FROM sessions s
       WHERE s.id = $1 AND s.user_id = $2
       AND s.valid_until > NOW()
    '''
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, session_id, user_id)
        return res['valid_until'] if res is not None else res


async def delete_session_by_id(session_id: str):
    async with pool.acquire() as conn:
        await conn.execute('DELETE FROM sessions WHERE id = $1', session_id)


async def delete_session_by_user_id(user_id: str):
    async with pool.acquire() as conn:
        await conn.execute('DELETE FROM sessions WHERE user_id = $1', user_id)
