# Changelog

All notable changes to this project will be documented in this file.

Unreleased
----------

### Added
- **Kerf loss support**: Account for material lost during cutting (blade thickness)
  - `pack()` now accepts optional `kerf_width` parameter (default: 0)
  - `Bin` class tracks `kerf_loss`, `total_consumed`, and `waste` attributes
  - `Bin.can_fit()` method checks if item fits accounting for kerf
- **`get_packing_stats()` function**: Calculate statistics for packing solutions
  - Returns efficiency percentage, total kerf loss, waste, and more
- **CLI module** (`cli.py`): Separated interactive CLI from library code
  - `steel-opt` command available after install
  - `python -m steel_optimisation_problem` also works
- Comprehensive test suite for kerf loss scenarios (`tests/test_kerf_loss.py`)

### Changed
- `pack()` algorithm improved to use true First Fit (checks all bins, not just last)
- `Bin` class now supports float values for kerf precision
- Main CLI now prompts for kerf width
- **Switched from Poetry to UV** for faster, modern dependency management
- **Modernized type hints**: Using Python 3.12+ syntax (`list[T]`, `X | Y`)
- **Enhanced CI workflow**:
  - Multi-Python version testing (3.12, 3.13)
  - Ruff format checking in addition to linting
  - Package build verification with twine
  - 80% minimum coverage requirement
- **`StockInfo` is now a pure data class** (no side effects):
  - All parameters are required (no interactive input)
  - Added validation for `stock_length`, `number_of_stock`, and `kerf_width`
- **`StockInfo.check()` raises `ValueError`** instead of `SystemExit`

### Fixed
- Pack algorithm now correctly tries all existing bins (First Fit Decreasing)
  rather than only checking the most recent bin

### Breaking Changes
- `StockInfo()` no longer accepts interactive input; all parameters required
- `StockInfo.check()` raises `ValueError` instead of `SystemExit`
- Library code (`steel_opt.py`) no longer contains any `print()` or `input()` calls

### Developer Experience
- **Ruff configuration**: Comprehensive linting rules (pycodestyle, pyflakes, isort,
  flake8-bugbear, pylint, and more)
- **Ruff formatting**: Consistent code style with `ruff format`
- **pytest-cov**: Coverage reporting with branch coverage
- **hatchling**: Modern PEP 517 build backend

---

- Improve repository README and add contributing guidance. (unreleased)
