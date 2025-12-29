"""Unit tests for steel optimization module (updated imports)."""

import unittest
from unittest.mock import patch
from steel_optimisation_problem import StockInfo, Bin, pack


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
    @patch("builtins.input", side_effect=["1000", "5"])
    def test_valid_input(self, mock_input):
        stock_info = StockInfo()
        self.assertEqual(stock_info.stock_length, 1000)
        self.assertEqual(stock_info.number_of_stock, 5)
        self.assertEqual(stock_info.total_length, 5000)

    @patch("builtins.input", side_effect=["abc", "5"])
    def test_invalid_input_stock_length(self, mock_input):
        with self.assertRaises(ValueError):
            StockInfo()

    @patch("builtins.input", side_effect=["1000", "abc"])
    def test_invalid_input_number_of_stock(self, mock_input):
        with self.assertRaises(ValueError):
            StockInfo()

    @patch("builtins.input", side_effect=["0", "5"])
    def test_edge_case_zero_stock_length(self, mock_input):
        stock_info = StockInfo()
        self.assertEqual(stock_info.stock_length, 0)
        self.assertEqual(stock_info.number_of_stock, 5)
        self.assertEqual(stock_info.total_length, 0)

    @patch("builtins.input", side_effect=["1000", "0"])
    def test_edge_case_zero_number_of_stock(self, mock_input):
        stock_info = StockInfo()
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
        self.assertEqual(len(bins), 4)
        self.assertEqual(bins[0].currently_used, 50)
        self.assertEqual(bins[1].currently_used, 40)

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
