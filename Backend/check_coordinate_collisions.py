import pandas as pd

FILE = "data/processed/bangalore_routes_clean.csv"

df = pd.read_csv(FILE)

print("=== SOURCE COORDINATE COLLISIONS ===")

source_collisions = (
    df.groupby(["lat_src", "lon_src"])["source_location"]
    .nunique()
)

source_collisions = source_collisions[source_collisions > 1]

print("Coordinate pairs used by multiple source names:", len(source_collisions))

if len(source_collisions) > 0:
    for lat, lon in source_collisions.index:
        names = df[
            (df["lat_src"] == lat) &
            (df["lon_src"] == lon)
        ]["source_location"].unique()

        print(f"\n({lat}, {lon})")
        print(names)


print("\n=== DESTINATION COORDINATE COLLISIONS ===")

destination_collisions = (
    df.groupby(["lat_dest", "lon_dest"])["destination_location"]
    .nunique()
)

destination_collisions = destination_collisions[destination_collisions > 1]

print(
    "Coordinate pairs used by multiple destination names:",
    len(destination_collisions)
)

if len(destination_collisions) > 0:
    for lat, lon in destination_collisions.index:
        names = df[
            (df["lat_dest"] == lat) &
            (df["lon_dest"] == lon)
        ]["destination_location"].unique()

        print(f"\n({lat}, {lon})")
        print(names)