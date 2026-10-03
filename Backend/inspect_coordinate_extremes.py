import pandas as pd

FILE = "data/processed/bangalore_routes_clean.csv"

df = pd.read_csv(FILE)

print("=== SOURCE COORDINATE EXTREMES ===")

print("\nLowest source latitude:")
print(
    df.nsmallest(10, "lat_src")[
        ["source_location", "lat_src", "lon_src"]
    ].to_string(index=False)
)

print("\nHighest source latitude:")
print(
    df.nlargest(10, "lat_src")[
        ["source_location", "lat_src", "lon_src"]
    ].to_string(index=False)
)

print("\nLowest source longitude:")
print(
    df.nsmallest(10, "lon_src")[
        ["source_location", "lat_src", "lon_src"]
    ].to_string(index=False)
)

print("\nHighest source longitude:")
print(
    df.nlargest(10, "lon_src")[
        ["source_location", "lat_src", "lon_src"]
    ].to_string(index=False)
)

print("\n=== DESTINATION COORDINATE EXTREMES ===")

print("\nLowest destination latitude:")
print(
    df.nsmallest(10, "lat_dest")[
        ["destination_location", "lat_dest", "lon_dest"]
    ].to_string(index=False)
)

print("\nHighest destination latitude:")
print(
    df.nlargest(10, "lat_dest")[
        ["destination_location", "lat_dest", "lon_dest"]
    ].to_string(index=False)
)

print("\nLowest destination longitude:")
print(
    df.nsmallest(10, "lon_dest")[
        ["destination_location", "lat_dest", "lon_dest"]
    ].to_string(index=False)
)

print("\nHighest destination longitude:")
print(
    df.nlargest(10, "lon_dest")[
        ["destination_location", "lat_dest", "lon_dest"]
    ].to_string(index=False)
)