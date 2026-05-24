import joblib
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__),'fuel_predictor.pkl')

model = joblib.load(model_path)

def predict_fuel(cargo,distance,weather):
    dataInputArray = np.array([[cargo,distance,weather]])

    predictedFuel = model.predict(dataInputArray)

    return predictedFuel


