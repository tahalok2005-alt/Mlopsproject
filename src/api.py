"""FastAPI inference service for the Wine model, instrumented for Prometheus."""
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field

from src.inference import predict

app = FastAPI(title="Wine Classifier API", version="1.0.0")

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


class WineFeatures(BaseModel):
    alcohol: float = Field(..., gt=0, examples=[14.23])
    malic_acid: float = Field(..., gt=0, examples=[1.71])
    ash: float = Field(..., gt=0, examples=[2.43])
    alcalinity_of_ash: float = Field(..., gt=0, examples=[15.6])
    magnesium: float = Field(..., gt=0, examples=[127.0])
    total_phenols: float = Field(..., gt=0, examples=[2.8])
    flavanoids: float = Field(..., gt=0, examples=[3.06])
    nonflavanoid_phenols: float = Field(..., gt=0, examples=[0.28])
    proanthocyanins: float = Field(..., gt=0, examples=[2.29])
    color_intensity: float = Field(..., gt=0, examples=[5.64])
    hue: float = Field(..., gt=0, examples=[1.04])
    od280_od315_ratio: float = Field(..., gt=0, examples=[3.92])
    proline: float = Field(..., gt=0, examples=[1065.0])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict_endpoint(features: WineFeatures):
    try:
        return predict(features.model_dump())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
