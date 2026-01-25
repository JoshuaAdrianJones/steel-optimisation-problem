"""Command-line interface for steel cutting optimization.

This module provides an interactive CLI for the steel optimization library.
Run with: python -m steel_optimisation_problem
"""

from .steel_opt import StockInfo, get_packing_stats, pack


def print_section(message: str) -> None:
    """Print a section header with separator line."""
    print("-" * 80)
    print(message)


def main() -> None:
    """Run the interactive steel cutting optimization CLI."""
    print_section("Input starting materials")

    stock_length = int(
        input("Please enter your stock length in mm (e.g., 6000 for 6m bar): ")
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

    cut_lengths: list[int | float] = []
    answer = "y"
    while answer == "y":
        length = int(input("Please enter your cut length in mm: "))
        quantity = int(input("How many do you need? "))
        cut_lengths.extend([length] * quantity)

        print(f"Current total cut length: {sum(cut_lengths)} mm")

        try:
            stock_info.check(cut_lengths)
        except ValueError as e:
            print(f"Warning: {e}")

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


if __name__ == "__main__":
    main()
