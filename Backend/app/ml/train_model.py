import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


TRAIN_PATH = "data/processed/train.csv"
TEST_PATH = "data/processed/test.csv"


FEATURES = [
    "lat_src",
    "lon_src",
    "lat_dest",
    "lon_dest",
    "distance",
    "day_of_week",
    "hour",
    "is_peak",
    "weather",
    "road_capacity",
    "vehicles",
    "speed",
    "signal_time"
]

TARGET = "travel_time"


print("Loading training data...")

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)


X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]


# Convert categorical columns
for column in ["day_of_week", "weather"]:
    X_train[column] = X_train[column].astype("category")
    X_test[column] = X_test[column].astype("category")


print("\nTraining LightGBM...")


model = lgb.LGBMRegressor(
    objective="regression",
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,
    random_state=42,
    n_jobs=-1
)


model.fit(
    X_train,
    y_train,
    categorical_feature=["day_of_week", "weather"]
)


print("\nModel training complete.")


predictions = model.predict(X_test)


mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))


print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")

MODEL_PATH = "app/ml/lightgbm_model.txt"

model.booster_.save_model(MODEL_PATH)

print(f"\nModel saved to:")
print(MODEL_PATH)