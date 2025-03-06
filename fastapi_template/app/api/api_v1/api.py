# app/api/api_v1/api.py
from fastapi import APIRouter
from app.api.api_v1.endpoints import cve, projects, analysis

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(
    cve.router,
    prefix="/cves",
    tags=["cves"]
)

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"]
)

api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)