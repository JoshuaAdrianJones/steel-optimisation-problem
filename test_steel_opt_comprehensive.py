"""Comprehensive pytest suite for steel_opt.py.

These tests focus on correctness properties, edge cases, and basic smoke/performance checks.
"""
from collections import Counter
import random
import pytest

from steel_opt import pack, StockInfo


def items_multiset_from_bins(bins):
    items = []
    for b in bins:
        items.extend(b.items)
    return Counter(items)


def test_pack_preserves_items_and_sum():
    values = [5, 15, 20, 20, 30]
    bin_size = 50
    total = sum(values)

    bins = pack(values, bin_size)

    # All items are present the same number of times
    assert items_multiset_from_bins(bins) == Counter(values)

    # Sum preserved
    assert sum(b.currently_used for b in bins) == total

    # No bin exceeds capacity
    assert all(b.currently_used <= b.capacity for b in bins)


@pytest.mark.parametrize(
    "values,bin_size,expected_bins",
    [
        ([10, 20, 20], 60, 1),
        ([50, 40, 30, 20, 10], 60, 4),
        ([20, 20, 20, 20], 40, 4),
    ],
)
def test_pack_parametrized_smoke(values, bin_size, expected_bins):
    bins = pack(values, bin_size)
    assert len(bins) == expected_bins


def test_pack_handles_repeated_and_sorted_inputs():
    values = [3] * 10 + [7] * 5 + [10]
    bin_size = 15
    bins = pack(values, bin_size)

    # every item used exactly as many times as provided
    assert items_multiset_from_bins(bins) == Counter(values)
    assert all(b.currently_used <= b.capacity for b in bins)


def test_stockinfo_check_raises_on_insufficient():
    s = StockInfo.__new__(StockInfo)
    # manually set stock info without invoking interactive ctor
    s.stock_length = 100
    s.number_of_stock = 1
    s.total_length = 100

    # requires more than available
    with pytest.raises(SystemExit):
        s.check([60, 50])


def test_randomized_properties():
    random.seed(0)
    for _ in range(50):
        n = random.randint(1, 12)
        values = [random.randint(1, 50) for _ in range(n)]
        bin_size = random.randint(20, 100)

        # skip trivially invalid cases where a single value > bin_size
        if max(values) > bin_size:
            continue

        bins = pack(values, bin_size)

        # property: all items accounted for
        assert items_multiset_from_bins(bins) == Counter(values)

        # property: no bin exceeds capacity
        assert all(b.currently_used <= b.capacity for b in bins)


def test_performance_smoke():
    # basic smoke test to ensure function handles bigger inputs quickly
    values = [random.randint(1, 100) for _ in range(1000)]
    bin_size = 150
    # avoid invalid inputs for this smoke test
    if max(values) > bin_size:
        values = [v for v in values if v <= bin_size]
    bins = pack(values, bin_size)
    assert items_multiset_from_bins(bins) == Counter(values)
