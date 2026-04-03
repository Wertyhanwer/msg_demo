from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from configs.engine_config import ip, user, password, port, dbname
import logging




# engine = create_async_engine(DATABASE_URL, echo=True)
#
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

class DBEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        self._init_logger()
        self._generate_db_url()
        self._create_async_engine()
        self._create_session_fabric()

        self._initialized = True


    def _generate_db_url(self):
        self._db_url = f"postgresql+asyncpg://{user}:{password}@{ip}:{port}/{dbname}"

    def _init_logger(self):
        self._logger = logging.getLogger("messenger.db")

    def _create_async_engine(self):
        self._db_engine = create_async_engine(
            self._db_url,
            echo=True
        )

    def _create_session_fabric(self):
        self._async_session_maker = async_sessionmaker(
            bind=self._db_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
