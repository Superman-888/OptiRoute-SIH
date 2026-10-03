import math
from app.ml.predict import model, FEATURES
import pandas as pd

def predict_bulk(data_list):
    if not data_list or model is None:
        return [0.0] * len(data_list)
        
    df = pd.DataFrame(data_list)
    df["day_of_week"] = df["day_of_week"].astype("category")
    df["weather"] = df["weather"].astype("category")
    df = df[FEATURES]
    
    predictions = model.predict(df)
    return [float(p) for p in predictions]

def build_travel_time_matrix(locations, distance_matrix, traffic_context):
    n = len(locations)
    data_list = []
    indices = []
    
    # 1. Collect all valid pairs
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            distance_meters = distance_matrix[i][j]
            if distance_meters == float("inf"):
                continue
                
            data = {
                "lat_src": locations[i]["latitude"],
                "lon_src": locations[i]["longitude"],
                "lat_dest": locations[j]["latitude"],
                "lon_dest": locations[j]["longitude"],
                "distance": distance_meters / 1000.0,
                "day_of_week": traffic_context["day_of_week"],
                "hour": traffic_context["hour"],
                "is_peak": traffic_context["is_peak"],
                "weather": traffic_context["weather"],
                "road_capacity": traffic_context["road_capacity"],
                "vehicles": traffic_context["vehicles"],
                "speed": traffic_context["speed"],
                "signal_time": traffic_context["signal_time"]
            }
            data_list.append(data)
            indices.append((i, j))
            
    # 2. Bulk predict
    predictions = predict_bulk(data_list)
    
    # 3. Reconstruct matrix
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for idx, (i, j) in enumerate(indices):
        matrix[i][j] = predictions[idx]
        
    for i in range(n):
        for j in range(n):
            if i != j and distance_matrix[i][j] == float("inf"):
                matrix[i][j] = float("inf")
                
    import numpy as np
    return np.array(matrix)

def build_traffic_cost_matrix(locations, distance_matrix, traffic_context):
    # Same bulk pattern for traffic cost
    n = len(locations)
    data_list = []
    indices = []
    
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            distance_meters = distance_matrix[i][j]
            if distance_meters == float("inf"):
                continue
                
            data = {
                "lat_src": locations[i]["latitude"],
                "lon_src": locations[i]["longitude"],
                "lat_dest": locations[j]["latitude"],
                "lon_dest": locations[j]["longitude"],
                "distance": distance_meters / 1000.0,
                "day_of_week": traffic_context["day_of_week"],
                "hour": traffic_context["hour"],
                "is_peak": traffic_context["is_peak"],
                "weather": traffic_context["weather"],
                "road_capacity": traffic_context["road_capacity"],
                "vehicles": traffic_context["vehicles"],
                "speed": traffic_context["speed"],
                "signal_time": traffic_context["signal_time"]
            }
            data_list.append(data)
            indices.append((i, j))
            
    predictions = predict_bulk(data_list)
    
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for idx, (i, j) in enumerate(indices):
        expected_time = (distance_matrix[i][j] / 1000.0) / traffic_context["speed"] * 60
        matrix[i][j] = max(0.0, predictions[idx] - expected_time)
        
    for i in range(n):
        for j in range(n):
            if i != j and distance_matrix[i][j] == float("inf"):
                matrix[i][j] = float("inf")
                
    import numpy as np
    return np.array(matrix)

from app.ml.predict import get_model_metrics

def get_traffic_model_metrics():
    return get_model_metrics()

def get_predicted_travel_time(data):
    """
    Restore single prediction method for /traffic endpoint
    """
    res = predict_bulk([data])
    return res[0]
