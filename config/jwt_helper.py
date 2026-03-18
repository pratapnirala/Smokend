# config/jwt_helper.py
import jwt
from fastapi import HTTPException, status
from config import config
from datetime import datetime, timedelta


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.config.secret_key, algorithm=config.config.algorithm)
    return encoded_jwt


def refresh_token(data: dict):
    to_encode = data.copy()
    # to_encode.update({"exp": datetime.utcnow() + timedelta(days=7)})
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=30)})
    refreshed = jwt.encode(to_encode,
                           config.config.secret_key, algorithm=config.config.algorithm
                           )
    return refreshed


def validate_token(token: str):
    """
    Validates JWT and returns user_id from payload.
    """
    try:
        payload = jwt.decode(token, config.config.secret_key, algorithms=[config.config.algorithm])
        user_id = payload.get("userID")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_id not found."
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def decode_jwt_token(data: dict):
    """
        Decode JWT token when it's received inside a JSON object:
        { "jwttoken": "<token>" }
        """
    print(data)
    token = data.get("jwttoken")
    if not token:
        raise HTTPException(status_code=400, detail="Missing JWT token")

    try:
        payload = jwt.decode(token, config.config.secret_key, algorithms=[config.config.algorithm])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
