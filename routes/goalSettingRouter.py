from fastapi import APIRouter, Header, HTTPException, status, Depends

from database import database
from models import goalsettingmodel
from config.jwt_helper import validate_token
from database.database import client, db

GoleSettingRouter = APIRouter()


# ===== smoking assessment  Route =====
@GoleSettingRouter.post("/golesetting")
def golesetting(data: goalsettingmodel.smokgoleset, token: str = Header(None, alias="smokend-auth-token")):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing in header")
    # validate and extract user_id
    user_id = validate_token(token)
    print("Received token:", token)
    print("Received Body:", data)
    db.golesetting.insert_one({"mainReason": data.main_reason, "customReason": data.custom_reason,
                               "userID": user_id})

    return {"success": True, "token": token, "data": data}
