import pytest
from fastapi.testclient import TestClient

from src.api import app
from src.train import train

PAYLOAD = {
    "alcohol": 14.23,
    "malic_acid": 1.71,
    "ash": 2.43,
    "alcalinity_of_ash": 15.6,
    "magnesium": 127.0,
    "total_phenols": 2.8,
    "flavanoids": 3.06,
    "nonflavanoid_phenols": 0.28,
    "proanthocyanins": 2.29,
    "color_intensity": 5.64,
    "hue": 1.04,
    "od280_od315_ratio": 3.92,
    "proline": 1065.0,
}


@pytest.fixture(scope="module", autouse=True)
def ensure_model():
    train()


client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_predict():
    resp = client.post("/predict", json=PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert body["predicted_class"] == "cultivar_1"
    assert set(body["probabilities"]) == {"cultivar_1", "cultivar_2", "cultivar_3"}
    assert abs(sum(body["probabilities"].values()) - 1.0) < 1e-6


def test_predict_rejects_invalid_input():
    resp = client.post("/predict", json={**PAYLOAD, "alcohol": -1})
    assert resp.status_code == 422


def test_metrics_endpoint_exposed():
    resp = client.get("/metrics")
    assert resp.status_code == 200
