from pydantic import BaseModel


class TrafficRequest(BaseModel):
    lat_src: float
    lon_src: float
    lat_dest: float
    lon_dest: float
    distance: float
    day_of_week: str
    hour: int
    is_peak: int
    weather: str
    road_capacity: int
    vehicles: int
    speed: float
    signal_time: int