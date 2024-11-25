import os
import asyncio
import asyncpg
from db import db


async def run_migration(conn: asyncpg.Connection, migration: str) -> None:
    async with conn.transaction():
        await conn.execute(migration)


def get_migrations():
    migrations_dir = os.environ['MIGRATIONS_DIRECTORY']
    migrations = sorted(os.listdir(migrations_dir))
    for migration in migrations:
        full = os.path.join(migrations_dir, migration)
        print(f'running {full}')
        with open(full) as f:
            yield f.read()


async def run_migrations():
    conn = await db()
    for migration in get_migrations():
        await run_migration(conn, migration)
    await conn.close()


if __name__ == '__main__':
    asyncio.run(run_migrations())
    print('Migrations complete!')
