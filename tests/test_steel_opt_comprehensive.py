"""Comprehensive pytest suite for steel_opt (updated imports)."""

import random
from collections import Counter

import pytest

from steel_optimisation_problem import StockInfo, pack


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

    assert items_multiset_from_bins(bins) == Counter(values)
    assert sum(b.currently_used for b in bins) == total
    assert all(b.currently_used <= b.capacity for b in bins)


@pytest.mark.parametrize(
    "values,bin_size,expected_bins",
    [
        ([10, 20, 20], 60, 1),
        # True First Fit: [50,40,30,20,10] -> Bin1: 50+10, Bin2: 40+20, Bin3: 30
        ([50, 40, 30, 20, 10], 60, 3),
        # True First Fit allows exact fits: [20,20,20,20] -> Bin1: 20+20, Bin2: 20+20
        ([20, 20, 20, 20], 40, 2),
    ],
)
def test_pack_parametrized_smoke(values, bin_size, expected_bins):
    bins = pack(values, bin_size)
    assert len(bins) == expected_bins


def test_pack_handles_repeated_and_sorted_inputs():
    values = [3] * 10 + [7] * 5 + [10]
    bin_size = 15
    bins = pack(values, bin_size)

    assert items_multiset_from_bins(bins) == Counter(values)
    assert all(b.currently_used <= b.capacity for b in bins)


def test_stockinfo_check_raises_on_insufficient():
    s = StockInfo.__new__(StockInfo)
    s.stock_length = 100
    s.number_of_stock = 1
    s.total_length = 100

    with pytest.raises(SystemExit):
        s.check([60, 50])


def test_randomized_properties():
    random.seed(0)
    for _ in range(50):
        n = random.randint(1, 12)
        values = [random.randint(1, 50) for _ in range(n)]
        bin_size = random.randint(20, 100)

        if max(values) > bin_size:
            continue

        bins = pack(values, bin_size)

        assert items_multiset_from_bins(bins) == Counter(values)
        assert all(b.currently_used <= b.capacity for b in bins)


def test_performance_smoke():
    values = [random.randint(1, 100) for _ in range(1000)]
    bin_size = 150
    if max(values) > bin_size:
        values = [v for v in values if v <= bin_size]
    bins = pack(values, bin_size)
    assert items_multiset_from_bins(bins) == Counter(values)
