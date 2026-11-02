"""Standalone Streamlit demo for the Wine classifier (loads model directly, no API needed)."""
from pathlib import Path

import streamlit as st

from src.inference import MODEL_PATH, predict
from src.train import train

# name: (label, min, max, default)
FEATURES = {
    "alcohol": ("Alcohol (%)", 11.0, 15.0, 14.23),
    "malic_acid": ("Malic acid", 0.7, 5.8, 1.71),
    "ash": ("Ash", 1.3, 3.3, 2.43),
    "alcalinity_of_ash": ("Alcalinity of ash", 10.0, 30.0, 15.6),
    "magnesium": ("Magnesium", 70.0, 165.0, 127.0),
    "total_phenols": ("Total phenols", 0.9, 3.9, 2.8),
    "flavanoids": ("Flavanoids", 0.3, 5.1, 3.06),
    "nonflavanoid_phenols": ("Nonflavanoid phenols", 0.1, 0.7, 0.28),
    "proanthocyanins": ("Proanthocyanins", 0.4, 3.6, 2.29),
    "color_intensity": ("Color intensity", 1.2, 13.0, 5.64),
    "hue": ("Hue", 0.4, 1.8, 1.04),
    "od280_od315_ratio": ("OD280/OD315 ratio", 1.2, 4.0, 3.92),
    "proline": ("Proline", 270.0, 1700.0, 1065.0),
}

st.set_page_config(page_title="Wine Classifier", page_icon="🍷")
st.title("🍷 Wine Cultivar Classifier")
st.caption("A simple MLOps demo project — RandomForest trained on the UCI Wine dataset.")

if not Path(MODEL_PATH).exists():
    with st.spinner("No trained model found — training one now..."):
        train()

col1, col2 = st.columns(2)
values = {}
for i, (name, (label, low, high, default)) in enumerate(FEATURES.items()):
    with col1 if i % 2 == 0 else col2:
        values[name] = st.slider(label, low, high, default)

if st.button("Predict cultivar", type="primary"):
    result = predict(values)
    st.success(f"Predicted cultivar: **{result['predicted_class']}**")
    st.bar_chart(result["probabilities"])
