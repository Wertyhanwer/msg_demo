from logger.logger_config import setup_logging
from fastapi import FastAPI
from routers import users_router, registration_router, loging_router

setup_logging()

app = FastAPI(title="RotCom")
app.include_router(users_router)
app.include_router(registration_router)
app.include_router(loging_router)