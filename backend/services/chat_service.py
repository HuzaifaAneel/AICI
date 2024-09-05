from db.database import user_collection
from datetime import datetime, timezone

async def save_chat_message(user_id: str, message: str):
    chat_message = {
        "from_user": user_id,
        "message": message,
        "timestamp": datetime.now(timezone.utc),
    }
    await user_collection.update_one(
        {"user_id": user_id},
        {"$push": {"chats": chat_message}},
        upsert=True
    )

async def get_chat_history(user_id: str):
    user_chat = await user_collection.find_one({"user_id": user_id}, {"chats": 1})
    if user_chat and "chats" in user_chat:
        return user_chat["chats"]
    return []
