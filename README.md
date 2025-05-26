# Multiplicative Nim Game Analysis

This project analyzes positions in the multiplicative Nim game, where players take turns multiplying numbers. The goal is to reach a target product while avoiding losing positions.

## Features

- Generates all possible game positions with specified count and max value
- Filters positions based on prime number arithmetic (product % prime = 1)
- Identifies non-convertible positions (can't be converted by reducing one number)
- Identifies reduced non-convertible positions (can't be converted by replacing one number)
- Exports results to multiple CSV files for further analysis
- Provides detailed statistics about position counts

## Requirements

- Python 3.7+
- Numpy >= 1.24.0
- Pandas >= 2.0.0
- Plotly >= 5.17.0

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

The main script is `multiplicative_nim.py`. Run it with positional arguments:
```bash
python3 multiplicative_nim.py COUNT MAX_VALUE PRIME [--output FILENAME] [--verbose]
```

Example:
```bash
python3 multiplicative_nim.py 3 4 5 --verbose
```

The script will:
1. Generate all positions with the specified count and max value
2. Filter positions where product % prime = 1
3. Identify non-convertible positions
4. Identify reduced non-convertible positions
5. Export results to CSV files

## Output

The script generates multiple CSV files:
- `multiplicative_nim_positions.csv` - All generated positions
- `losing_multiplicative_nim_positions.csv` - Positions where product % prime = 1
- `non_convertible_multiplicative_nim_positions.csv` - Non-convertible positions
- `reduced_non_convertible_multiplicative_nim_positions.csv` - Reduced non-convertible positions
- `positions_countX_maxY_primeZ.csv` - All filtered positions
- `non_convertible_positions_countX_maxY_primeZ.csv` - Non-convertible positions
- `reduced_non_convertible_positions_countX_maxY_primeZ.csv` - Reduced non-convertible positions

Where X is the count, Y is the max_value, and Z is the prime number.

## Output Statistics

The script provides detailed statistics about:
- Total number of positions generated
- Number of losing positions
- Number of non-convertible positions
- Number of reduced non-convertible positions
- Number of convertible positions

## License

MIT License - see LICENSE file for details
