from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ConfigurationError
import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI")

try:
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client.aici
    user_collection = database.get_collection("users")
    logger.info("Successfully connected to the database.")
except (ConnectionFailure, ConfigurationError) as e:
    logger.error(f"Database connection error: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to connect to the database."
    )
