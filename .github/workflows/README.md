# GitHub Actions Workflows

This folder contains CI workflow definitions.

## Workflows

- `ci.yml`: runs Ruff linting, pytest, Bandit security scanning, and pip-audit on pushes
  and pull requests targeting `main`.

When adding a new workflow, document its trigger, purpose, and required secrets here.
