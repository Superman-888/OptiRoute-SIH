from fastapi import APIRouter

from app.schemas.routing import RouteRequest
from app.services.routing_service import get_route

router = APIRouter()


@router.post("/routing")
def route(request: RouteRequest):
    return get_route(request)