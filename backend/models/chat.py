from pydantic import BaseModel
from datetime import datetime
from typing import List
class ChatMessage(BaseModel):
    from_user: str
    message: str
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    user_id: str
    messages: List[ChatMessage]
    
class MessageRequest(BaseModel):
    message: str
