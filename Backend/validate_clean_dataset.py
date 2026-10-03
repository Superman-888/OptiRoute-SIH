import pandas as pd

FILE = "data/processed/bangalore_routes_clean.csv"

df = pd.read_csv(FILE)

print("=== BASIC INFO ===")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n=== MISSING VALUES ===")
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.any() else "No missing values")

print("\n=== DUPLICATE ROWS ===")
print("Duplicate rows:", df.duplicated().sum())

print("\n=== COORDINATE CHECK ===")

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

print("Invalid source coordinates:", bad_src.sum())
print("Invalid destination coordinates:", bad_dest.sum())

print("\n=== DISTANCE CHECK ===")
print("Zero/negative distance:", (df["distance"] <= 0).sum())
print("Minimum distance:", df["distance"].min())
print("Maximum distance:", df["distance"].max())

print("\n=== TRAVEL TIME CHECK ===")
print("Zero/negative travel time:", (df["travel_time"] <= 0).sum())
print("Minimum travel time:", df["travel_time"].min())
print("Maximum travel time:", df["travel_time"].max())

print("\n=== DATA TYPES ===")
print(df.dtypes.to_string())