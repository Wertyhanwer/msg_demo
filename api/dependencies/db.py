from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import DBEngine

async def get_session():
    engine = DBEngine()
    async with engine.get_session() as session:
        yield session
