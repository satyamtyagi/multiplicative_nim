# Multiplicative Nim Game Analysis

This project provides tools for analyzing the multiplicative Nim game, where players take turns multiplying numbers instead of removing them. The goal is to reach a target product while avoiding certain losing positions.

## Features

- Generates positions for multiplicative Nim analysis
- Identifies reduced non-convertible positions
- Handles prime number arithmetic for target product calculations
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
python3 multiplicative_nim.py --count 3 --max_value 4 --prime 5
```

The script will:
1. Generate all positions
2. Filter positions based on prime number arithmetic
3. Identify non-convertible positions
4. Export results to CSV

## Output

The script generates a CSV file containing the reduced non-convertible positions, which are positions in the game that cannot be converted to a winning position through multiplication.

The CSV files will be named with the format:
- `positions_countX_maxY_primeZ.csv` - All filtered positions
- `non_convertible_positions_countX_maxY_primeZ.csv` - Non-convertible positions
- `reduced_non_convertible_positions_countX_maxY_primeZ.csv` - Reduced non-convertible positions

Where X is the count, Y is the max_value, and Z is the prime number.

## License

MIT License - see LICENSE file for details
