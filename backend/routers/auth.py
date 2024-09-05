from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from models.user import UserCreate, UserResponse
from services.auth_service import create_user, get_user_by_email, verify_password
from services.auth_service import create_access_token
from utils.logger import logger
from bson import ObjectId

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    try:
        existing_user = await get_user_by_email(user.email)

        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )
        
        new_user = await create_user(user)
        logger.info(f"New user registered with email: {user.email}")
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration."
        )

@router.post("/login")
async def login_user(login_request: LoginRequest):
    try:
        user = await get_user_by_email(login_request.email)

        if not user or not verify_password(login_request.password, user["password"]):
            logger.warning(f"Failed login attempt for email: {login_request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password."
            )

        user_id_str = str(user["_id"])

        access_token = create_access_token(data={"sub": user_id_str})

        logger.info(f"User logged in successfully: {login_request.email}")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "user_id": user_id_str,
                "email": user["email"]
            }
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login."
        )
