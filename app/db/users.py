from pydantic import BaseModel
from .db import pool


class PubUser(BaseModel):
    nick: str | None
    email: str


class User(PubUser):
    id: str


class UpdateUserNick(PubUser):
    pass


class UpdateUserEmail(BaseModel):
    id: str
    new_email: str


async def create_user(to_insert: PubUser):
    query = 'INSERT INTO users (nick, email) VALUES ($1, $2)'
    async with pool.acquire() as conn:
        await conn.execute(query, to_insert.nick, to_insert.email)


async def delete_user(user_id: str):
    query = 'DELETE FROM users WHERE id = $1'
    async with pool.acquire() as conn:
        await conn.execute(query, user_id)


async def update_user_nick(update_data: UpdateUserNick):
    query = 'UPDATE users SET nick = $1 WHERE email = $2'
    async with pool.acquire() as conn:
        await conn.execute(query, update_data.nick, update_data.email)


async def update_user_email(update_data: UpdateUserEmail):
    query = 'UPDATE users SET email = $1 WHERE id = $2'
    async with pool.acquire() as conn:
        await conn.execute(query, update_data.new_email, update_data.id)
