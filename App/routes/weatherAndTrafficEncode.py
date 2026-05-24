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

def weatherEncode(weatherArray):
    weatherData = [WEATHER_ENCODING.get(w,WEATHER_ENCODING["unknown"]) for w in weatherArray]
    return sum(weatherData)/len(weatherData)

def trafficEncode(trafficArray):
    trafficData = [TRAFFIC_ENCODING.get(t,TRAFFIC_ENCODING["unknown"]) for t in trafficArray]
    return sum(trafficData)/len(trafficData)