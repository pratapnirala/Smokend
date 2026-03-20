import base64

from fastapi import APIRouter, HTTPException, Header, status, Depends
from passlib.context import CryptContext

from database.database import client, db
from models import usermodel
from datetime import datetime, timedelta
from config import config
import jwt
from database import database
from Cryptodome.Cipher import AES
from config.jwt_helper import create_access_token, decode_jwt_token, refresh_token
import base64

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# In-memory "database"
fake_users_db = {}


# encrypted_phone = cipher.encrypt("9876543210".encode())

# ===== Helper Functions =====

def cipherEncrypt(plaintext: str):
    # key = get_random_bytes(16)
    # print("Generated Key (base64):", base64.b64encode(key).decode())
    # encrypted_data= get_random_bytes(16)
    fixed_iv = b"12345678"  # must be correct length
    cipher = AES.new(config.config.cipher_key.encode(), AES.MODE_CTR, nonce=fixed_iv)

    # cipher = AES.new(config.config.cipher_key.encode(), AES.MODE_CTR)
    # iv = cipher.nonce  # Random IV generated automatically

    encrypted_bytes = cipher.encrypt(plaintext.encode())

    # Combine IV + encrypted data and base64 encode
    encrypted_data = base64.b64encode(fixed_iv + encrypted_bytes).decode()
    print("Encrypted:", encrypted_data)
    return encrypted_data


def cipherDecrypt(plaintext: str):
    # ---- Decrypt ----
    fixed_iv = b"12345678"  # must be correct length
    cipher = AES.new(config.config.cipher_key.encode(), AES.MODE_CTR, nonce=fixed_iv)
    decoded = base64.b64decode(plaintext)
    iv_dec = decoded[:len(fixed_iv)]
    encrypted_text = decoded[len(fixed_iv):]

    cipher_dec = AES.new(config.config.cipher_key.encode(), AES.MODE_CTR, nonce=iv_dec)
    decrypted = cipher_dec.decrypt(encrypted_text).decode()
    return decrypted


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, config.config.secret_key, algorithm=config.config.algorithm)
#     return encoded_jwt


def encode_jwt_token(data: dict):
    """
    Encode JWT token without expiration.
    Returns:
        { "jwttoken": "<encoded_token>" }
    """

    try:
        token = jwt.encode(
            data,
            config.config.secret_key,
            algorithm=config.config.algorithm
        )

        return token

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token encoding error: {str(e)}")


# def decode_jwt_token(data: dict):
#     """
#         Decode JWT token when it's received inside a JSON object:
#         { "jwttoken": "<token>" }
#         """
#     print(data)
#     token = data.get("jwttoken")
#     if not token:
#         raise HTTPException(status_code=400, detail="Missing JWT token")
#
#     try:
#         payload = jwt.decode(token, config.config.secret_key, algorithms=[config.config.algorithm])
#         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#         print(payload)
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#

# ===== Signup Route =====
@router.post("/signup")
def signup(user: usermodel.UserSignup):
    # Encrypt data

    userEmail = cipherEncrypt(user.email)
    # print(userEmail)

    userPhone = cipherEncrypt(user.phone)
    if database.users_collection.find_one({"email": userEmail}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = hash_password(user.password)
    database.users_collection.insert_one(
        {"firstname": user.firstname, "lastname": user.lastname, "email": userEmail, "password": hashed_pwd,
         "gender": user.gender, "age": user.age, "phone": userPhone, "createdAt": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
})
    return {"message": "User created successfully"}


# ===== Login Route =====
@router.post("/login")
def login(user: usermodel.UserLogin):
    userEmail = cipherEncrypt(user.email)
    # Find user by plain email
    db_user = database.users_collection.find_one({"email": userEmail})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create token with user details
    access_token = create_access_token(
        data={
            "userEmail": cipherDecrypt(db_user['email']),
            "userID": str(db_user['_id']),  # Convert ObjectId to string
            "userFName": db_user['firstname'],
            "userLName": db_user['lastname'],
            "userMobile": cipherDecrypt(db_user['phone']),
            "userGender": db_user['gender'],
            "userAge": db_user['age']
        },
        expires_delta=timedelta(minutes=config.config.access_token_expire_minutes)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ======= JWT refresh=====
@router.post("/refresh")
def refreshToken(token: str = Header(None, alias="smokend-auth-token")):  # ✅  model name
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing in header")

    payload = refresh_token(decode_jwt_token({"jwttoken": token}))
    return payload


# ====== JWT Decode =====
@router.post("/decode")
def jwttokenDecode(user: usermodel.UserInfoDecode):  # ✅ use correct model name
    payload = decode_jwt_token({"jwttoken": user.jwttoken})  # ✅ pass dict or directly decode
    return payload


@router.get("/ping")
async def ping_db():
    try:
        client.admin.command("ping")
        return {"status": f"MongoDB connected to {db.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")
