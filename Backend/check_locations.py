import pandas as pd

df = pd.read_csv("data/raw/bangalore_routes.csv")

names = [
    "Shanthi Pura",
    "Bidrahalli",
    "Richard's Park",
    "Singanahalli",
    "lal bagh",
    "Jaya Chamarajendra Nagar",
    "Ragavendra Nagar",
    "Ananth Nagar",
    "Vijaypura",
    "Jagajeevanram Nagar",
    "Kunigal Road"
]

print("=== SOURCE COORDINATES ===")

source = df[
    df["source_location"].isin(names)
][
    ["source_location", "lat_src", "lon_src"]
].drop_duplicates().sort_values("source_location")

print(source.to_string(index=False))

print("\n=== DESTINATION COORDINATES ===")

destination = df[
    df["destination_location"].isin(names)
][
    ["destination_location", "lat_dest", "lon_dest"]
].drop_duplicates().sort_values("destination_location")

print(destination.to_string(index=False))