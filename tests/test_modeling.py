from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from customer_segmentation.modeling import train_kmeans_model


def make_clustered_customers() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    centers = np.array(
        [
            [22, 30, 80],
            [42, 65, 45],
            [60, 95, 20],
        ]
    )
    rows = []
    for center in centers:
        rows.extend(center + rng.normal(0, 2, size=(8, 3)))

    return pd.DataFrame(rows, columns=["Age", "Income (k$)", "How Much They Spend"])


def test_train_kmeans_model_returns_labels_and_metrics() -> None:
    customers = make_clustered_customers()

    result = train_kmeans_model(customers, n_clusters=3, random_state=42)

    assert len(result.labels) == len(customers)
    assert result.metrics.n_clusters == 3
    assert result.metrics.n_samples == len(customers)
    assert result.metrics.silhouette_score > 0
    assert result.metrics.inertia is not None


def test_train_kmeans_model_requires_more_rows_than_clusters() -> None:
    customers = pd.DataFrame(
        {
            "Age": [20, 21],
            "Income (k$)": [30, 32],
            "How Much They Spend": [80, 82],
        }
    )

    with pytest.raises(ValueError, match="more rows than clusters"):
        train_kmeans_model(customers, n_clusters=2)
