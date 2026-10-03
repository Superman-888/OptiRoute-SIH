from pydantic import BaseModel
from typing import List


class Depot(BaseModel):
    latitude: float
    longitude: float


class Customer(BaseModel):
    node_id: int
    latitude: float
    longitude: float
    demand: float
    earliest: float
    latest: float
    service_time: float


class Vehicle(BaseModel):
    vehicle_id: int
    capacity: float


class OptimizationRequest(BaseModel):
    depot: Depot
    customers: List[Customer]
    vehicles: List[Vehicle]