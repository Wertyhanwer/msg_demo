from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from configs.engine_config import ip, user, password, port, dbname



engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class DBEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Создаю единственный экземпляр!")
        return cls._instance

    def __init__(self):
        self._db_url = self._generate_db_url()

    @staticmethod
    def _generate_db_url():
        db_url = f"postgresql+asyncpg://{user}:{password}@{ip}:{port}/{dbname}"
        return db_url
