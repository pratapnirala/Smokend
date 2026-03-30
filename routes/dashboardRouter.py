from typing import Optional

from fastapi import APIRouter, Header, HTTPException, status, Depends

from database import database

from config.jwt_helper import validate_token
from database.database import client, db
from datetime import datetime, timedelta
from models.dashboardmodal import Dashboard

DashboardRouter = APIRouter()


# ===== dashboard  Route =====
@DashboardRouter.post("/dashboard")
def dashboard(data: Optional[Dashboard] = None, token: str = Header(None, alias="smokend-auth-token")):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing in header")
    # validate and extract user_id
    user_id = validate_token(token)
    print("Received token:", token)
    print("Received Body:", data)
    # db.dailyCheckIn.insert_one({"mood": data.mood, "motivation": data.motivation,
    #                             "reason": data.reason,
    #                             "userID": user_id, "createdAt": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")})

    return {"success": True, "token": token, "data": {
        "not_smoked": "10%",
        "lung_function": "10%",
        "money_saved": "10%",
        "time_saved": "5:20hr"
    }}
