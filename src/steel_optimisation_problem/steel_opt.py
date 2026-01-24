"""Steel optimization module (packaged under src layout).

This file was moved into a package so the project follows a modern
`src/` layout. The original implementation is preserved.
"""

from typing import List, Union

# Type alias for numeric values (int or float for kerf precision)
Numeric = Union[int, float]


class Bin:
    """Container for items that tracks used stock capacity including kerf loss.

    Attributes:
        capacity: Maximum capacity of the bin.
        items: List of items (cut lengths) in the bin.
        kerf_width: Width of material lost per cut (blade thickness).
        currently_used: Total length currently used (items only, excludes kerf).
        total_consumed: Total material consumed including kerf loss.
        kerf_loss: Total kerf loss in this bin.
        waste: Remaining unused capacity after accounting for kerf.
    """

    def __init__(self, capacity: Numeric, kerf_width: Numeric = 0) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        if kerf_width < 0:
            raise ValueError("Kerf width cannot be negative")
        self.capacity = capacity
        self.kerf_width = kerf_width
        self.items: List[Numeric] = []
        self.currently_used: Numeric = 0
        self.kerf_loss: Numeric = 0
        self.total_consumed: Numeric = 0
        self.waste: Numeric = capacity

    def can_fit(self, item: Numeric) -> bool:
        """Check if an item can fit in this bin accounting for kerf.

        When adding an item to a bin that already has items, we need one
        additional kerf cut between the existing items and the new item.
        """
        if not self.items:
            # First item: no kerf needed before it
            return item <= self.capacity
        else:
            # Additional items need kerf between them
            return self.total_consumed + self.kerf_width + item <= self.capacity

    def update(self, item: Numeric) -> None:
        """Add an item to the bin and recalculate totals."""
        self.items.append(item)
        self.currently_used = sum(self.items)
        self.kerf_loss = self.kerf_width * max(0, len(self.items) - 1)
        self.total_consumed = self.currently_used + self.kerf_loss
        self.waste = self.capacity - self.total_consumed

    def __str__(self) -> str:
        if self.kerf_width > 0:
            return (
                f"Bin(capacity={self.capacity}, cuts={self.items}, "
                f"used={self.currently_used}, kerf_loss={self.kerf_loss}, "
                f"total_consumed={self.total_consumed}, waste={self.waste})"
            )
        return (
            f"Bin(capacity={self.capacity}, currently_used={self.currently_used}, "
            f"cuts={self.items})"
        )


class StockInfo:
    """Manages stock information and validates available stock.

    Can be initialized programmatically or interactively.

    Args:
        stock_length: Length of each stock piece in mm. If None, prompts user.
        number_of_stock: Number of stock pieces available. If None, prompts user.
        kerf_width: Blade/saw kerf width in mm. Default 0.

    Example:
        >>> # Programmatic usage
        >>> stock = StockInfo(stock_length=6000, number_of_stock=10, kerf_width=3)

        >>> # Interactive usage (prompts user)
        >>> stock = StockInfo()
    """

    def __init__(
        self,
        stock_length: Numeric = None,
        number_of_stock: int = None,
        kerf_width: Numeric = 0,
    ) -> None:
        if stock_length is None:
            self.stock_length = int(
                input(
                    "Please enter your stock length in mm:  (for example you might "
                    "purchase 1m tubes in which case enter 1000): "
                )
            )
        else:
            self.stock_length = stock_length

        if number_of_stock is None:
            self.number_of_stock = int(input("How many do you have? "))
        else:
            self.number_of_stock = number_of_stock

        self.kerf_width = kerf_width
        self.total_length = self.stock_length * self.number_of_stock

        # Only print when running interactively
        if stock_length is None or number_of_stock is None:
            print(f"Stock Length is: {self.stock_length}")
            print(f"Total Stock Length is: {self.total_length}")
            if kerf_width > 0:
                print(f"Kerf Width: {self.kerf_width}mm")

    def check(self, cut_list: List[Numeric]) -> None:
        """Validate that total cuts don't exceed available stock."""
        if sum(cut_list) > self.total_length:
            print("Not enough stock.")
            raise SystemExit("Insufficient stock for requested cuts")

    def __str__(self) -> str:
        return (
            f"StockInfo(stock_length={self.stock_length}, "
            f"number_of_stock={self.number_of_stock}, "
            f"total_length={self.total_length}, "
            f"kerf_width={self.kerf_width})"
        )


def pack(
    values: List[Numeric], bin_size: Numeric, kerf_width: Numeric = 0
) -> List[Bin]:
    """Pack values into bins using First Fit Decreasing algorithm.

    This algorithm sorts items by size (largest first) and places each item
    in the first bin where it fits. This greedy approach typically achieves
    solutions within 11/9 * OPT + 6/9 of optimal.

    Args:
        values: List of cut lengths needed.
        bin_size: Capacity of each stock piece (e.g., 6000mm for 6m bar).
        kerf_width: Width of material lost per cut due to blade thickness.
            Common values: 3-4mm for band saws, 2-3mm for cold saws.
            Default is 0 (no kerf loss).

    Returns:
        List of Bin objects containing the packed items.

    Raises:
        ValueError: If values list is empty, bin_size is too small for any item,
            or kerf_width is negative.

    Example:
        >>> # Without kerf
        >>> bins = pack([500, 600, 700], bin_size=2000)
        >>> len(bins)
        1

        >>> # With 3mm kerf (more realistic)
        >>> bins = pack([500, 600, 700], bin_size=2000, kerf_width=3)
        >>> bins[0].kerf_loss  # 2 cuts between 3 pieces = 6mm kerf
        6
    """
    if not values:
        raise ValueError("Values list cannot be empty")
    if kerf_width < 0:
        raise ValueError("Kerf width cannot be negative")
    if max(values) > bin_size:
        raise ValueError("bin_size too small")

    bins: List[Bin] = []
    cuts = sorted(values, reverse=True)
    # create first bin
    bins.append(Bin(capacity=bin_size, kerf_width=kerf_width))

    for cut in cuts:
        # Try to fit in existing bins (First Fit)
        placed = False
        for existing_bin in bins:
            if existing_bin.can_fit(cut):
                existing_bin.update(cut)
                placed = True
                break

        # If no existing bin can fit, create a new one
        if not placed:
            new_bin = Bin(capacity=bin_size, kerf_width=kerf_width)
            new_bin.update(cut)
            bins.append(new_bin)

    return bins


def get_packing_stats(bins: List[Bin]) -> dict:
    """Calculate statistics for a packing solution.

    Args:
        bins: List of Bin objects from pack().

    Returns:
        Dictionary with statistics:
            - num_bins: Number of stock pieces used
            - total_capacity: Total available material
            - total_cut_length: Sum of all cut lengths
            - total_kerf_loss: Total material lost to kerf
            - total_consumed: Cut lengths + kerf loss
            - total_waste: Unused material (offcuts)
            - efficiency: Percentage of material used for cuts
    """
    if not bins:
        return {
            "num_bins": 0,
            "total_capacity": 0,
            "total_cut_length": 0,
            "total_kerf_loss": 0,
            "total_consumed": 0,
            "total_waste": 0,
            "efficiency": 0.0,
        }

    total_capacity = sum(b.capacity for b in bins)
    total_cut_length = sum(b.currently_used for b in bins)
    total_kerf_loss = sum(b.kerf_loss for b in bins)
    total_consumed = sum(b.total_consumed for b in bins)
    total_waste = sum(b.waste for b in bins)

    # Efficiency is the ratio of useful cut material to total material used
    efficiency = (total_cut_length / total_capacity * 100) if total_capacity > 0 else 0

    return {
        "num_bins": len(bins),
        "total_capacity": total_capacity,
        "total_cut_length": total_cut_length,
        "total_kerf_loss": total_kerf_loss,
        "total_consumed": total_consumed,
        "total_waste": total_waste,
        "efficiency": round(efficiency, 2),
    }


def print_section(message: str) -> None:
    print("-" * 80)
    print(message)


if __name__ == "__main__":
    print_section("Input starting materials")

    stock_length = int(
        input(
            "Please enter your stock length in mm (e.g., 6000 for 6m bar): "
        )
    )
    number_of_stock = int(input("How many stock pieces do you have? "))

    kerf_input = input(
        "Enter kerf/blade width in mm (press Enter for 0, typical: 3-4mm): "
    )
    kerf_width = float(kerf_input) if kerf_input.strip() else 0

    stock_info = StockInfo(
        stock_length=stock_length,
        number_of_stock=number_of_stock,
        kerf_width=kerf_width,
    )
    print(stock_info)

    print_section("Input cut list")

    cut_lengths: List[Numeric] = []
    answer = "y"
    while answer == "y":
        length = int(input("Please enter your cut length in mm: "))
        quantity = int(input("How many do you need? "))
        cut_lengths.extend([length] * quantity)

        print(f"Current total cut length: {sum(cut_lengths)} mm")

        stock_info.check(cut_lengths)
        answer = input("Do you have more cuts to add? (y/n): ").lower()

    print_section("Optimization Results")

    cut_lengths.sort()
    print(f"Cut list: {cut_lengths}")
    print(stock_info)

    total_cut_length = sum(cut_lengths)
    min_bins_needed = (
        total_cut_length + stock_info.stock_length - 1
    ) // stock_info.stock_length
    print(f"Minimum bins needed (ignoring kerf): {min_bins_needed}")

    bins = pack(cut_lengths, stock_info.stock_length, kerf_width=kerf_width)
    stats = get_packing_stats(bins)

    print(f"\nSolution using {stats['num_bins']} stock pieces:")
    print("-" * 40)
    for i, bin_obj in enumerate(bins, 1):
        print(f"Stock #{i}: {bin_obj}")

    print("-" * 40)
    print(f"Total cut length requested: {stats['total_cut_length']} mm")
    if kerf_width > 0:
        print(f"Total kerf loss: {stats['total_kerf_loss']} mm")
        print(f"Total material consumed: {stats['total_consumed']} mm")
    print(f"Total waste (offcuts): {stats['total_waste']} mm")
    print(f"Material efficiency: {stats['efficiency']}%")
