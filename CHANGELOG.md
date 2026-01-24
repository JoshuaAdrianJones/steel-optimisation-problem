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
- **Programmatic `StockInfo` initialization**: No longer requires interactive input
  - `StockInfo(stock_length=6000, number_of_stock=10, kerf_width=3)`
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

### Fixed
- Pack algorithm now correctly tries all existing bins (First Fit Decreasing)
  rather than only checking the most recent bin

### Developer Experience
- **Ruff configuration**: Comprehensive linting rules (pycodestyle, pyflakes, isort,
  flake8-bugbear, pylint, and more)
- **Ruff formatting**: Consistent code style with `ruff format`
- **pytest-cov**: Coverage reporting with branch coverage
- **hatchling**: Modern PEP 517 build backend

---

- Improve repository README and add contributing guidance. (unreleased)
