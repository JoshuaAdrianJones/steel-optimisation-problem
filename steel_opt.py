"""Steel_opt.py
An optimisation program to determine the number of steel stock
lengths to use for a steel structure cut from stock
"""


class Bin(object):
    """Container for items that keeps a running sum of how much of the stock has been used"""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError()
        self.capacity = capacity
        self.items = []
        self.currently_used = 0

    def update(self, item):
        self.items.append(item)
        self.currently_used = sum(self.items)

    def __str__(self):
        """Printable representation"""
        return f"Bin(capacity={self.capacity}, currently_used={self.currently_used}, cuts={self.items})"


class StockInfo:
    def __init__(self):
        self.stock_length = int(
            input(
                "Please enter your stock length in mm:  (for example you might purchase 1m tubes in which case enter 1000): "
            )
        )
        self.number_of_stock = int(input("How many do you have? "))
        self.total_length = self.stock_length * self.number_of_stock
        print(f"Stock Length is: {self.stock_length}")
        print(f"Total Stock Length is: {self.total_length}")

    def check(self, cut_list):
        if sum(cut_list) > self.total_length:
            print("Not enough stock.")
            quit()

    def __str__(self):
        """Printable representation"""
        return "StockInfo(stock_length=%d, number_of_stock=%d, total_length=%d)" % (
            self.stock_length,
            self.number_of_stock,
            self.total_length,
        )


def pack(values, bin_size):
    """
    Pack a list of values into bins where the sum of the values in each bin
    does not exceed bin_size.

    The algorithm used is First Fit Decreasing, described at
    https://www.ams.org/publicoutreach/feature-column/fcarc-bins2
    """
    if max(values) > bin_size:
        raise ValueError("bin_size too small")
    if len(values) == 0:
        raise ValueError("no values")
    bins = []
    cuts = sorted(values, reverse=True)
    print("cuts", cuts)
    # create first bin
    bins.append(Bin(capacity=bin_size))

    # iterate over cuts and place in bins
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


def new_section(message):
    print("-" * 80)
    print(message)


if __name__ == "__main__":
    # get input for bin sizes and total number of bins
    new_section("Input starting materials")

    stock_info = StockInfo()

    new_section("Input cut list")

    cut_lengths = []
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
    print(
        "List with sum",
        sum(cut_lengths),
        "requires at least",
        (sum(cut_lengths) + stock_info.stock_length - 1) / stock_info.stock_length,
        "bins",
    )
    bins = pack(cut_lengths, stock_info.stock_length)

    print("Solution using", len(bins), "bins:")
    for bin in bins:
        print(bin)
    print("total length requested:", sum(cut_lengths))
    print("total length used:", sum([bin.currently_used for bin in bins]))
