import pandas as pd

FILE = "data/processed/bangalore_routes_clean.csv"

df = pd.read_csv(FILE)

zero = df[df["distance"] <= 0]

print("=== ZERO DISTANCE ROWS ===")
print(
    zero[
        [
            "source_location",
            "destination_location",
            "lat_src",
            "lon_src",
            "lat_dest",
            "lon_dest",
            "distance",
            "travel_time"
        ]
    ].to_string(index=False)
)