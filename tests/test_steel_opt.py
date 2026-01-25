"""Unit tests for steel optimization module (updated imports)."""

import unittest

from steel_optimisation_problem import Bin, StockInfo, pack


class TestBinInit(unittest.TestCase):
    def test_valid_capacity(self):
        bin_obj = Bin(10)
        self.assertEqual(bin_obj.capacity, 10)
        self.assertEqual(bin_obj.items, [])
        self.assertEqual(bin_obj.currently_used, 0)

    def test_zero_capacity(self):
        with self.assertRaises(ValueError):
            Bin(0)

    def test_negative_capacity(self):
        with self.assertRaises(ValueError):
            Bin(-1)


class TestStockInfoInit(unittest.TestCase):
    def test_valid_input(self):
        stock_info = StockInfo(stock_length=1000, number_of_stock=5)
        self.assertEqual(stock_info.stock_length, 1000)
        self.assertEqual(stock_info.number_of_stock, 5)
        self.assertEqual(stock_info.total_length, 5000)

    def test_valid_input_with_kerf(self):
        stock_info = StockInfo(stock_length=6000, number_of_stock=10, kerf_width=3.5)
        self.assertEqual(stock_info.kerf_width, 3.5)
        self.assertEqual(stock_info.total_length, 60000)

    def test_invalid_stock_length_zero(self):
        with self.assertRaises(ValueError):
            StockInfo(stock_length=0, number_of_stock=5)

    def test_invalid_stock_length_negative(self):
        with self.assertRaises(ValueError):
            StockInfo(stock_length=-100, number_of_stock=5)

    def test_invalid_number_of_stock_negative(self):
        with self.assertRaises(ValueError):
            StockInfo(stock_length=1000, number_of_stock=-1)

    def test_edge_case_zero_number_of_stock(self):
        stock_info = StockInfo(stock_length=1000, number_of_stock=0)
        self.assertEqual(stock_info.stock_length, 1000)
        self.assertEqual(stock_info.number_of_stock, 0)
        self.assertEqual(stock_info.total_length, 0)


class TestPackFunction(unittest.TestCase):
    def test_single_bin(self):
        values = [10, 20, 20]
        bin_size = 60
        bins = pack(values, bin_size)
        self.assertEqual(len(bins), 1)
        self.assertEqual(bins[0].currently_used, 50)

    def test_multiple_bins(self):
        values = [10, 20, 30, 40, 50]
        bin_size = 60
        bins = pack(values, bin_size)
        # True First Fit Decreasing: sorted [50,40,30,20,10]
        # Bin1: 50+10=60, Bin2: 40+20=60, Bin3: 30 -> 3 bins total
        self.assertEqual(len(bins), 3)
        self.assertEqual(bins[0].currently_used, 60)  # 50+10
        self.assertEqual(bins[1].currently_used, 60)  # 40+20

    def test_values_exceed_bin_size(self):
        values = [10, 20, 30, 100]
        bin_size = 60
        with self.assertRaises(ValueError):
            pack(values, bin_size)

    def test_empty_list(self):
        values = []
        bin_size = 60
        with self.assertRaises(ValueError):
            pack(values, bin_size)


if __name__ == "__main__":
    unittest.main()
