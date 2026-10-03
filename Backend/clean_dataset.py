import pandas as pd
from pathlib import Path

INPUT_FILE = "data/raw/bangalore_routes.csv"
OUTPUT_FILE = "data/processed/bangalore_routes_clean.csv"

# Load raw dataset
df = pd.read_csv(INPUT_FILE)

print("Original rows:", len(df))

# Detect invalid source coordinates
bad_src = (
    (df["lat_src"] < 12) |
    (df["lat_src"] > 14) |
    (df["lon_src"] < 77) |
    (df["lon_src"] > 78)
)

# Detect invalid destination coordinates
bad_dest = (
    (df["lat_dest"] < 12) |
    (df["lat_dest"] > 14) |
    (df["lon_dest"] < 77) |
    (df["lon_dest"] > 78)
)

# A row is invalid if either endpoint is invalid
bad_rows = bad_src | bad_dest

print("Bad source rows:", bad_src.sum())
print("Bad destination rows:", bad_dest.sum())
print("Rows removed:", bad_rows.sum())

# Keep only valid rows
clean_df = df[~bad_rows].copy()

print("Clean rows:", len(clean_df))

# Create output directory
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Save cleaned dataset
clean_df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)