from fastapi import APIRouter

from app.api.v1.endpoints import auth, company, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(company.router, prefix="/companies", tags=["companies"])
router.include_router(users.router, prefix="/users", tags=["users"])
