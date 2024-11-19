from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class TrafficIncident(BaseModel):
    id: str
    type: str
    severity: int
    start_time: datetime
    end_time: Optional[datetime]
    latitude: float
    longitude: float
    description: str


class TrafficFlow(BaseModel):
    latitude: float
    longitude: float
    speed: float
    jam_factor: float
    timestamp: datetime


class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    time: str
