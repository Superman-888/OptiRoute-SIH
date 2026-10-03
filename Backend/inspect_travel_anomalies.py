import pandas as pd

FILE = "data/processed/bangalore_routes_clean.csv"

df = pd.read_csv(FILE)

# Ignore zero-distance rows because their theoretical time is zero
valid = df["distance"] > 0

df = df[valid].copy()

# Expected travel time in minutes
df["expected_time"] = (df["distance"] / df["speed"]) * 60

df["time_ratio"] = df["travel_time"] / df["expected_time"]

print("=== HIGHEST TIME RATIOS ===")

print(
    df.nlargest(20, "time_ratio")[
        [
            "source_location",
            "destination_location",
            "distance",
            "speed",
            "travel_time",
            "expected_time",
            "time_ratio",
            "signal_time",
            "is_peak",
            "weather",
            "road_capacity",
            "vehicles"
        ]
    ].to_string(index=False)
)

print("\n=== LONGEST TRAVEL TIMES ===")

print(
    df.nlargest(20, "travel_time")[
        [
            "source_location",
            "destination_location",
            "distance",
            "speed",
            "travel_time",
            "expected_time",
            "time_ratio",
            "signal_time",
            "is_peak",
            "weather",
            "road_capacity",
            "vehicles"
        ]
    ].to_string(index=False)
)