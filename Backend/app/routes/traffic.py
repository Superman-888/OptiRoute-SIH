from fastapi import APIRouter

from app.schemas.traffic import TrafficRequest
from app.services.traffic_service import get_predicted_travel_time, get_traffic_model_metrics


router = APIRouter()


@router.post("/traffic")
def predict_traffic(data: TrafficRequest):
    predicted_time = get_predicted_travel_time(
        data.model_dump()
    )

    return {
        "predicted_travel_time": predicted_time
    }
@router.get("/traffic/metrics")
def traffic_metrics():
    metrics = get_traffic_model_metrics()
    if metrics:
        return {"status": "success", "metrics": metrics}
    return {"status": "error", "message": "ML model not loaded."}
