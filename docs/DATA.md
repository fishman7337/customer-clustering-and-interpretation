# Data Contract

## Expected Input

The default training command expects a CSV file at:

```text
data/raw/CA2-Customer-Data.csv
```

You can pass another path with:

```powershell
customer-segmentation train --data path/to/customers.csv
```

## Required Columns

| Column | Type | Description |
| --- | --- | --- |
| `Gender` | categorical | Customer gender, expected values are `Female` or `Male`. |
| `Age` | numeric | Customer age. |
| `Income (k$)` | numeric | Annual income in thousands. |
| `How Much They Spend` | numeric | Spending behavior score used for segmentation. |

`CustomerID` is optional. If present, it is preserved in labelled outputs but not used as a
model feature.

## Accepted Aliases

The Python package normalizes these common source names:

| Source column | Normalized column |
| --- | --- |
| `Genre` | `Gender` |
| `Annual Income (k$)` | `Income (k$)` |
| `Spending Score (1-100)` | `How Much They Spend` |
| `Spending Score` | `How Much They Spend` |

## Preprocessing

- Duplicate rows are dropped.
- Numeric feature columns are coerced to numeric and rejected if invalid values appear.
- `Gender` values are normalized to title case and validated.
- Income outliers are removed with the 1.5 IQR rule by default.
- The model uses `Age`, `Income (k$)`, and `How Much They Spend` as clustering features.

## Privacy and Governance

Do not commit raw customer data unless its license, privacy status, and assessment rules are
clear. Treat customer-level data as sensitive even when it appears anonymized.
