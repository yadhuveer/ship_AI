import pickle
import numpy as np
import joblib

# Load the saved model
#with open("fuel_predictor.pkl", "rb") as f:
    #model = pickle.load(f)

model = joblib.load("fuel_predictor.pkl")

# Sample input values (you can change these later)
cargo = float(input("Enter cargo weight (tons): "))
distance = float(input("Enter distance (km): "))
weather = float(input("Enter weather condition (0=clear to 5=stormy): "))

# Make prediction
input_data = np.array([[cargo, distance, weather]])
predicted_fuel = model.predict(input_data)


print(f"Predicted fuel needed: {predicted_fuel[0]:.2f} units")
