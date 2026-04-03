import logging

from db.exceptions import DatabaseError
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._logger = logging.getLogger("messenger.db")

    async def create(self, username: str, email: str, password_hash: str) -> User:
        self._logger.info(f"User create request {{username: {username}, email: {email}}}")
        try:
            user = User(username=username, email=email, password_hash=password_hash)
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)
            return user
        except Exception as e:
            self._logger.error(f"Error at user creating {username}: {e}")
            raise DatabaseError(f"Error at user creating {username}") from e

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        return user

    async def update_username_by_user_id(self, user_id: int, new_username: str) -> User | None:
       user: User = await self.get_by_id(user_id)
       if user is None:
           return None

       user.username = new_username
       await self._session.commit()
       await self._session.refresh(user)
       return user

    async def delete_user_by_id(self, user_id: int) -> User | None:
        user: User = await self.get_by_id(user_id)
        if user is None:
            return None
        await self._session.delete(user)
        await self._session.commit()
        return user