from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from customer_segmentation.cli import main


def test_train_cli_writes_model_metrics_and_segments(tmp_path: Path) -> None:
    rows = []
    for offset in range(8):
        rows.append(["Female", 20 + offset, 30 + offset, 80 - offset])
        rows.append(["Male", 45 + offset, 70 + offset, 45 + offset])
        rows.append(["Female", 60 + offset, 95 + offset, 20 + offset])

    data_path = tmp_path / "customers.csv"
    pd.DataFrame(
        rows,
        columns=["Gender", "Age", "Income (k$)", "How Much They Spend"],
    ).to_csv(data_path, index=False)

    model_output = tmp_path / "model.joblib"
    metrics_output = tmp_path / "metrics.json"
    segments_output = tmp_path / "segments.csv"

    exit_code = main(
        [
            "train",
            "--data",
            str(data_path),
            "--model-output",
            str(model_output),
            "--metrics-output",
            str(metrics_output),
            "--segments-output",
            str(segments_output),
            "--clusters",
            "3",
        ]
    )

    assert exit_code == 0
    assert model_output.exists()
    assert metrics_output.exists()
    assert segments_output.exists()

    metrics = json.loads(metrics_output.read_text(encoding="utf-8"))
    segments = pd.read_csv(segments_output)

    assert metrics["model"] == "KMeans"
    assert metrics["metrics"]["n_clusters"] == 3
    assert "Cluster" in segments.columns
