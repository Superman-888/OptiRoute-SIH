import pandas as pd

FILE = "data/processed/bangalore_routes_clean.csv"

df = pd.read_csv(FILE)

# Expected travel time in minutes
df["expected_time"] = (df["distance"] / df["speed"]) * 60

# Difference between recorded and theoretical time
df["time_difference"] = (
    df["travel_time"] - df["expected_time"]
)

df["time_ratio"] = (
    df["travel_time"] / df["expected_time"]
)

print("=== BASIC STATISTICS ===")

print("\nDistance:")
print(df["distance"].describe().to_string())

print("\nSpeed:")
print(df["speed"].describe().to_string())

print("\nTravel time:")
print(df["travel_time"].describe().to_string())

print("\n=== TIME CONSISTENCY ===")

print(
    "Expected travel time mean:",
    df["expected_time"].mean()
)

print(
    "Actual travel time mean:",
    df["travel_time"].mean()
)

print(
    "Mean absolute difference:",
    df["time_difference"].abs().mean()
)

print(
    "Median time ratio:",
    df["time_ratio"].median()
)

print(
    "Minimum time ratio:",
    df["time_ratio"].min()
)

print(
    "Maximum time ratio:",
    df["time_ratio"].max()
)

print("\n=== MOST EXTREME DIFFERENCES ===")

print(
    df.nlargest(10, "time_difference")[
        [
            "source_location",
            "destination_location",
            "distance",
            "speed",
            "travel_time",
            "expected_time",
            "time_ratio"
        ]
    ].to_string(index=False)
)