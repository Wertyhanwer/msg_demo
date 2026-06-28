from .users import router as users_router
from .auth.login import router as loging_router
from .auth.registration import router as registration_router

__all__ = [users_router, loging_router, registration_router]