from fastapi import APIRouter, Request, HTTPException
from services.chat_service import get_chat_history, save_chat_message
from models.chat import ChatHistoryResponse, MessageRequest

router = APIRouter()

@router.get("/chat-history", response_model=ChatHistoryResponse)
async def fetch_chat_history(request: Request):
    try:
        current_user_id = request.state.user
        messages = await get_chat_history(current_user_id)
        return {"user_id": current_user_id, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch chat history")

@router.post("/save-message")
async def save_message(request: Request, message_request: MessageRequest):
    try:
        current_user_id = request.state.user
        await save_chat_message(current_user_id, message_request.message)
        return {"detail": "Message saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save message")
