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

### Fixed
- Pack algorithm now correctly tries all existing bins (First Fit Decreasing)
  rather than only checking the most recent bin

---

- Improve repository README and add contributing guidance. (unreleased)
