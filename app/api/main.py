from fastapi import APIRouter
from app.api.routes import upload, download, login, register

api_router = APIRouter()
api_router.include_router(router=upload.router)
api_router.include_router(router=download.router)
api_router.include_router(router=login.router)
api_router.include_router(router=register.router)
