import os
import jwt
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("SECRET_KEY")

def create_token(user_id: str) -> str:
    return jwt.encode({"user_id": user_id}, SECRET, algorithm="HS256")

def decode_token(token: str) -> str:
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")