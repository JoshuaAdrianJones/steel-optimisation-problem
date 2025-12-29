"""Steel optimization program.

An optimization program to determine the number of steel stock
lengths needed to cut from stock efficiently.
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
        """Initialize a bin with given capacity.

        Args:
            capacity: Maximum capacity of the bin (must be positive).

        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.items: List[int] = []
        self.currently_used = 0

    def update(self, item: int) -> None:
        """Add an item to the bin and update used capacity.

        Args:
            item: The item (length) to add to the bin.
        """
        self.items.append(item)
        self.currently_used = sum(self.items)

    def __str__(self) -> str:
        """Return a string representation of the bin."""
        return (
            f"Bin(capacity={self.capacity}, currently_used={self.currently_used}, "
            f"cuts={self.items})"
        )


class StockInfo:
    """Manages stock information and validates available stock.

    Attributes:
        stock_length: Length of each stock piece in mm.
        number_of_stock: Number of stock pieces available.
        total_length: Total available stock length in mm.
    """

    def __init__(self) -> None:
        """Initialize stock info by prompting user for input."""
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
        """Check if cut list exceeds available stock.

        Args:
            cut_list: List of cut lengths to verify.

        Raises:
            SystemExit: If total cut length exceeds available stock.
        """
        if sum(cut_list) > self.total_length:
            print("Not enough stock.")
            raise SystemExit("Insufficient stock for requested cuts")

    def __str__(self) -> str:
        """Return a string representation of stock info."""
        return (
            f"StockInfo(stock_length={self.stock_length}, "
            f"number_of_stock={self.number_of_stock}, "
            f"total_length={self.total_length})"
        )


def pack(values: List[int], bin_size: int) -> List[Bin]:
    """Pack values into bins using First Fit Decreasing algorithm.

    Pack a list of values into bins where the sum of the values in each bin
    does not exceed bin_size. The algorithm used is First Fit Decreasing,
    described at https://www.ams.org/publicoutreach/feature-column/fcarc-bins2

    Args:
        values: List of lengths to pack.
        bin_size: Maximum capacity of each bin.

    Returns:
        List of Bin objects containing packed items.

    Raises:
        ValueError: If any value exceeds bin_size or values list is empty.
    """
    if not values:
        raise ValueError("Values list cannot be empty")
    if max(values) > bin_size:
        raise ValueError("bin_size too small")

    bins: List[Bin] = []
    cuts = sorted(values, reverse=True)
    print("cuts", cuts)
    # create first bin
    bins.append(Bin(capacity=bin_size))

    for cut in cuts:
        current_bin = bins[-1]
        # Try to fit item into a bin
        print(f"currently used = {current_bin.currently_used} cut = {cut}")
        if current_bin.currently_used + cut < current_bin.capacity:
            current_bin.update(cut)
        else:
            print("bin full")
            new_bin = Bin(capacity=bin_size)
            new_bin.update(cut)
            print("new bin", new_bin)
            bins.append(new_bin)

    return bins


def print_section(message: str) -> None:
    """Print a formatted section header.

    Args:
        message: The section title to display.
    """
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
