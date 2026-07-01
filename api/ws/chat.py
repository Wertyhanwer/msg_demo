from fastapi import APIRouter, WebSocket
import logging

from db.repository.message_repository import MessageRepository
from routers.service.JWT.token_decode import decode_token
from routers.service.JWT.token_payload_model import TokenPayloadModel
from db.repository.private_chat_repository import PrivateChatRepository
from db.repository.user_repository import UserRepository
from dependencies.db import get_session
from .connection_manager import connection_manager

router = APIRouter(prefix="/ws", tags=["ws"])

logger = logging.getLogger("messenger.ws")

@router.websocket("/{other_user_id}")
async def chat(websocket: WebSocket, other_user_id: int, token: str):
    await websocket.accept()

    logger.info(f"Ws request chat get or create by: {other_user_id}")
    token_model: TokenPayloadModel = decode_token(token)
    current_user_id = int(token_model.sub)

    async with get_session() as session:
        user_rep = UserRepository(session)
        private_chat_rep = PrivateChatRepository(session)

        current_user = await user_rep.get_by_id(current_user_id)
        if not current_user:
            logger.info(f"Ws connection closed! current_user: {other_user_id} does not exists")
            await websocket.close(code=1008)
            return

        other_user = await user_rep.get_by_id(other_user_id)
        if not other_user:
            logger.info(f"Ws connection closed! other_user: {other_user} does not exists")
            await websocket.close(code=1008)
            return

        private_chat = await private_chat_rep.get_by_users(current_user, other_user)
        if not private_chat:
            private_chat = await private_chat_rep.create(current_user, other_user)

    await connection_manager.connect(current_user.id_, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            async with get_session() as session:
                message_rep = MessageRepository(session)
                await message_rep.create(private_chat.id_, current_user.id_, data)
            await connection_manager.send_to(other_user.id_, data)
    finally:
        connection_manager.disconnect(current_user.id_)
