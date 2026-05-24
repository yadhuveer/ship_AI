import random
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data = []


def RetrainFuelFun(retrainFuelData):
    a, b, c, d = 2, 3, 1, 5

    for _ in range(100):
        cargo = random.randint(1, 10)
        distance = random.randint(10, 100)
        weather = random.randint(0, 5)
        fuel = a * cargo + b * distance + c * weather + d
        
        data.append([cargo, distance, weather, fuel])

    for trainData in retrainFuelData.trainData:
        data.append([trainData.cargo,trainData.distance,trainData.weatherFactor,trainData.predictedFuel])

    df = pd.DataFrame(data, columns=['cargo', 'distance', 'weather', 'fuel'])

    X = df[['cargo', 'distance', 'weather']]
    y = df['fuel']

    model = LinearRegression()
    model.fit(X, y)

    MODEL_PATH = os.path.join(BASE_DIR, "fuel_predictor.pkl")

    
    joblib.dump(model, MODEL_PATH)
    
    print("✅ Model trained and saved as fuel_predictor.pkl")
    return "Fuel model has been sucessfully retrained"

    

