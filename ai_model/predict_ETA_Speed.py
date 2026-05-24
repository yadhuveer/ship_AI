import joblib
import numpy as np
import os

etaModelPath = os.path.join(os.path.dirname(__file__),'models/eta_model.pkl')

speedModelPath = os.path.join(os.path.dirname(__file__),'models/speed_model.pkl')

etaModel = joblib.load(etaModelPath)
speedModel = joblib.load(speedModelPath)


def predictEta(cargo,distance,weather,traffic):
    etaInputArray = np.array([[distance,weather,traffic]])

    predictedETA = etaModel.predict(etaInputArray)
    return predictedETA

def predictSpeed(cargo,distance,weather):
    speedInputArray = np.array([[cargo,distance,weather]])

    predictedSpeed = speedModel.predict(speedInputArray)
    return predictedSpeed


