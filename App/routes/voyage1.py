from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from ai_model.predict_fuel import predict_fuel
from ai_model.predict_ETA_Speed import predictEta
from ai_model.predict_ETA_Speed import predictSpeed

#from getCordinates import get_coordinates





from App.routes.getCordinates import get_coordinates

from App.routes.getDistance import haversine_distance
#from getDistance import haversine_distance


router = APIRouter()

class VoyageInput(BaseModel):
    cargo:float
    weather: float
    origin: str
    destination: str


@router.post("/plan-voyage")
def plan_voyage(data:VoyageInput):
    try:
        originObj= get_coordinates(data.origin)
        destObj= get_coordinates(data.destination)
        
        originLat = originObj["lat"]
        originLon = originObj["lon"]

        destLat = destObj["lat"]
        destLon = destObj["lon"]
        
        distance = haversine_distance(originLat,originLon,destLat,destLon) 
        
        print(distance)
    
        fuel=predict_fuel(data.cargo,distance,data.weather)
        eta= predictEta(data.cargo,distance,data.weather)
        speed = predictSpeed(data.cargo, distance, data.weather)
        return{
        "eta": f"{eta[0]:1f} hours",
        "speed_schedule" : f"{speed[0]:1f} knots",
        "expected_fuel_use":f"{fuel[0]:.1f} liters"
         }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))