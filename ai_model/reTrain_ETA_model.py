import random
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

ETA_COEFF = {'cargo':0.5,'distance':0.8,'weather':2.0,'traffic':3.0,'bias':5}

Speed_COEFF = {'cargo':0.3,'distance':0.2,'weather':-1.0, 'bias':25}

WEATHER_ENCODING = {
    "sunny": 0,
    "cloudy": 1,
    "windy": 2,
    "rainy": 3,
    "snowy": 4,
    "stormy": 5,
    "unknown": 1
}

TRAFFIC_ENCODING = {
    "light": 0,
    "moderate": 1,
    "heavy": 2,
    "unknown": 1
}


def encode_and_average(values, encoding_map):
    numeric = [encoding_map.get(v, encoding_map['unknown']) for v in values]
    return sum(numeric) / len(numeric)

data=[]



def RetrainETAFun(retrainDataArray):

    for _ in range(1000):
        cargo = random.uniform(5000, 200000)
        distance = random.uniform(50,1000)

        weather_list = random.choices(list(WEATHER_ENCODING.keys()), k=random.randint(1, 5))
        traffic_list = random.choices(list(TRAFFIC_ENCODING.keys()), k=len(weather_list))

        weather = encode_and_average(weather_list, WEATHER_ENCODING)
        traffic = encode_and_average(traffic_list, TRAFFIC_ENCODING)

        base_speed = 30  
        speed = base_speed - (cargo / 100000) * 5 - weather * 0.5  
        speed = max(10, speed)  

   
        eta = (distance / speed)  + traffic * 10 + weather * 5
        
        data.append([distance,weather,traffic,eta,speed])

    print("1st is completed")
    for trainData in retrainDataArray.trainData:


        data.append([trainData.distance,trainData.weatherFactor,trainData.TrafficFactor,trainData.predictedETA,trainData.speed])

    print("Second is completed")
        
    df = pd.DataFrame(data,columns=["distance","weather","traffic","ETA","Speed"])
    
    X = df[['distance','weather','traffic']] 
    Y_eta = df['ETA']
    etaModel = LinearRegression()
    etaModel.fit(X,Y_eta)

    MODEL_PATH = os.path.join(MODEL_DIR, "eta_model.pkl")

    joblib.dump(etaModel,MODEL_PATH)

    return "ETA model has been sucessfully retrained"
