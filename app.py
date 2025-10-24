from fastapi import FastAPI
from routes.userRoutes import router
from routes.askRoutes import askRouter
from config import config
app = FastAPI(title=config.config.app_name)

# Include auth router
app.include_router(router, prefix="/v1")
app.include_router(askRouter, prefix="/v1")