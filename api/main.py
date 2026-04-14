import asyncio

from logger import setup_logging
from fastapi import FastAPI
from routers import users



async def main():
    setup_logging()

    app = FastAPI()
    app.include_router(users.router)


if __name__ == "__main__":
    asyncio.run(main())