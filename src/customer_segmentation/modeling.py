"""Model training and evaluation utilities."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from math import nan
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from customer_segmentation.config import MODEL_FEATURES


@dataclass(frozen=True)
class ClusteringMetrics:
    """Evaluation metrics for an unsupervised clustering run."""

    n_samples: int
    n_clusters: int
    silhouette_score: float
    davies_bouldin_score: float
    calinski_harabasz_score: float
    inertia: float | None

    def to_dict(self) -> dict[str, float | int | None]:
        """Convert metrics to a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class TrainingResult:
    """Container for the trained pipeline, labels, and metrics."""

    pipeline: Pipeline
    labels: np.ndarray
    metrics: ClusteringMetrics
    feature_columns: tuple[str, ...]


def build_kmeans_pipeline(
    *,
    n_clusters: int = 6,
    random_state: int = 42,
    n_init: int = 10,
) -> Pipeline:
    """Build the standard scaler plus K-Means pipeline used by this project."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "clusterer",
                KMeans(
                    n_clusters=n_clusters,
                    init="random",
                    max_iter=100,
                    n_init=n_init,
                    algorithm="lloyd",
                    random_state=random_state,
                ),
            ),
        ]
    )


def train_kmeans_model(
    data: pd.DataFrame,
    *,
    feature_columns: Iterable[str] = MODEL_FEATURES,
    n_clusters: int = 6,
    random_state: int = 42,
) -> TrainingResult:
    """Train K-Means on prepared customer data and return labels plus metrics."""
    features = tuple(feature_columns)
    missing = sorted(set(features) - set(data.columns))
    if missing:
        raise ValueError(f"Missing feature columns: {', '.join(missing)}")
    if len(data) <= n_clusters:
        raise ValueError("K-Means requires more rows than clusters.")

    x = data.loc[:, features]
    pipeline = build_kmeans_pipeline(n_clusters=n_clusters, random_state=random_state)
    labels = pipeline.fit_predict(x)
    clusterer = pipeline.named_steps["clusterer"]
    metrics = evaluate_clustering(
        x,
        labels,
        inertia=float(clusterer.inertia_),
    )

    return TrainingResult(
        pipeline=pipeline,
        labels=labels,
        metrics=metrics,
        feature_columns=features,
    )


def evaluate_clustering(
    data: pd.DataFrame,
    labels: np.ndarray,
    *,
    inertia: float | None = None,
) -> ClusteringMetrics:
    """Evaluate clustering labels with guardrails for degenerate label sets."""
    unique_labels = np.unique(labels)
    n_samples = len(labels)
    n_clusters = len(unique_labels)

    if n_clusters < 2 or n_clusters >= n_samples:
        return ClusteringMetrics(
            n_samples=n_samples,
            n_clusters=n_clusters,
            silhouette_score=nan,
            davies_bouldin_score=nan,
            calinski_harabasz_score=nan,
            inertia=inertia,
        )

    return ClusteringMetrics(
        n_samples=n_samples,
        n_clusters=n_clusters,
        silhouette_score=float(silhouette_score(data, labels)),
        davies_bouldin_score=float(davies_bouldin_score(data, labels)),
        calinski_harabasz_score=float(calinski_harabasz_score(data, labels)),
        inertia=inertia,
    )


def save_model(pipeline: Pipeline, path: str | Path) -> Path:
    """Persist a trained pipeline with joblib."""
    model_path = Path(path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    return model_path
