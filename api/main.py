from logger import setup_logging
import asyncio


def start_logger():
    logger = setup_logging()


async def main():
    start_logger()
    db = Database()  # logger уже готов внутри!
    await db.connect()
    # ...

asyncio.run(main())