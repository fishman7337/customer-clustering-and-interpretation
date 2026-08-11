"""Data loading, validation, and preprocessing helpers."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from customer_segmentation.config import (
    COLUMN_ALIASES,
    CUSTOMER_ID_COLUMN,
    GENDER_COLUMN,
    MODEL_FEATURES,
)


class DataValidationError(ValueError):
    """Raised when the customer data does not match the expected schema."""


def load_customer_data(path: str | Path) -> pd.DataFrame:
    """Load a customer CSV file and normalize common source column names."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {csv_path}. Place the CA2 CSV in data/raw/ or pass --data."
        )

    return standardize_columns(pd.read_csv(csv_path))


def standardize_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the data with known column aliases normalized."""
    normalized = data.copy()
    normalized.columns = [str(column).strip() for column in normalized.columns]
    return normalized.rename(columns=COLUMN_ALIASES)


def validate_customer_schema(
    data: pd.DataFrame,
    required_columns: Iterable[str] = (*MODEL_FEATURES, GENDER_COLUMN),
) -> None:
    """Validate that all required customer columns are present."""
    missing = sorted(set(required_columns) - set(data.columns))
    if missing:
        raise DataValidationError(f"Missing required columns: {', '.join(missing)}")


def prepare_customer_data(
    data: pd.DataFrame,
    *,
    drop_outliers: bool = True,
    outlier_columns: Iterable[str] = ("Income (k$)",),
) -> pd.DataFrame:
    """Clean the raw customer data into the feature table used by the model."""
    prepared = standardize_columns(data)
    validate_customer_schema(prepared)

    selected_columns = [GENDER_COLUMN, *MODEL_FEATURES]
    if CUSTOMER_ID_COLUMN in prepared.columns:
        selected_columns = [CUSTOMER_ID_COLUMN, *selected_columns]

    prepared = prepared.loc[:, selected_columns].drop_duplicates().reset_index(drop=True)

    for column in MODEL_FEATURES:
        prepared[column] = pd.to_numeric(prepared[column], errors="coerce")

    if prepared[list(MODEL_FEATURES)].isna().any().any():
        bad_columns = (
            prepared[list(MODEL_FEATURES)]
            .columns[prepared[list(MODEL_FEATURES)].isna().any()]
            .tolist()
        )
        columns = ", ".join(bad_columns)
        raise DataValidationError(f"Numeric columns contain invalid values: {columns}")

    prepared[GENDER_COLUMN] = prepared[GENDER_COLUMN].astype(str).str.strip().str.title()
    unknown_gender = sorted(set(prepared[GENDER_COLUMN]) - {"Female", "Male"})
    if unknown_gender:
        raise DataValidationError(
            "Gender column contains unsupported values: " + ", ".join(unknown_gender)
        )

    if drop_outliers:
        prepared = remove_iqr_outliers(prepared, columns=outlier_columns)

    return prepared.reset_index(drop=True)


def remove_iqr_outliers(data: pd.DataFrame, *, columns: Iterable[str]) -> pd.DataFrame:
    """Remove rows outside the 1.5 IQR fences for the supplied columns."""
    filtered = data.copy()
    for column in columns:
        if column not in filtered.columns:
            raise DataValidationError(f"Cannot remove outliers for missing column: {column}")

        q1 = filtered[column].quantile(0.25)
        q3 = filtered[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        filtered = filtered[filtered[column].between(lower_bound, upper_bound, inclusive="both")]

    return filtered
