from fastapi import APIRouter
from app.api.routes import upload

api_router = APIRouter()
api_router.include_router(router=upload.router)