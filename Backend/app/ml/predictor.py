import numpy as np


def predict(model, features):
    feature_array = np.array(features)

    prediction = model.predict(feature_array)

    return prediction