"""Tests for offcut tracking functionality.

TDD: These tests are written first, then implementation follows.
"""

from steel_optimisation_problem import Bin, get_packing_stats, get_usable_offcuts, pack


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


class TestPackingStatsOffcuts:
    """Tests for offcuts list in get_packing_stats()."""

    def test_offcuts_in_stats(self):
        """Stats should include list of offcut lengths."""
        bins = pack([400, 400, 400], bin_size=1000, kerf_width=0)
        stats = get_packing_stats(bins)

        assert "offcuts" in stats
        assert isinstance(stats["offcuts"], list)

    def test_offcuts_values(self):
        """Offcuts list should contain correct values for each bin."""
        # 3 items of 400mm each, bin size 1000mm
        # Should pack into 2 bins: [400, 400] and [400]
        bins = pack([400, 400, 400], bin_size=1000, kerf_width=0)
        stats = get_packing_stats(bins)

        # Bin 1: 400+400=800, offcut=200
        # Bin 2: 400, offcut=600
        assert sorted(stats["offcuts"]) == [200, 600]

    def test_offcuts_with_kerf(self):
        """Offcuts should account for kerf loss."""
        # 2 items of 400mm, bin size 1000mm, kerf 5mm
        # Bin 1: 400 + 5 + 400 = 805, offcut = 195
        bins = pack([400, 400], bin_size=1000, kerf_width=5)
        stats = get_packing_stats(bins)

        assert stats["offcuts"] == [195]

    def test_offcuts_empty_bins_list(self):
        """Empty bins list should return empty offcuts."""
        stats = get_packing_stats([])

        assert stats["offcuts"] == []

    def test_offcuts_single_bin_full(self):
        """Single bin fully used should have zero offcut."""
        bins = pack([500, 500], bin_size=1000, kerf_width=0)
        stats = get_packing_stats(bins)

        assert stats["offcuts"] == [0]

    def test_offcuts_matches_total_waste(self):
        """Sum of offcuts should equal total_waste."""
        bins = pack([300, 400, 500, 200], bin_size=1000, kerf_width=3)
        stats = get_packing_stats(bins)

        assert sum(stats["offcuts"]) == stats["total_waste"]


class TestGetUsableOffcuts:
    """Tests for get_usable_offcuts() function."""

    def test_returns_all_offcuts_by_default(self):
        """With no min_length, return all offcuts."""
        bins = pack([400, 400, 400], bin_size=1000, kerf_width=0)
        offcuts = get_usable_offcuts(bins)

        # Offcuts: 200 and 600
        assert sorted(offcuts) == [200, 600]

    def test_filters_by_min_length(self):
        """Only return offcuts >= min_length."""
        bins = pack([400, 400, 400], bin_size=1000, kerf_width=0)
        offcuts = get_usable_offcuts(bins, min_length=300)

        # Only 600 >= 300
        assert offcuts == [600]

    def test_min_length_excludes_all(self):
        """When min_length exceeds all offcuts, return empty list."""
        bins = pack([400, 400, 400], bin_size=1000, kerf_width=0)
        offcuts = get_usable_offcuts(bins, min_length=1000)

        assert offcuts == []

    def test_min_length_zero_returns_all(self):
        """min_length=0 should return all offcuts including zeros."""
        bins = pack([500, 500], bin_size=1000, kerf_width=0)
        offcuts = get_usable_offcuts(bins, min_length=0)

        # Single bin fully used, offcut=0
        assert offcuts == [0]

    def test_min_length_excludes_zero_offcuts(self):
        """min_length=1 should exclude zero offcuts."""
        bins = pack([500, 500], bin_size=1000, kerf_width=0)
        offcuts = get_usable_offcuts(bins, min_length=1)

        # Zero offcut excluded
        assert offcuts == []

    def test_empty_bins_list(self):
        """Empty bins list returns empty offcuts."""
        offcuts = get_usable_offcuts([])

        assert offcuts == []

    def test_preserves_order(self):
        """Offcuts should be in same order as bins."""
        bins = pack([900, 100], bin_size=1000, kerf_width=0)
        # FFD: sorts to [900, 100], both fit in one bin
        # Bin 1: 900+100=1000, offcut=0
        offcuts = get_usable_offcuts(bins)

        assert offcuts == [0]

    def test_real_world_scenario(self):
        """Realistic scenario: find reusable offcuts for small parts."""
        # Cutting various lengths from 6m bars
        cuts = [1500, 1500, 1200, 1000, 800, 500, 500, 300]
        bins = pack(cuts, bin_size=6000, kerf_width=3)

        # Find offcuts >= 200mm (could be used for small brackets)
        usable = get_usable_offcuts(bins, min_length=200)

        # All offcuts should be >= 200
        assert all(o >= 200 for o in usable)
