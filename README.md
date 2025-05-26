# Multiplicative Nim Game Analysis

This project provides tools for analyzing the multiplicative Nim game, where players take turns multiplying numbers instead of removing them. The goal is to reach a target product while avoiding certain losing positions.

## Features

- Generates combinations of numbers for multiplicative Nim analysis
- Identifies reduced non-convertible combinations
- Handles modular arithmetic for target product calculations
- Exports results to CSV files for further analysis

## Requirements

- Python 3.7+
- Numpy
- Pandas
- Plotly

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip3 install -r requirements.txt
```

## Usage

The main script is `multiplicative_nim.py`. Run it with:
```bash
python3 multiplicative_nim.py --count 3 --max_value 4 --mod 5
```

The script will:
1. Generate all combinations of numbers
2. Filter combinations based on modular arithmetic
3. Identify non-convertible combinations
4. Export results to CSV

## Output

The script generates a CSV file containing the reduced non-convertible combinations, which are positions in the game that cannot be converted to a winning position through multiplication.

## License

MIT License - see LICENSE file for details
