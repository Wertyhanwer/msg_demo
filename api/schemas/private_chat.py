from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class PrivateChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_: int
    user1_id: int
    user2_id: int
    created_at: datetime
    last_event_at: datetime
    last_message: Optional[str]
