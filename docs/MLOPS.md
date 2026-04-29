# MLOps Workflow

## Lifecycle

1. Place source data in `data/raw/`.
2. Validate schema and clean the dataset with the package preprocessing code.
3. Train the K-Means pipeline through the CLI.
4. Export the model to `models/`.
5. Export metrics and labelled customer segments to `reports/`.
6. Review metrics and cluster profiles before using the output for recommendations.

## Local Commands

```powershell
python -m pip install -r requirements-dev.txt
ruff check .
pytest
bandit -c pyproject.toml -r src
pip-audit --skip-editable .
customer-segmentation train --data data/raw/CA2-Customer-Data.csv
```

## CI Gates

GitHub Actions runs:

- Ruff linting.
- Pytest with coverage output.
- Bandit static security scanning.
- Pip dependency vulnerability audit.

Dependabot monitors GitHub Actions and Python dependencies weekly.

## Reproducibility

- The CLI uses `random_state=42` by default.
- The package stores model configuration in source code.
- Generated artifacts are ignored by git and can be regenerated from the data and code.
- The notebook remains as a human-readable analysis record.

## Artifact Policy

Raw data, trained models, and reports should not be committed by default. Commit generated
artifacts only when the project owner confirms that they are allowed and useful for review.

## Future Enhancements

- Add dataset versioning with DVC or an equivalent artifact store.
- Add model registry integration if the project moves beyond coursework.
- Add notebook execution checks once the dataset can be distributed safely.
- Add drift monitoring if future customer batches are scored regularly.
