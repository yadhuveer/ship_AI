from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from typing import List, Optional

from fastapi.responses import JSONResponse

import networkx as nx
import csv
from pathlib import Path
from typing import List, Dict
from App.services.weather_service import get_weather_for_path

from App.services.traffic_service import get_traffic_for_path
from App.routes.weatherAndTrafficEncode import weatherEncode,trafficEncode
import asyncio



from ai_model.predict_fuel import predict_fuel
from ai_model.predict_ETA_Speed import predictEta
from ai_model.predict_ETA_Speed import predictSpeed

from ai_model.predict_score import predictScore

from ai_model.reTrain_ETA_model import RetrainETAFun
from ai_model.retrain_Fuel_model import RetrainFuelFun
from App.utils.cache import set_cache, get_cache

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PORTS_CSV = DATA_DIR / "ports_50.csv"
EDGES_CSV = DATA_DIR / "connections_50.csv"

K_PATHS   = 5


router = APIRouter()
graph = nx.Graph()         
port_id_to_meta = {}

def load_graph() -> None:
    if not PORTS_CSV.exists() or not EDGES_CSV.exists():
        raise RuntimeError("Port/edge CSV files not found in 'data/' directory")

   
    with PORTS_CSV.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            port_id = row["port_id"]
            port_id_to_meta[port_id] = {
                "name": row["port_name"],
                "country": row["country"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
            }
            graph.add_node(port_id)

   
    with EDGES_CSV.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            a, b, d_km = row["from_port_id"], row["to_port_id"], float(row["distance_km"])
            # add UN-directed edge (both ways) so routes can flow either direction
            graph.add_edge(a, b, weight=d_km)
            graph.add_edge(b, a, weight=d_km)

try:
    load_graph()
except Exception as e:
    # Fail fast if graph can't be built
    raise RuntimeError(f"Failed to initialise port graph: {e}") from e



class VoyageInput(BaseModel):
    cargo:float
   
    origin_id: str
    destination_id: str

class RetrainInput(BaseModel):
    cargo: Optional[float] = None
    distance: Optional[float] = None
    weatherFactor: Optional[float] = None
    speed: Optional[float] = None
    TrafficFactor: Optional[float] = None
    predictedETA: Optional[float] = None   
    predictedFuel: Optional[float] = None

    model_config = {
        "extra": "allow"   
    } 


class RetrainArrayInput(BaseModel):
    trainData: List[RetrainInput]

@router.post("/plan-voyage")
def plan_voyage(data: VoyageInput):
    origin = data.origin_id
    dest   = data.destination_id

    # 1) quick validation
    if origin not in port_id_to_meta or dest not in port_id_to_meta:
        raise HTTPException(status_code=400, detail="Invalid origin or destination port_id")

    try:
        # 2) generate up to K shortest paths (Yen's algorithm via NetworkX)
        cache_key = f"paths:{origin}:{dest}"
        k_paths = get_cache(cache_key)

        if not k_paths:
            all_paths = nx.shortest_simple_paths(graph, origin, dest, weight="weight")
            k_paths: List[List[str]] = []
            for i, path in enumerate(all_paths):
                if i >= K_PATHS:
                    break
                k_paths.append(path)
            set_cache(cache_key, k_paths, ttl=3600)

        # 3) build response with distances
        response_paths = []
        for path in k_paths:
            total_dist = sum(
                graph[path[idx]][path[idx+1]]["weight"] for idx in range(len(path)-1)
                
            )

            # --- fetch live weather for this path (async) ---
            weather_seq = asyncio.run(get_weather_for_path(path, port_id_to_meta))
            #weather_score_seq = [WEATHER_TO_SCORE[w] for w in weather_seq]   # if you need numeric

            traffic_Data = asyncio.run(get_traffic_for_path(path,port_id_to_meta))

            weather_num = weatherEncode(weather_seq)
            traffic_nuam = trafficEncode(traffic_Data)

            ETA = predictEta(data.cargo,total_dist,weather_num,traffic_nuam)
            Speed =total_dist/ETA
            Fuel =  predict_fuel(data.cargo,total_dist,weather_num)
            Score = predictScore(total_dist,ETA[0],Fuel[0],traffic_nuam,weather_num)
            response_paths.append({
                "path_ids"  : path,
                "path_names": [
                    f"{port_id_to_meta[p]['name']} ({p})" for p in path
                ],
                "distance_km": total_dist,
                "weather": weather_seq,
                "traffic":traffic_Data,
                "weatherNum":weather_num,
                "trafficNum":traffic_nuam,
                "ETA":ETA[0],
                "Speed":Speed[0],
                "Fuel":Fuel[0],
                "score":Score

            })

        maxScore=response_paths[0]["score"]
        reqPath=response_paths[0]
        for p in response_paths:
            if(p["score"]> maxScore):
                maxScore=p["score"]
                reqPath=p

        
        
        #reqPath = ""
        #for k in portPath["path_names"]:
            #reqPath+=k+"-->"


        


        return {
            "origin": port_id_to_meta[origin]["name"],
            "destination": port_id_to_meta[dest]["name"],
            "cargo":data.cargo,
            "originPort":origin,
            "destinationPort":dest,
            "k_paths": response_paths,
            "reqPath": reqPath
            
            # → NEXT STEP: add weather, traffic, fuel, eta, speed, RF score
        
        }

    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No route found between these ports")
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/retrainData")
def retrainEtaFuel(trainData:RetrainArrayInput):
    try:
        print(trainData)
        result1 = RetrainETAFun(trainData)
        result2 = RetrainFuelFun(trainData)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "etaResult": result1,
                "fuelResult": result2
            }
        )


    except  Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
