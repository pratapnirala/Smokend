from typing import Optional

from fastapi import APIRouter, Header, HTTPException, status, Depends

from database import database

from config.jwt_helper import validate_token
from database.database import client, db
from models.usertrackingmodal import UserTracking

UserTrackingRouter = APIRouter()


# ===== User Tracking  Route =====
@UserTrackingRouter.get("/usertracking")
def usertracking(data: Optional[UserTracking] = None, token: str = Header(None, alias="smokend-auth-token")):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing in header")
    # validate and extract user_id
    user_id = validate_token(token)
    # print("Received token:", token)
    # print("Received Body:", data)
    # Query MongoDB
    results = list(db.dailyCheckIn.find({"userID": user_id}, {"_id": 0}))
    # "_id":0 removes the ObjectId field if you don’t want it in the response

    return {
        "success": True,
        "token": token,
        "data": results
    }

