from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routes.adminRoutes import adminRouter
from routes.dailycheckInRouter import DailyCheckInRouter
from routes.dashboardRouter import  DashboardRouter
from routes.smokingAssessmentRouter import assessmentRouter
from routes.goalSettingRouter import GoleSettingRouter
from routes.userRoutes import router
from routes.askRoutes import askRouter
from routes.videoRoutes import videoRouter

from config import config

app = FastAPI(title=config.config.app_name)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*",                       # Only for development
    "https://yourwebsite.com",  # Production domain
    "exp://*",                 # For React Native Expo
    "http://localhost:19006",  # React Native Metro
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ✅ Serve assets (static files)
app.mount("/admin/assets", StaticFiles(directory="assets"), name="assets")
# Include auth router
app.include_router(router, prefix="/v1")
app.include_router(askRouter, prefix="/v1")
app.include_router(videoRouter, prefix="/v1")
app.include_router(assessmentRouter, prefix="/v1")
app.include_router(GoleSettingRouter, prefix="/v1")
app.include_router(DailyCheckInRouter, prefix="/v1")
app.include_router(DashboardRouter, prefix="/v1")
app.include_router(adminRouter, prefix="/admin")
