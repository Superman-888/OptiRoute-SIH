import requests
import json
import logging

def get_route(source, destination):
    return {
        "source": source,
        "destination": destination,
        "message": "Routing service is working"
    }

def build_road_graph(latitude, longitude, distance=5000):
    # Mock function since OSRM does not require a pre-downloaded graph
    return {"status": "OSRM bypassed graph"}

def get_nearest_node(graph, latitude, longitude):
    pass

def build_distance_matrix(graph, locations):
    if not locations:
        return []
        
    coords = ";".join([f"{loc["longitude"]},{loc["latitude"]}" for loc in locations])
    url = f"http://router.project-osrm.org/table/v1/driving/{coords}?annotations=distance"
    
    try:
        res = requests.get(url, timeout=3.0)
        data = res.json()
        if data.get("code") == "Ok":
            import numpy as np
            return np.array(data["distances"])
    except Exception as e:
        logging.error(f"OSRM distance matrix error: {e}")
        
    # Fallback to Haversine if OSRM fails
    import math
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000 # Radius of earth in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c * 1.3 # 1.3 road winding factor
        
    matrix = []
    for src in locations:
        row = []
        for dst in locations:
            row.append(haversine(src["latitude"], src["longitude"], dst["latitude"], dst["longitude"]))
        matrix.append(row)
    import numpy as np
    return np.array(matrix)

def build_route_geometry(graph, locations, route):
    if not route:
        return []
        
    node_sequence = [0] + [c + 1 for c in route] + [0]
    
    coords = ";".join([f"{locations[i]["longitude"]},{locations[i]["latitude"]}" for i in node_sequence])
    url = f"http://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson"
    
    try:
        res = requests.get(url, timeout=3.0)
        data = res.json()
        if data.get("code") == "Ok":
            coordinates = data["routes"][0]["geometry"]["coordinates"]
            # OSRM returns [lon, lat], Leaflet wants [lat, lon]
            return [[lat, lon] for lon, lat in coordinates]
    except Exception as e:
        logging.error(f"OSRM route geometry error: {e}")
        
    # Fallback straight lines
    path = []
    for i in node_sequence:
        path.append([locations[i]["latitude"], locations[i]["longitude"]])
    return path
