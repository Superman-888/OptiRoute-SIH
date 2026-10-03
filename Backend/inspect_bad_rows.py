import pandas as pd

df = pd.read_csv("data/raw/bangalore_routes.csv")

bad_src = (
    (df["lat_src"] < 12) |
    (df["lat_src"] > 14) |
    (df["lon_src"] < 77) |
    (df["lon_src"] > 78)
)

bad_dest = (
    (df["lat_dest"] < 12) |
    (df["lat_dest"] > 14) |
    (df["lon_dest"] < 77) |
    (df["lon_dest"] > 78)
)

bad = df[bad_src | bad_dest]

print("=== BAD ROW SAMPLE ===")
print(
    bad[
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
    ].head(30).to_string(index=False)
)

print("\n=== DISTANCE STATISTICS ===")
print(
    bad["distance"].describe().to_string()
)

print("\n=== TRAVEL TIME STATISTICS ===")
print(
    bad["travel_time"].describe().to_string()
)