from fastapi import APIRouter

from app.api.endpoints import charity_project, donation, user

router = APIRouter()

router.include_router(
    charity_project.router,
    prefix="/charity_project",
    tags=["charity_projects"],
)
router.include_router(donation.router, prefix="/donation", tags=["donations"])
router.include_router(user.router)
