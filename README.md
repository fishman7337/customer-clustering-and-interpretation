# Customer Segmentation and Interpretation

Production-ready repository for a customer clustering study using unsupervised machine
learning. The original academic notebook is preserved, while the reusable workflow is now
packaged, tested, documented, and protected by CI checks.

## Evidence and interpretation

| Evidence-backed measure | Current repository evidence |
| --- | --- |
| Model comparison | The notebooks compare **3 clustering families**: K-Means, Agglomerative Clustering, and DBSCAN. |
| Packaged default | The reusable workflow defaults to **6 K-Means segments** and reports four internal evaluation measures. |

The qualitative outcome is an interpretable segmentation workflow with preprocessing, outlier handling, scaling, model comparison, and business-oriented profiles. Marketing implications are analytical interpretations, not measured campaign lift.

## Academic Context

This project was completed under Singapore Polytechnic, School of Computing, Diploma in
Applied AI & Analytics. It was submitted for the AI & Machine Learning module (ST1511),
CA2 Part B, by Goh Kun Ming, DAAA student, in AY24/25 Year 1 Semester 2. The lecturer was
Adjunct Lecturer Tai Hock Lin (Andy).

## What This Project Does

The project segments customers using demographic and spending behavior features. The
main clustering workflow focuses on:

- Data validation and preprocessing.
- Outlier handling with the IQR method.
- Feature scaling with standardization.
- K-Means clustering with six customer segments by default.
- Cluster evaluation using silhouette, Davies-Bouldin, Calinski-Harabasz, and inertia in the same standardized feature space used to fit K-Means.
- Model and report artifact generation through a command line interface.

## Repository Layout

```text
.
├── .github/workflows/        # CI for tests, linting, and security checks
├── data/                     # Local data drop zone; raw data is intentionally ignored
├── docs/                     # Project, model, MLOps, data, and governance documentation
├── models/                   # Generated model artifacts; ignored by git
├── notebooks/                # Full original notebook plus smaller section notebooks
├── reports/                  # Generated metrics, labelled outputs, and figures
├── src/customer_segmentation # Tested Python package and CLI
└── tests/                    # Pytest suite
```

## Quick Start

Create a virtual environment and install the development dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Place the CA2 customer CSV at:

```text
data/raw/CA2-Customer-Data.csv
```

Train the model:

```powershell
customer-segmentation train --data data/raw/CA2-Customer-Data.csv
```

Default outputs:

- `models/customer_segmentation_kmeans.joblib`
- `reports/metrics.json`
- `reports/customer_segments.csv`

## Development Checks

Run the same local checks that CI runs:

```powershell
ruff check .
pytest
bandit -c pyproject.toml -r src scripts
pip-audit --skip-editable .
```

## Notebook

The original full notebook is available at
`notebooks/customer_segmentation_analysis.ipynb`. It now points to the normalized project
folders:

- Input data: `../data/raw/CA2-Customer-Data.csv`
- Saved models: `../models/`

For easier review, the same notebook content is split into smaller phase notebooks under
`notebooks/sections/`. The split notebooks preserve the full notebook's cells in order, and
the test suite verifies that the split files recombine back to the original cell content.

## Documentation

- [Project context](docs/PROJECT_CONTEXT.md)
- [Data contract](docs/DATA.md)
- [Model card](docs/MODEL_CARD.md)
- [MLOps workflow](docs/MLOPS.md)
- [Repository structure](docs/REPOSITORY_STRUCTURE.md)
- [Contributing guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Code of conduct](CODE_OF_CONDUCT.md)

## Governance

Raw data, trained models, and generated reports are excluded from version control by
default. Commit those artifacts only when their licensing, privacy, and assessment
requirements are clear.

## License

This project is released under the [MIT License](LICENSE).
