"""Project-wide configuration constants."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CUSTOMER_ID_COLUMN = "CustomerID"
GENDER_COLUMN = "Gender"
MODEL_FEATURES = ("Age", "Income (k$)", "How Much They Spend")
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "CA2-Customer-Data.csv"
MODEL_OUTPUT_PATH = PROJECT_ROOT / "models" / "customer_segmentation_kmeans.joblib"
METRICS_OUTPUT_PATH = PROJECT_ROOT / "reports" / "metrics.json"
SEGMENTS_OUTPUT_PATH = PROJECT_ROOT / "reports" / "customer_segments.csv"

COLUMN_ALIASES = {
    "Genre": GENDER_COLUMN,
    "Annual Income (k$)": "Income (k$)",
    "Spending Score (1-100)": "How Much They Spend",
    "Spending Score": "How Much They Spend",
}
