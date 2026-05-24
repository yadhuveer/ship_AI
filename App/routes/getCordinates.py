import requests
from fastapi import HTTPException

OPENCAGE_API_KEY = "d6b830a8975d4d589069e3efd3e4fb45"  # Replace with your actual API key

def get_coordinates(city_name: str):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch coordinates")

    data = response.json()
    if not data['results']:
        raise HTTPException(status_code=400, detail=f"Invalid city name: {city_name}")

    lat = data['results'][0]['geometry']['lat']
    lon = data['results'][0]['geometry']['lng']
    return {"lat": lat, "lon": lon}
