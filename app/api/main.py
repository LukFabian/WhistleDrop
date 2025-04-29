from fastapi import APIRouter
from app.api.routes import upload, download

api_router = APIRouter()
api_router.include_router(router=upload.router)
api_router.include_router(router=download.router)