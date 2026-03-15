from fastapi import APIRouter
from app.users.routes import router as user_router
from app.auth.routes import router as auth_router
from app.auth.otp_routes import router as otp_router
from app.groups.routes import router as group_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(otp_router)
api_router.include_router(group_router)
