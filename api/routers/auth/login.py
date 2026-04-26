from fastapi import APIRouter

router = APIRouter(prefix="/login", tags=["login"])

@router.get("/", response_model=...)
def login_user(login: str, password: str):
    ...