"""Tests for offcut tracking functionality.

TDD: These tests are written first, then implementation follows.
"""

from steel_optimisation_problem import Bin


class TestBinOffcut:
    """Tests for Bin.offcut property."""

    def test_offcut_equals_waste(self):
        """Offcut should be the same as waste (remaining material)."""
        bin_obj = Bin(capacity=100, kerf_width=0)
        bin_obj.update(30)
        bin_obj.update(40)

        assert bin_obj.offcut == bin_obj.waste
        assert bin_obj.offcut == 30

    def test_offcut_with_kerf(self):
        """Offcut should account for kerf loss."""
        bin_obj = Bin(capacity=100, kerf_width=3)
        bin_obj.update(30)
        bin_obj.update(40)

        # total_consumed = 30 + 40 + 3 (kerf) = 73
        # offcut = 100 - 73 = 27
        assert bin_obj.offcut == 27

    def test_offcut_empty_bin(self):
        """Empty bin should have offcut equal to capacity."""
        bin_obj = Bin(capacity=1000, kerf_width=5)

        assert bin_obj.offcut == 1000

    def test_offcut_full_bin(self):
        """Fully used bin should have zero offcut."""
        bin_obj = Bin(capacity=100, kerf_width=0)
        bin_obj.update(100)

        assert bin_obj.offcut == 0

    def test_offcut_nearly_full_bin(self):
        """Bin with small offcut."""
        bin_obj = Bin(capacity=1000, kerf_width=0)
        bin_obj.update(999)

        assert bin_obj.offcut == 1
