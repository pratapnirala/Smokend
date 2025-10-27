from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext

from database.database import client, db
from models import usermodel
from datetime import datetime, timedelta
from config import config
import jwt
from database import database


router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory "database"
fake_users_db = {}


# ===== Helper Functions =====
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.config.secret_key, algorithm=config.config.algorithm)
    return encoded_jwt


def decode_jwt_token(data: dict):
        """
        Decode JWT token when it's received inside a JSON object:
        { "jwttoken": "<token>" }
        """

        token = data.get("jwttoken")
        if not token:
            raise HTTPException(status_code=400, detail="Missing JWT token")

        try:
            payload = jwt.decode(token, config.config.secret_key, algorithms=[config.config.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

# ===== Signup Route =====
@router.post("/signup")
def signup(user: usermodel.UserSignup):
    if database.users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = hash_password(user.password)
    database.users_collection.insert_one(
        {"firstname": user.firstname, "lastname": user.lastname, "email": user.email, "password": hashed_pwd,
         "gender": user.gender, "age": user.gender})
    return {"message": "User created successfully"}


# ===== Login Route =====
@router.post("/login")
def login(user: usermodel.UserLogin):
    db_user = database.users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token(data={"userEmail": user.email},
                                       expires_delta=timedelta(minutes=config.config.access_token_expire_minutes))
    return {"access_token": access_token, "token_type": "bearer"}


# ====== JWT Decode =====
@router.post("/decode")
def jwttokenDecode(user:usermodel.UserInfoDecode):  # ✅ use correct model name
    payload = decode_jwt_token({"jwttoken": user.jwttoken})  # ✅ pass dict or directly decode
    return payload

@router.get("/ping")
async def ping_db():
    try:
        client.admin.command("ping")
        return {"status": f"MongoDB connected to {db.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")
