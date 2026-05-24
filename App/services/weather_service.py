# App/services/weather_service.py
import os, httpx, asyncio
from dotenv import load_dotenv

load_dotenv()

OWM_KEY    = os.getenv("OWM_API_KEY")
BASE_URL   = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT    = 8.0  # seconds
# Map OpenWeather "main" field to your 5 categories
WX_MAP = {
    "Clear":  "sunny",
    "Clouds": "cloudy",
    "Drizzle":"rainy",
    "Rain":   "rainy",
    "Thunderstorm": "stormy",
    "Snow":   "snowy",
    "Mist":   "windy",
    "Fog":    "windy",
    "Haze":   "windy"
}

async def fetch_weather(lat: float, lon: float, client: httpx.AsyncClient) -> str:
    """Return one of ['sunny','cloudy','rainy','stormy','windy','snowy']"""
    params = {"lat": lat, "lon": lon, "appid": OWM_KEY}
    try:
        r = await client.get(BASE_URL, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        wx_main = r.json()["weather"][0]["main"]  
        #print(r.json())         # e.g. 'Clear'
        return WX_MAP.get(wx_main, "unknown")
    except Exception as exc:
        # Fail‑soft: treat as unknown so ML can penalise if desired
        return "unknown"

async def get_weather_for_path(path_ids: list[str], meta_by_id: dict) -> list[str]:
    """Parallel‑fetch weather for each port in the path."""
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_weather(meta_by_id[p]["lat"], meta_by_id[p]["lon"], client)
            for p in path_ids
        ]
        
        return await asyncio.gather(*tasks)
