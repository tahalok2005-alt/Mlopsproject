"""Train a RandomForest classifier on the Wine dataset and save it to disk."""
import json
from pathlib import Path

import joblib
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
MODEL_PATH = MODEL_DIR / "model.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"


def train():
    data = load_wine(as_frame=True)
    # The raw column name contains a slash; rename it to match the API field.
    X = data.data.rename(columns={"od280/od315_of_diluted_wines": "od280_od315_ratio"})
    y = data.target
    target_names = [f"cultivar_{i + 1}" for i in range(len(data.target_names))]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "f1_macro": f1_score(y_test, preds, average="macro"),
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": model, "feature_names": X.columns.tolist(), "target_names": target_names},
        MODEL_PATH,
    )
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))

    print(f"Saved model to {MODEL_PATH}")
    print(f"Metrics: {metrics}")
    return metrics


if __name__ == "__main__":
    train()
