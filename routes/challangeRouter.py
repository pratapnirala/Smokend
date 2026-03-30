from typing import Optional

from fastapi import APIRouter, Header, HTTPException, status, Depends

from database import database

from config.jwt_helper import validate_token
from database.database import client, db
from datetime import datetime, timedelta

from models.challangemodel import Challange

ChallangeRouter = APIRouter()

# ===== challange  Route =====
@ChallangeRouter.post("/challange")
def challange(data: Challange, token: str = Header(None, alias="smokend-auth-token")):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing in header")
    # validate and extract user_id
    user_id = validate_token(token)
    print("Received token:", token)
    print("Received Body:", data)

    db.challange.insert_one({"insomnia": data.insomnia, "infoxin": data.infoxin,
                             "craving": data.craving,
                             "extraInfo": data.extraInfo,
                             "userID": user_id, "createdAt": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")})

    return {"success": True, "token": token, "data": data}
