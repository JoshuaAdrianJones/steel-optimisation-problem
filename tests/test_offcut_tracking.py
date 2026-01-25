"""Tests for offcut tracking functionality.

TDD: These tests are written first, then implementation follows.
"""

from steel_optimisation_problem import Bin, get_packing_stats, pack


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
