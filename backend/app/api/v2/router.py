from fastapi import APIRouter

from app.api.v2.endpoints import users

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
