from datetime import datetime
from pydantic import BaseModel
from .db import pool


class BaseItem(BaseModel):
    user_id: str
    description: str | None


class Item(BaseItem):
    id: str
    created_at: datetime
    done: bool


class Pagination(BaseModel):
    limit: int
    offset: int


async def create_item(create_data: BaseItem) -> Item:
    query = """
        INSERT INTO items (user_id, description)
        VALUES ($1, $2)
        RETURNING id, user_id, description, done, created_at
    """
    async with pool.acquire() as conn:
        res = await conn.fetchrow(query, create_data.user_id, create_data.description)
    return Item(
        id=str(res["id"]),
        user_id=res["user_id"],
        description=res["description"],
        done=res["done"],
        created_at=res["created_at"],
    )


async def get_user_items(user_id: str, pagination: Pagination | None) -> list[Item]:
    query = """
        SELECT id, user_id, description, done, created_at
        FROM items
        WHERE user_id = $1
        ORDER BY created_at DESC
        LIMIT $2 OFFSET $3
    """
    if pagination:
        limit = pagination.limit
        offset = pagination.offset
    else:
        limit = 10
        offset = 0
    if pagination is None:
        pagination = Pagination(limit=10, offset=0)
    async with pool.acquire() as conn:
        res = await conn.fetch(query, user_id, limit, offset)
    return [
        Item(
            id=str(row["id"]),
            user_id=row["user_id"],
            description=row["description"],
            done=row["done"],
            created_at=row["created_at"],
        )
        for row in res
    ]


async def mark_item_done(item_id: str, done: bool):
    async with pool.acquire() as conn:
        res = await conn.fetchrow(
            "UPDATE items SET done = $1 WHERE id = $2", done, item_id
        )
    return Item(
        id=str(res["id"]),
        user_id=str(res["user_id"]),
        description=res["description"],
        created_at=res["created_at"],
        done=res["done"],
    )
