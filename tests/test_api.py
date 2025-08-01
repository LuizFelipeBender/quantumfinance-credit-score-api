import joblib
import numpy as np

def test_model_load_and_predict():
    model = joblib.load("models/model_latest.pkl")
    encoder = joblib.load("models/label_encoder.pkl")

    sample = np.array([[48000.0, 3800.0, 2, 1, 15.0, 1, 4, 2.0, 1200.0, 2.0, 34.5, 1600.0, 2500.0, 29]])
    pred = model.predict(sample)
    
    assert pred.shape == (1,)
    assert pred[0] in [0, 1, 2]
