import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

async def main():
    for url in (settings.database_url, settings.test_database_url):
        engine = create_async_engine(url)
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT current_database()"))
            print(result.scalar_one())
        await engine.dispose()

asyncio.run(main())