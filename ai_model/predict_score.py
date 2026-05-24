import joblib
import numpy as np
import os

import pandas as pd

scoreModelPath = os.path.join(os.path.dirname(__file__),'models/random_forest_path_scorer.pkl')
scalerModelPath = os.path.join(os.path.dirname(__file__),'models/path_input_scaler.pkl')


scalerModel = joblib.load(scalerModelPath)
scoreModel = joblib.load(scoreModelPath)


FEATURES = ['distance', 'eta', 'fuel', 'traffic', 'weather']

def predictScore(distance,eta,fuel,traffic,weather):
    #dataInputArray = np.array([[distance,eta,fuel,traffic,weather]])
    df = pd.DataFrame([{
        "distance": distance,
        "eta": eta,
        "fuel": fuel,
        "traffic": traffic,
        "weather": weather
    }])
    print("Input DF:\n", df)

    X_scaled = pd.DataFrame(scalerModel.transform(df), columns=FEATURES)

    print("Scaled Input:\n", X_scaled)

    score = scoreModel.predict(X_scaled)[0]
    print("Predicted Score:", score)
    return score

