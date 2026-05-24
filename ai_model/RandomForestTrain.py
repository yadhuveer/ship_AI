import pandas as pd
import networkx as nx
import random
import joblib
from tqdm import tqdm
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from itertools import islice

from predict_fuel import predict_fuel
from predict_ETA_Speed import predictEta

eta_model = joblib.load("models/eta_model.pkl")
fuel_model = joblib.load("fuel_predictor.pkl")


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
print(DATA_DIR)

df= pd.read_csv(DATA_DIR/"connections_50.csv")
G= nx.Graph()


for _, row in df.iterrows():
    G.add_edge(row['from_port_id'],row['to_port_id'],weight=row['distance_km'])
    G.add_edge(row['to_port_id'],row['from_port_id'],weight=row['distance_km'])



TRAFFIC_ENCODING ={"light":0, "moderate":1, "heavy":2}
WEATHER_ENCODING ={"sunny":0, "cloudy":1, "windy":2, "rainy":3, "snowy":4, "stormy":5}


def get_top_k_paths(G,source,target,k=5):
    try:
        return list(islice(nx.shortest_simple_paths(G, source, target, weight='weight'), k))
       # return list(nx.shortest_simple_paths(G,source,target,weight='weight'))[:k]
    
    except Exception as e:

        print("err "+str(e))
        return []

def compute_path_features(path):
    total_distance = 0
    weather_vals = []

    traffic_vals = []

    for i in range(len(path)-1):
        edge_data = G.get_edge_data(path[i],path[i+1])
        total_distance+= edge_data['weight']

        weather_vals.append(random.choice(list(WEATHER_ENCODING.values())))
        traffic_vals.append(random.choice(list(TRAFFIC_ENCODING.values())))

    weather = sum(weather_vals)/len(weather_vals)
    traffic = sum(traffic_vals)/len(traffic_vals)
    
    cargo = random.uniform(1000,400000)
    eta = predictEta(cargo,total_distance,weather,traffic)[0]
    fuel= predict_fuel(cargo,total_distance,weather)[0]

    return total_distance, eta, fuel, traffic, weather


def compute_score(d,e,f,t,w):
    score = 20000  # Increased base score

    score -= 0.02 * d
    score -= 0.05 * e
    score -= 0.01 * f
    score -= 10.0 * t
    score -= 20.0 * w

    
    return max(0, min(20000, score))
    


all_ports = list(G.nodes())
data=[]


for _ in tqdm(range(1000), desc="Generating training data"):
    src,dst = random.sample(all_ports,2)
    #print("src port is "+src)
    #print("Dest port is "+dst)
    paths = get_top_k_paths(G,src,dst,k=5)
    #print(paths)
    for path in paths:
        d,e,f,t,w = compute_path_features(path)
        s=compute_score(d,e,f,t,w)
        data.append([d,e,f,t,w,s])

#df_data = pd.DataFrame(data,)

df= pd.DataFrame(data, columns=['distance','eta','fuel','traffic','weather','score'])

X=df[["distance","eta","fuel","traffic","weather"]]
y=df["score"]


scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)


X_train,X_test,y_train,y_test = train_test_split(X_scaled,y,test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100,random_state=42)
model.fit(X_train,y_train)


joblib.dump(model,"models/random_forest_path_scorer.pkl")
joblib.dump(scaler, "models/path_input_scaler.pkl")

print(scaler.data_min_)
print(scaler.data_max_)


print("describe")
print(df["score"].describe())
