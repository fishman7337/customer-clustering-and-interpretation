"""Command line interface for training the customer segmentation model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from customer_segmentation.config import (
    METRICS_OUTPUT_PATH,
    MODEL_FEATURES,
    MODEL_OUTPUT_PATH,
    RAW_DATA_PATH,
    SEGMENTS_OUTPUT_PATH,
)
from customer_segmentation.data import load_customer_data, prepare_customer_data
from customer_segmentation.modeling import save_model, train_kmeans_model


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="customer-segmentation",
        description="Train and export the customer segmentation K-Means model.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    train = subparsers.add_parser("train", help="Train the clustering model.")
    train.add_argument("--data", type=Path, default=RAW_DATA_PATH, help="Path to the input CSV.")
    train.add_argument(
        "--model-output",
        type=Path,
        default=MODEL_OUTPUT_PATH,
        help="Path for the trained joblib model.",
    )
    train.add_argument(
        "--metrics-output",
        type=Path,
        default=METRICS_OUTPUT_PATH,
        help="Path for metrics JSON.",
    )
    train.add_argument(
        "--segments-output",
        type=Path,
        default=SEGMENTS_OUTPUT_PATH,
        help="Path for labelled customer CSV.",
    )
    train.add_argument("--clusters", type=int, default=6, help="Number of K-Means clusters.")
    train.add_argument("--random-state", type=int, default=42, help="Random seed.")
    train.add_argument(
        "--keep-outliers",
        action="store_true",
        help="Keep rows outside the IQR outlier fences.",
    )

    return parser


def train_command(args: argparse.Namespace) -> int:
    """Run the training command and persist outputs."""
    raw_data = load_customer_data(args.data)
    prepared_data = prepare_customer_data(raw_data, drop_outliers=not args.keep_outliers)
    result = train_kmeans_model(
        prepared_data,
        feature_columns=MODEL_FEATURES,
        n_clusters=args.clusters,
        random_state=args.random_state,
    )

    save_model(result.pipeline, args.model_output)

    labelled = prepared_data.copy()
    labelled["Cluster"] = result.labels
    args.segments_output.parent.mkdir(parents=True, exist_ok=True)
    labelled.to_csv(args.segments_output, index=False)

    metrics_payload = {
        "model": "KMeans",
        "feature_columns": list(result.feature_columns),
        "metrics": result.metrics.to_dict(),
    }
    args.metrics_output.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_output.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")

    print(f"Saved model to {args.model_output}")
    print(f"Saved metrics to {args.metrics_output}")
    print(f"Saved labelled segments to {args.segments_output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "train":
        return train_command(args)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
