from logger.logger_config import setup_logging
from fastapi import FastAPI
from routers import users

setup_logging()

app = FastAPI(title="RotCom")
app.include_router(users.router)
