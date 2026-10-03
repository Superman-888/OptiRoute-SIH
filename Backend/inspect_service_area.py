import pandas as pd

FILE = "data/processed/bangalore_routes_clean.csv"

df = pd.read_csv(FILE)

# Candidate Bengaluru-area envelope for investigation only.
# This is NOT being used to delete data.
MIN_LAT = 12.8
MAX_LAT = 13.2
MIN_LON = 77.4
MAX_LON = 77.8

outside_src = (
    (df["lat_src"] < MIN_LAT) |
    (df["lat_src"] > MAX_LAT) |
    (df["lon_src"] < MIN_LON) |
    (df["lon_src"] > MAX_LON)
)

outside_dest = (
    (df["lat_dest"] < MIN_LAT) |
    (df["lat_dest"] > MAX_LAT) |
    (df["lon_dest"] < MIN_LON) |
    (df["lon_dest"] > MAX_LON)
)

print("=== CANDIDATE SERVICE AREA CHECK ===")

print("Rows with source outside:", outside_src.sum())
print("Rows with destination outside:", outside_dest.sum())
print(
    "Rows with either endpoint outside:",
    (outside_src | outside_dest).sum()
)

print("\n=== UNIQUE SOURCE LOCATIONS OUTSIDE ===")

print(
    df.loc[
        outside_src,
        ["source_location", "lat_src", "lon_src"]
    ]
    .drop_duplicates()
    .sort_values("source_location")
    .to_string(index=False)
)

print("\n=== UNIQUE DESTINATION LOCATIONS OUTSIDE ===")

print(
    df.loc[
        outside_dest,
        ["destination_location", "lat_dest", "lon_dest"]
    ]
    .drop_duplicates()
    .sort_values("destination_location")
    .to_string(index=False)
)