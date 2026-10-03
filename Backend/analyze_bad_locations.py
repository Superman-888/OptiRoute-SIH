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

print("=== BAD SOURCE LOCATION FREQUENCY ===")
print(
    df.loc[bad_src, "source_location"]
    .value_counts()
    .to_string()
)

print("\n=== BAD DESTINATION LOCATION FREQUENCY ===")
print(
    df.loc[bad_dest, "destination_location"]
    .value_counts()
    .to_string()
)

print("\n=== TOTAL AFFECTED ROWS ===")
print("Bad source rows:", bad_src.sum())
print("Bad destination rows:", bad_dest.sum())

both_bad = bad_src & bad_dest
print("Both source and destination bad:", both_bad.sum())