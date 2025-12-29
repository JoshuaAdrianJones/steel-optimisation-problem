
# steel-optimisation-problem

[![Python Versions](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

One-sentence: library for solving a 1D bin-packing problem focused on optimising how many fixed-length steel tubes to buy and how to cut them to satisfy a set of required lengths.

Why this exists
----------------
When you need to cut parts from fixed-length stock (steel tubes, bars, or similar), it’s useful to minimise wasted material and the number of stock pieces purchased. This project provides simple algorithms and helpers to explore packing strategies for that problem.

Installation
------------
Install from source for development:

```bash
pip install -e .
```

Quick start
-----------
```python
from steel_optimisation_problem import pack, StockInfo

# stock length 2000mm, want 3x500mm and 2x600mm
stock = StockInfo(length=2000)
items = [500,500,500,600,600]
result = pack(items, stock)
print(result)
```

Running tests
-------------
Run the test suite locally (ensure `src` is on `PYTHONPATH` or install the package):

```bash
# from repository root
PYTHONPATH=src pytest -q
```

Contributing
------------
See CONTRIBUTING.md for how to set up a development environment, run tests, and submit PRs.

License
-------
MIT
