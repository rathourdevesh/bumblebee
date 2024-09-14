from fastapi import APIRouter

from app.api.routes import users, services, health

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(services.router, prefix="/services", tags=["services"])

health_router = APIRouter()
health_router.include_router(health.router, tags=["health"])
