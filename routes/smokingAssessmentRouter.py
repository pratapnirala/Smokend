from fastapi import APIRouter, Header, HTTPException, status, Depends

from database import database
from models import smokingassessmentmodel
from config.jwt_helper import validate_token
from database.database import client, db

assessmentRouter = APIRouter()


# ===== smoking assessment  Route =====
@assessmentRouter.post("/assessment")
def assessment(data: smokingassessmentmodel.Assessment, token: str = Header(None, alias="smokend-auth-token")):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing in header")
    # validate and extract user_id
    user_id = validate_token(token)
    print("Received token:", token)
    print("Received Body:", data)
    db.assessment.insert_one({"cigarettesPerDay": data.cigarettesPerDay, "yearsSmoking": data.yearsSmoking,
                              "quitAttempts": data.quitAttempts, "motivation": data.motivation,
                              "userID": data.userID})

    return {"success": True, "token": token, "data": data}
