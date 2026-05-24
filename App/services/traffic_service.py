import os, httpx, asyncio

from dotenv import load_dotenv

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

BASEURL = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic"

TIMEOUT = 8.0

def mock_duration_to_traffic(duration, typical):
    if duration > typical * 1.2:
        return "heavy"
    elif duration > typical * 1.05:
        return "moderate"
    else:
        return "light"





async def getTraffic(lat,lon,client):

    dest_lat = lat + 10
    dest_lon = lon + 10  

    coords = f"{lon},{lat};{dest_lon},{dest_lat}"

    
    url =  f"https://api.mapbox.com/directions/v5/mapbox/driving-traffic/{coords}"
   
    params={
        "alternatives": "false",
        "geometries": "geojson",
        "overview": "full",
        "steps": "true",
        "access_token": MAPBOX_API_KEY
        }

    try:
        trafficResponse = await client.get(url,params=params,timeout=TIMEOUT)
        trafficResponse.raise_for_status()
        data = trafficResponse.json()
        #print(data)
        results = data.get("routes",[])

        if not results:
            return "unknown"
        

        duration = results[0].get("duration", 0)  
        duration_typical = results[0].get("duration_typical", duration)

        return mock_duration_to_traffic(duration, duration_typical)
        

        

    except httpx.RequestError as e:
        print(f"Network error: {e}")
        return "Error"
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        return "Error"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error"










async def get_traffic_for_path(path_ids,meta_by_id):

    async with httpx.AsyncClient() as client:
        tasks = [getTraffic(meta_by_id[p]['lat'],meta_by_id[p]['lon'],client)  for p in path_ids]
        return await asyncio.gather(*tasks)
