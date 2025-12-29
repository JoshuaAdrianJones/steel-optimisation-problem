"""Steel optimization module (packaged under src layout).

This file was moved into a package so the project follows a modern
`src/` layout. The original implementation is preserved.
"""

from typing import List


class Bin:
    """Container for items that tracks used stock capacity.

    Attributes:
        capacity: Maximum capacity of the bin.
        items: List of items in the bin.
        currently_used: Total length currently used in the bin.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.items: List[int] = []
        self.currently_used = 0

    def update(self, item: int) -> None:
        self.items.append(item)
        self.currently_used = sum(self.items)

    def __str__(self) -> str:
        return (
            f"Bin(capacity={self.capacity}, currently_used={self.currently_used}, "
            f"cuts={self.items})"
        )


class StockInfo:
    """Manages stock information and validates available stock."""

    def __init__(self) -> None:
        self.stock_length = int(
            input(
                "Please enter your stock length in mm:  (for example you might purchase "
                "1m tubes in which case enter 1000): "
            )
        )
        self.number_of_stock = int(input("How many do you have? "))
        self.total_length = self.stock_length * self.number_of_stock
        print(f"Stock Length is: {self.stock_length}")
        print(f"Total Stock Length is: {self.total_length}")

    def check(self, cut_list: List[int]) -> None:
        if sum(cut_list) > self.total_length:
            print("Not enough stock.")
            raise SystemExit("Insufficient stock for requested cuts")

    def __str__(self) -> str:
        return (
            f"StockInfo(stock_length={self.stock_length}, "
            f"number_of_stock={self.number_of_stock}, "
            f"total_length={self.total_length})"
        )


def pack(values: List[int], bin_size: int) -> List[Bin]:
    """Pack values into bins using First Fit Decreasing algorithm."""
    if not values:
        raise ValueError("Values list cannot be empty")
    if max(values) > bin_size:
        raise ValueError("bin_size too small")

    bins: List[Bin] = []
    cuts = sorted(values, reverse=True)
    # create first bin
    bins.append(Bin(capacity=bin_size))

    for cut in cuts:
        current_bin = bins[-1]
        if current_bin.currently_used + cut < current_bin.capacity:
            current_bin.update(cut)
        else:
            new_bin = Bin(capacity=bin_size)
            new_bin.update(cut)
            bins.append(new_bin)

    return bins


def print_section(message: str) -> None:
    print("-" * 80)
    print(message)


if __name__ == "__main__":
    print_section("Input starting materials")

    stock_info = StockInfo()

    print_section("Input cut list")

    cut_lengths: List[int] = []
    answer = "y"
    while answer == "y":
        length = int(input("Please enter your cut length in mm: "))
        quantity = int(input("How many do you have? "))
        cut_lengths.extend([length] * quantity)

        print(f"Current Length is: {sum(cut_lengths)} mm")

        stock_info.check(cut_lengths)
        answer = input("do you have more to add? y/n?: ")

    cut_lengths.sort()
    print(cut_lengths)
    print(stock_info)
    total_cut_length = sum(cut_lengths)
    min_bins_needed = (total_cut_length + stock_info.stock_length - 1) // stock_info.stock_length
    print(
        f"List with sum {total_cut_length} requires at least {min_bins_needed} bins"
    )
    bins = pack(cut_lengths, stock_info.stock_length)

    print(f"Solution using {len(bins)} bins:")
    for bin_obj in bins:
        print(bin_obj)
    print(f"total length requested: {total_cut_length}")
    print(f"total length used: {sum(bin_obj.currently_used for bin_obj in bins)}")
