from passlib.context import CryptContext
from models.user import UserCreate
from db.database import user_collection
from typing import Optional
from pymongo.errors import PyMongoError
from fastapi import HTTPException, status
from utils.logger import logger
from datetime import datetime, timedelta, timezone
from jose import jwt
import os
from dotenv import load_dotenv

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_user_by_email(email: str) -> Optional[dict]:
    try:
        user = await user_collection.find_one({"email": email})
        return user if user else None
    except PyMongoError as e:
        logger.error(f"Database error while fetching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while fetching user data."
        )

async def create_user(user: UserCreate) -> dict:
    try:
        user_data = user.model_dump()
        user_data["password"] = get_password_hash(user_data["password"])
        await user_collection.insert_one(user_data)
        logger.info(f"User created successfully with email: {user.email}")
        return {"email": user.email}
    except PyMongoError as e:
        logger.error(f"Database error while creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating a new user."
        )
