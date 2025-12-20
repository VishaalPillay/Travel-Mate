from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

# Import our AI Engine
from app.ml_engine.risk_scorer import risk_engine
router = APIRouter()

# Define the Input Schema (What the App sends)
class RouteRequest(BaseModel):
    start_loc: str
    end_loc: str
    elevation_gain: int
    is_night: bool
    current_snow_level: Optional[int] = 0
    current_wind_speed: Optional[int] = 0

# Define the Output Schema (What the App receives)
class RiskResponse(BaseModel):
    risk_score: int
    status: str
    warnings: List[str]

@router.post("/predict-risk", response_model=RiskResponse)
async def predict_route_risk(request: RouteRequest):
    
    # 1. Structure the data for the AI engine
    route_info = {
        "start": request.start_loc,
        "end": request.end_loc,
        "elevation_gain": request.elevation_gain,
        "is_night_travel": request.is_night
    }
    
    weather_info = {
        "snow_level_cm": request.current_snow_level,
        "wind_speed": request.current_wind_speed
    }

    # 2. Run the AI Prediction
    prediction = risk_engine.calculate_risk(route_info, weather_info)

    return prediction