"""Shared helper to load the trained model and run predictions."""
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model.pkl"


@lru_cache(maxsize=1)
def load_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No trained model found at {MODEL_PATH}. Run `python -m src.train` first."
        )
    return joblib.load(MODEL_PATH)


def predict(features: dict[str, float]):
    bundle = load_bundle()
    model = bundle["model"]
    target_names = bundle["target_names"]
    feature_names = bundle["feature_names"]

    frame = pd.DataFrame([features], columns=feature_names)
    pred_idx = int(model.predict(frame)[0])
    proba = model.predict_proba(frame)[0].tolist()

    return {
        "predicted_class": target_names[pred_idx],
        "predicted_index": pred_idx,
        "probabilities": dict(zip(target_names, proba)),
    }
