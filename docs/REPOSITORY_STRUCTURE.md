# Repository Structure

```text
.
├── .github/
│   ├── dependabot.yml
│   └── workflows/ci.yml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── presentation/
│   ├── DATA.md
│   ├── MLOPS.md
│   ├── MODEL_CARD.md
│   ├── PROJECT_CONTEXT.md
│   └── REPOSITORY_STRUCTURE.md
├── models/
├── notebooks/
│   ├── customer_segmentation_analysis.ipynb
│   └── sections/
├── reports/
│   └── figures/
├── src/
│   └── customer_segmentation/
└── tests/
```

## Folder Responsibilities

- `data/raw/`: local source CSV files.
- `data/processed/`: optional cleaned or derived datasets.
- `docs/`: permanent project documentation.
- `docs/presentation/`: submitted slide deck.
- `models/`: generated model artifacts.
- `notebooks/`: preserved full academic notebook and derived smaller section notebooks.
- `reports/`: generated metrics, labelled outputs, and figures.
- `src/`: reusable package code.
- `tests/`: automated test suite.
