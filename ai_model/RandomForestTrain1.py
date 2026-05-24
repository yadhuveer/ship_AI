import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib

import random



def compute_score(d,e,f,t,w):
   
    score=100
    score-=0.001 *d     # smaller weight
    score-=0.1 *e       # smaller weight
    score-=0.0002 *f    # smaller weight
    score-= 1*t
    score-= 1 *w
    return max(0,min(100,score))
    


data=[]


for _ in range(1000):
    d=random.uniform(8000,9000)  # match real distances
    e=random.uniform(380,390)    # match ETA
    f=random.uniform(32000,33000)  # match fuel
    t=random.uniform(0,1)        # already normalized trafficNum
    w=random.uniform(0,1)        # already normalized weatherNum

    #d=random.uniform(1000,1500)
    #e=random.uniform(60,90)
    #f=random.uniform(8500,11000)
    #t=random.randint(0,3)
    #w=random.randint(0,3)
    s=compute_score(d,e,f,t,w)
    data.append([d,e,f,t,w,s])





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
