from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token")
        return user_id
    except jwt.JWTError:
        raise ValueError("Invalid token")

class TokenVerificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_routes = ["/auth/login", "/auth/register"]
        
        if any(route in request.url.path for route in public_routes):
            return await call_next(request)
        
        authorization: str = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization required")
        
        token = authorization.split(" ")[1]
        try:
            user_id = decode_access_token(token)
            request.state.user = user_id
        except ValueError as e:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        response = await call_next(request)
        return response
