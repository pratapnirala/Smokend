import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
# from fastapi import FastAPI
# from config import config
#
# app = FastAPI(title=config.config.app_name)
#
# @app.get("/")
# def read_root():
#     return {"app_name": config.config.app_name}
