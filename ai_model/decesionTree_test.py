import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
import matplotlib.pyplot as plt

data = {
    "distance_km": [1000, 800, 1200, 1500, 700, 900, 1100, 1300],
    "wind_speed": [20, 15, 35, 10, 5, 25, 30, 40],
    "traffic_level": [5, 3, 8, 2, 1, 6, 7, 9],  # 1 (low) to 10 (high)
    "cargo_tons": [3000, 2000, 4000, 2500, 1000, 3500, 3200, 4200],
    "eta_hrs": [20, 18, 24, 28, 14, 22, 23, 26],
    "route_ok": [1, 1, 0, 1, 1, 0, 0, 0],  # 1 = Good Route, 0 = Avoid
}


df=pd.DataFrame(data)

X=df[["distance_km","wind_speed","traffic_level","cargo_tons","eta_hrs","route_ok"]]

y=df["route_ok"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)

clf = DecisionTreeClassifier()
clf.fit(X_train,y_train)

y_pred = clf.predict(X_test)


print("Accuracy:", accuracy_score(y_test, y_pred))


plt.figure(figsize=(12,6))
tree.plot_tree(clf, feature_names=X.columns, class_names=["Avoid", "Good"], filled=True)
plt.show()