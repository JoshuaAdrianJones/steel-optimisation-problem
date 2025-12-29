# Contributing

Thanks for considering contributing — small, focused contributions are welcome.

Development setup
-----------------
1. Create a virtualenv and install the package in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt  # optional if present
```

Running tests
-------------
Run tests from the repository root. The test environment expects the package importable from `src`:

```bash
PYTHONPATH=src pytest -q
```

Style and linting
-----------------
This project uses `ruff` for linting. To check locally:

```bash
ruff check src tests
```

Submitting changes
------------------
- Fork the repository and create a branch named `issue/<number>-short-desc`.
- Keep commits focused and reference the issue number in commit messages (e.g. `fix(issue-10): ...`).
- Run tests and linters locally before opening a PR.

For larger changes, open an issue first to discuss the approach.
