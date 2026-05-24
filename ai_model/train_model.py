import random
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Constants for hidden fuel formula
a, b, c, d = 2, 3, 1, 5

# Generate dummy training data
data = []
for _ in range(100):
    cargo = random.randint(1, 10)
    distance = random.randint(10, 100)
    weather = random.randint(0, 5)
    fuel = a * cargo + b * distance + c * weather + d
    data.append([cargo, distance, weather, fuel])


df = pd.DataFrame(data, columns=['cargo', 'distance', 'weather', 'fuel'])

# Train the model
X = df[['cargo', 'distance', 'weather']]
y = df['fuel']
model = LinearRegression()
model.fit(X, y)

# Save the model to disk
joblib.dump(model, 'fuel_predictor.pkl')

print("✅ Model trained and saved as fuel_predictor.pkl")
