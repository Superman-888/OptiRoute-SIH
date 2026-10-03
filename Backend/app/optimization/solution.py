from dataclasses import dataclass
from typing import List


@dataclass
class VehicleRoute:
    vehicle_id: int
    customers: List[int]


@dataclass
class VRPSolution:
    routes: List[VehicleRoute]
    total_distance: float
    total_time: float
    total_traffic_cost: float
    penalty: float
    fitness: float