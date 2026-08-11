from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from customer_segmentation.data import (
    DataValidationError,
    prepare_customer_data,
    standardize_columns,
)


def test_standardize_columns_accepts_common_mall_customer_aliases() -> None:
    raw = pd.DataFrame(
        {
            "Genre": ["Male"],
            "Age": [21],
            "Annual Income (k$)": [42],
            "Spending Score (1-100)": [70],
        }
    )

    standardized = standardize_columns(raw)

    assert {"Gender", "Age", "Income (k$)", "How Much They Spend"} <= set(standardized.columns)


def test_prepare_customer_data_drops_id_duplicates_and_income_outliers() -> None:
    raw = pd.DataFrame(
        {
            "CustomerID": [1, 1, 2, 3, 4, 5],
            "Gender": ["Female", "Female", "Male", "Male", "Female", "Male"],
            "Age": [20, 20, 21, 22, 23, 24],
            "Income (k$)": [40, 40, 42, 43, 44, 400],
            "How Much They Spend": [65, 65, 61, 62, 63, 64],
        }
    )

    prepared = prepare_customer_data(raw)

    assert len(prepared) == 4
    assert prepared["CustomerID"].tolist() == [1, 2, 3, 4]


def test_prepare_customer_data_rejects_unknown_gender_values() -> None:
    raw = pd.DataFrame(
        {
            "Gender": ["Unknown"],
            "Age": [20],
            "Income (k$)": [40],
            "How Much They Spend": [65],
        }
    )

    with pytest.raises(DataValidationError, match="unsupported values"):
        prepare_customer_data(raw)


def test_prepare_customer_data_rejects_conflicting_duplicate_customer_ids() -> None:
    raw = pd.DataFrame(
        {
            "CustomerID": [1, "1"],
            "Gender": ["Female", "Female"],
            "Age": [20, 21],
            "Income (k$)": [40, 42],
            "How Much They Spend": [65, 61],
        }
    )

    with pytest.raises(DataValidationError, match="conflicting duplicate IDs"):
        prepare_customer_data(raw)


@pytest.mark.parametrize("customer_id", [np.nan, np.inf, -np.inf, "not-a-number"])
def test_prepare_customer_data_rejects_non_finite_customer_ids(customer_id) -> None:
    raw = pd.DataFrame(
        {
            "CustomerID": [customer_id],
            "Gender": ["Female"],
            "Age": [20],
            "Income (k$)": [40],
            "How Much They Spend": [65],
        }
    )

    with pytest.raises(DataValidationError, match="finite numeric values"):
        prepare_customer_data(raw)


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("Age", np.nan),
        ("Income (k$)", np.inf),
        ("How Much They Spend", -np.inf),
    ],
)
def test_prepare_customer_data_rejects_non_finite_model_features(column, value) -> None:
    row = {
        "CustomerID": [1],
        "Gender": ["Female"],
        "Age": [20],
        "Income (k$)": [40],
        "How Much They Spend": [65],
    }
    row[column] = [value]

    with pytest.raises(DataValidationError, match="non-finite values") as error:
        prepare_customer_data(pd.DataFrame(row))

    assert column in str(error.value)
