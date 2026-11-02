"""Send a steady stream of random predictions so the Grafana dashboard has live data."""
import json
import random
import sys
import time
import urllib.request

API_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001"

# name: (min, max), taken from the Wine dataset's ranges.
FEATURES = {
    "alcohol": (11.0, 14.8),
    "malic_acid": (0.8, 5.8),
    "ash": (1.4, 3.2),
    "alcalinity_of_ash": (10.6, 30.0),
    "magnesium": (70.0, 162.0),
    "total_phenols": (1.0, 3.9),
    "flavanoids": (0.4, 5.0),
    "nonflavanoid_phenols": (0.2, 0.6),
    "proanthocyanins": (0.5, 3.5),
    "color_intensity": (1.3, 13.0),
    "hue": (0.5, 1.7),
    "od280_od315_ratio": (1.3, 4.0),
    "proline": (280.0, 1680.0),
}


def main():
    print(f"Sending predictions to {API_URL} (Ctrl+C to stop)")
    while True:
        payload = {name: random.uniform(low, high) for name, (low, high) in FEATURES.items()}
        request = urllib.request.Request(
            f"{API_URL}/predict",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(request, timeout=5).read()
        time.sleep(random.uniform(0.1, 0.6))


if __name__ == "__main__":
    main()
