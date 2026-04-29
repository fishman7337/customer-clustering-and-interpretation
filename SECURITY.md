# Security Policy

## Supported Versions

This repository currently supports the `main` branch.

## Reporting a Vulnerability

Report suspected vulnerabilities privately to the repository owner. Please include:

- A short description of the issue.
- Steps to reproduce it.
- Affected files, commands, or dependencies.
- Any suggested mitigation, if known.

Avoid opening public issues for sensitive security reports.

## Security Practices

- CI runs Bandit static analysis on `src/`.
- CI runs `pip-audit` for dependency vulnerability checks.
- `.gitignore` excludes raw data, generated models, reports, virtual environments, and
  environment files.
- Pre-commit hooks include private key detection.
- No credentials or personal data should be committed.
