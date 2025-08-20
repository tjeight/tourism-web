from datetime import timedelta, datetime
from fastapi import Depends
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import jwt


load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 7


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expire_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    to_encode = data.copy()
    if expire_delta:
        expire_time = datetime.now() + expire_delta
    else:
        expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict, expire_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_MINUTES)
) -> str:
    to_encode = data.copy()
    if expire_delta:
        expire_time = datetime.now() + expire_delta
    else:
        expire_time = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> dict:
    global ALGORITHM
    if ALGORITHM is None:
        ALGORITHM = "HS256"
    payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    if not payload:
        raise Exception("Invalid refresh token")
    return payload


def get_current_user(token: str) -> dict:
    try:
        global ALGORITHM
        if ALGORITHM is None:
            ALGORITHM = "HS256"
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    except Exception as e:
        raise Exception(f"An error occurred while decoding the token: {str(e)}")


def user_required(current_user=Depends(get_current_user)) -> bool:
    if not current_user or current_user.get("role") != "user":
        raise Exception("User authentication required")
    return True


def admin_required(current_user=Depends(get_current_user)) -> bool:
    if not current_user or current_user.get("role") != "admin":
        raise Exception("Admin authentication required")
    return True
