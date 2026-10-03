from pydantic import BaseModel


class RouteRequest(BaseModel):
    source: int
    destination: int