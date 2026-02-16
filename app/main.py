from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="GitHub Repo Intelligence System")

app.include_router(router)
