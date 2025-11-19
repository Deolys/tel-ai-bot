from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel


class UserSession(BaseModel):
    id: str
    telegram_user_id: int
    username: str = ""
    first_name: str = ""
    conversation_context: Dict = {}
    created_at: datetime
    updated_at: datetime


class ChatMessage(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime
