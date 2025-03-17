from fastapi import APIRouter

from app.infrastructure.api.rest.v1.project_analytics import router as project_analytics

api = APIRouter()

api.include_router(project_analytics, prefix="/v1/projects", tags=["project_analytics"])
