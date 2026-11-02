from src.train import train


def test_train_produces_reasonable_accuracy():
    metrics = train()
    assert metrics["accuracy"] >= 0.85
    assert metrics["f1_macro"] >= 0.85
