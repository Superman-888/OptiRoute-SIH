from predict import predict_travel_time


sample_route = {
    "lat_src": 12.9716,
    "lon_src": 77.5946,
    "lat_dest": 12.9352,
    "lon_dest": 77.6245,
    "distance": 5.5,
    "day_of_week": "Monday",
    "hour": 18,
    "is_peak": 1,
    "weather": "Clear",
    "road_capacity": 1500,
    "vehicles": 500,
    "speed": 25.0,
    "signal_time": 60
}


prediction = predict_travel_time(sample_route)

print("Predicted travel time:", prediction)