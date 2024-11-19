from fastapi import APIRouter, HTTPException
from ..services.data_collector import TrafficDataCollector
from ..services.predictor import TrafficPredictor
from ..models.traffic_data import PredictionRequest
from ..config import settings

router = APIRouter()
data_collector = TrafficDataCollector()
predictor = TrafficPredictor()


@router.get("/traffic/incidents/{city}")
async def get_traffic_incidents(city: str):
    """Get traffic incidents for a specific city"""
    city_info = next(
        (c for c in settings.MONITORED_CITIES if c["name"].lower() == city.lower()),
        None,
    )
    if not city_info:
        raise HTTPException(status_code=404, detail="City not found")

    incidents = await data_collector.get_traffic_incidents(
        city_info["latitude"], city_info["longitude"]
    )
    return {"incidents": incidents}


@router.get("/traffic/flow/{city}")
async def get_traffic_flow(city: str):
    """Get traffic flow data for a specific city"""
    city_info = next(
        (c for c in settings.MONITORED_CITIES if c["name"].lower() == city.lower()),
        None,
    )
    if not city_info:
        raise HTTPException(status_code=404, detail="City not found")

    flow_data = await data_collector.get_traffic_flow(
        city_info["latitude"], city_info["longitude"]
    )
    return {"flow_data": flow_data}


@router.post("/traffic/predict")
async def predict_traffic(request: PredictionRequest):
    """Predict traffic conditions for a specific location and time"""
    prediction = predictor.predict(request.latitude, request.longitude, request.time)
    return {"prediction": prediction}
