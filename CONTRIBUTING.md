# Contributing

Thank you for improving this project. This repository contains an academic notebook and a
production-style Python package, so please keep changes clear, reproducible, and easy to
review.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Development Workflow

1. Create a focused branch.
2. Keep raw data, trained models, generated reports, and secrets out of git.
3. Update tests when behavior changes.
4. Update documentation when commands, outputs, assumptions, or limitations change.
5. Run the local quality checks before pushing.

```powershell
ruff check .
pytest
bandit -c pyproject.toml -r src
pip-audit --skip-editable .
```

## Data Rules

Do not commit raw datasets unless the license and privacy status are explicit. Use
`data/raw/` for local files and document any source or preprocessing decisions in
`docs/DATA.md`.

## Pull Request Checklist

- The change has a clear purpose.
- Tests pass locally.
- Security checks pass or any exception is documented.
- Documentation reflects the new behavior.
- The notebook remains a reproducible record of the original analysis.
