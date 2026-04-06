from typing import Optional

from fastapi import APIRouter, Header, HTTPException, status, Depends

from database import database

from config.jwt_helper import validate_token
from database.database import client, db
from datetime import datetime, timedelta

from models.achievementmodal import Achievement

AchievementRouter = APIRouter()


# ===== Achievement  Route =====
@AchievementRouter.post("/achievement")
def achievement(data: Achievement, token: str = Header(None, alias="smokend-auth-token")):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing in header")
    # validate and extract user_id
    user_id = validate_token(token)

    result = db.achievement.insert_one({
        "not_smoked": data.not_smoked,
        "go_for_run": data.go_for_run,
        "finished_book": data.finished_book,
        "notes": data.notes,
        "userID": user_id,
        "createdAt": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
    }
    )

    return {"success": True, "token": token, "data": data, "inserted_id": str(result.inserted_id)
            }
