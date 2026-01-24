"""Tests for kerf loss functionality in steel optimization."""

import pytest
from collections import Counter

from steel_optimisation_problem import pack, StockInfo, Bin, get_packing_stats


class TestBinWithKerf:
    """Tests for Bin class kerf functionality."""

    def test_bin_with_zero_kerf(self):
        """Bin with zero kerf should behave like original."""
        bin_obj = Bin(capacity=100, kerf_width=0)
        bin_obj.update(30)
        bin_obj.update(40)

        assert bin_obj.currently_used == 70
        assert bin_obj.kerf_loss == 0
        assert bin_obj.total_consumed == 70
        assert bin_obj.waste == 30

    def test_bin_with_kerf(self):
        """Bin should track kerf loss between cuts."""
        bin_obj = Bin(capacity=100, kerf_width=3)
        bin_obj.update(30)  # First cut: no kerf before it
        bin_obj.update(40)  # Second cut: 3mm kerf

        assert bin_obj.currently_used == 70
        assert bin_obj.kerf_loss == 3  # 1 kerf between 2 cuts
        assert bin_obj.total_consumed == 73
        assert bin_obj.waste == 27

    def test_bin_kerf_multiple_items(self):
        """Multiple items should have (n-1) kerfs."""
        bin_obj = Bin(capacity=1000, kerf_width=4)
        for _ in range(5):
            bin_obj.update(100)

        assert bin_obj.currently_used == 500
        assert bin_obj.kerf_loss == 16  # 4 kerfs between 5 cuts
        assert bin_obj.total_consumed == 516
        assert bin_obj.waste == 484

    def test_bin_can_fit_first_item(self):
        """First item should fit if it's <= capacity (no kerf needed)."""
        bin_obj = Bin(capacity=100, kerf_width=5)

        assert bin_obj.can_fit(100) is True
        assert bin_obj.can_fit(101) is False

    def test_bin_can_fit_subsequent_items(self):
        """Subsequent items must account for kerf."""
        bin_obj = Bin(capacity=100, kerf_width=5)
        bin_obj.update(50)

        # Remaining: 100 - 50 = 50, but need 5mm kerf
        # So max item that fits: 50 - 5 = 45
        assert bin_obj.can_fit(45) is True
        assert bin_obj.can_fit(46) is False

    def test_bin_negative_kerf_raises(self):
        """Negative kerf width should raise ValueError."""
        with pytest.raises(ValueError, match="negative"):
            Bin(capacity=100, kerf_width=-1)

    def test_bin_str_with_kerf(self):
        """String representation should include kerf info."""
        bin_obj = Bin(capacity=100, kerf_width=3)
        bin_obj.update(40)
        bin_obj.update(30)

        result = str(bin_obj)
        assert "kerf_loss" in result
        assert "total_consumed" in result
        assert "waste" in result

    def test_bin_str_without_kerf(self):
        """String representation without kerf should be simpler."""
        bin_obj = Bin(capacity=100, kerf_width=0)
        bin_obj.update(40)

        result = str(bin_obj)
        assert "kerf_loss" not in result


class TestPackWithKerf:
    """Tests for pack() function with kerf support."""

    def test_pack_without_kerf_backward_compatible(self):
        """pack() without kerf should work as before."""
        values = [30, 40, 50]
        bins = pack(values, bin_size=100)

        assert len(bins) == 2
        total_items = sum(len(b.items) for b in bins)
        assert total_items == 3

    def test_pack_with_kerf_needs_more_bins(self):
        """Kerf loss may require more bins than without."""
        values = [45, 45]  # Sum = 90, fits in 100 without kerf

        bins_no_kerf = pack(values, bin_size=100, kerf_width=0)
        bins_with_kerf = pack(values, bin_size=100, kerf_width=15)

        # Without kerf: 45 + 45 = 90 <= 100, fits in 1 bin
        assert len(bins_no_kerf) == 1

        # With 15mm kerf: 45 + 15 + 45 = 105 > 100, needs 2 bins
        assert len(bins_with_kerf) == 2

    def test_pack_kerf_realistic_scenario(self):
        """Test realistic scenario: 6m bar, 3mm blade."""
        stock_length = 6000  # 6 meters
        kerf = 3  # 3mm blade

        # Need 5 pieces of 1000mm each
        # Without kerf: 5000mm, fits in 1 bar
        # With kerf: 1000 + 3 + 1000 + 3 + 1000 + 3 + 1000 + 3 + 1000 = 5012mm
        values = [1000] * 5

        bins = pack(values, bin_size=stock_length, kerf_width=kerf)

        assert len(bins) == 1
        assert bins[0].currently_used == 5000
        assert bins[0].kerf_loss == 12  # 4 kerfs
        assert bins[0].total_consumed == 5012

    def test_pack_kerf_forces_split(self):
        """Test case where kerf forces items to different bins."""
        # 3 pieces of 330mm each = 990mm
        # With 10mm kerf: 330 + 10 + 330 + 10 + 330 = 1010mm > 1000mm
        values = [330, 330, 330]

        bins = pack(values, bin_size=1000, kerf_width=10)

        # Should need 2 bins
        assert len(bins) == 2

    def test_pack_preserves_all_items_with_kerf(self):
        """All items should be preserved when using kerf."""
        values = [100, 200, 300, 150, 250]

        bins = pack(values, bin_size=500, kerf_width=5)

        all_items = []
        for b in bins:
            all_items.extend(b.items)

        assert Counter(all_items) == Counter(values)

    def test_pack_negative_kerf_raises(self):
        """Negative kerf should raise ValueError."""
        with pytest.raises(ValueError, match="negative"):
            pack([100], bin_size=200, kerf_width=-1)


class TestGetPackingStats:
    """Tests for get_packing_stats() function."""

    def test_stats_empty_bins(self):
        """Empty bins list should return zero stats."""
        stats = get_packing_stats([])

        assert stats["num_bins"] == 0
        assert stats["efficiency"] == 0.0

    def test_stats_basic(self):
        """Basic stats calculation."""
        bins = pack([100, 200, 300], bin_size=500, kerf_width=0)
        stats = get_packing_stats(bins)

        assert stats["num_bins"] == len(bins)
        assert stats["total_cut_length"] == 600
        assert stats["total_kerf_loss"] == 0

    def test_stats_with_kerf(self):
        """Stats should include kerf loss."""
        bins = pack([100, 100, 100], bin_size=500, kerf_width=10)
        stats = get_packing_stats(bins)

        assert stats["total_cut_length"] == 300
        assert stats["total_kerf_loss"] == 20  # 2 kerfs in one bin


class TestStockInfoWithKerf:
    """Tests for StockInfo with kerf support."""

    def test_stockinfo_programmatic_init(self):
        """StockInfo can be initialized programmatically."""
        stock = StockInfo(stock_length=6000, number_of_stock=10, kerf_width=3)

        assert stock.stock_length == 6000
        assert stock.number_of_stock == 10
        assert stock.kerf_width == 3
        assert stock.total_length == 60000

    def test_stockinfo_default_kerf(self):
        """Default kerf should be 0."""
        stock = StockInfo(stock_length=1000, number_of_stock=5)

        assert stock.kerf_width == 0

    def test_stockinfo_str_includes_kerf(self):
        """String representation should include kerf."""
        stock = StockInfo(stock_length=1000, number_of_stock=5, kerf_width=3)

        result = str(stock)
        assert "kerf_width=3" in result


class TestRealWorldScenarios:
    """Integration tests for real-world cutting scenarios."""

    def test_pipe_cutting_with_kerf(self):
        """Simulate cutting pipes with band saw kerf."""
        # 6m steel tubes, 3.5mm band saw kerf
        stock_length = 6000
        kerf = 3.5

        # Order: need various lengths
        cuts = [
            500, 500, 500, 500,  # 4x 500mm
            750, 750,            # 2x 750mm
            1200, 1200,          # 2x 1200mm
            300, 300, 300,       # 3x 300mm
        ]

        bins = pack(cuts, bin_size=stock_length, kerf_width=kerf)
        stats = get_packing_stats(bins)

        # Verify all items are packed
        all_items = []
        for b in bins:
            all_items.extend(b.items)
        assert Counter(all_items) == Counter(cuts)

        # Verify no bin exceeds capacity
        for b in bins:
            assert b.total_consumed <= b.capacity

        # Print results for manual verification
        print("\nPipe cutting scenario:")
        print(f"  Bins used: {stats['num_bins']}")
        print(f"  Total kerf loss: {stats['total_kerf_loss']}mm")
        print(f"  Efficiency: {stats['efficiency']}%")

    def test_no_kerf_vs_kerf_comparison(self):
        """Compare solutions with and without kerf."""
        cuts = [400] * 10  # 10 pieces of 400mm
        stock_length = 2000

        bins_no_kerf = pack(cuts, bin_size=stock_length, kerf_width=0)
        bins_with_kerf = pack(cuts, bin_size=stock_length, kerf_width=5)

        # Without kerf: 5 pieces fit per bin (5*400=2000 exact fit)
        # 10 pieces / 5 per bin = 2 bins
        # With kerf: 400+5+400+5+400+5+400 = 1615mm (4 pieces, 3 kerfs)
        # Can't fit 5th piece: 1615+5+400=2020 > 2000
        # So 10 pieces / 4 per bin = 3 bins

        stats_no_kerf = get_packing_stats(bins_no_kerf)
        stats_with_kerf = get_packing_stats(bins_with_kerf)

        # Kerf loss requires more bins
        assert stats_no_kerf["num_bins"] == 2
        assert stats_with_kerf["num_bins"] == 3

        # Kerf loss is tracked
        assert stats_with_kerf["total_kerf_loss"] > 0
        assert stats_no_kerf["total_kerf_loss"] == 0
