from ai_model.predict_eta import predict_eta
from ai_model.predict_speed import predict_speed
from ai_model.predict_fuel import predict_fuel

@app.post("/plan-voyage")
def plan_voyage(data: VoyageInput):
    try:
        fuel = predict_fuel(data.cargo, data.distance, data.weather)
        eta = predict_eta(data.cargo, data.distance, data.weather)
        speed = predict_speed(data.cargo, data.distance, data.weather)
        return {
            "eta": f"{eta:.1f} hours",
            "speed_schedule": f"{speed:.1f} knots",
            "expected_fuel_use": f"{fuel:.1f} liters"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
