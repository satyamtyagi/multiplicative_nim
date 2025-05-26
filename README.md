# Multiplicative Nim Game Analysis

This project analyzes positions in the Multiplicative Nim game, which has two types of moves:
1. Subtract from a single pile (like traditional Nim)
2. Reduce the product of all piles by a factor, where the reduction cannot exceed a specified prime number

The goal is to force your opponent into a losing position where they cannot make a valid move.

## Features

- Generates all possible game positions with specified count and max value
- Filters positions based on prime number arithmetic (product % prime = 1)
- Identifies non-convertible positions (can't be converted by reducing one number)
- Identifies reduced non-convertible positions (can't be converted by replacing one number with another while maintaining product reduction)
- Analyzes positions that cannot be converted to winning positions through either move type
- Exports results to multiple CSV files for further analysis
- Provides detailed statistics about position counts

## Game Rules

1. Players take turns making moves
2. Each move must be one of two types:
   - Subtract any positive amount from a single pile
   - Reduce the product of all piles by a factor, where the reduction cannot exceed the specified prime number
3. A position is losing if:
   - The product of all piles is congruent to 1 modulo the prime number
   - The position cannot be converted to a winning position through either move type

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

Where:
- COUNT: Number of piles in the game
- MAX_VALUE: Maximum value that can be in any pile
- PRIME: Prime number that limits the product reduction factor

The script will:
1. Generate all valid positions with the specified count and max value
2. Filter positions where product % prime = 1 (losing positions)
3. Identify non-convertible positions (can't be converted by reducing one number)
4. Identify reduced non-convertible positions (can't be converted by replacing one number while maintaining product reduction)
5. Export results to CSV files

## Output

The script generates multiple CSV files:
- `multiplicative_nim_positions.csv` - All generated positions
- `losing_multiplicative_nim_positions.csv` - Positions where product % prime = 1
- `non_convertible_multiplicative_nim_positions.csv` - Positions that can't be converted by reducing one number
- `reduced_non_convertible_multiplicative_nim_positions.csv` - Positions that can't be converted by replacing one number while maintaining product reduction
- `positions_countX_maxY_primeZ.csv` - All filtered positions
- `non_convertible_positions_countX_maxY_primeZ.csv` - Non-convertible positions
- `reduced_non_convertible_positions_countX_maxY_primeZ.csv` - Reduced non-convertible positions

Where X is the count, Y is the max_value, and Z is the prime number.

## Output Statistics

The script provides detailed statistics about:
- Total number of positions generated
- Number of losing positions (product % prime = 1)
- Number of non-convertible positions (can't be converted by reducing one number)
- Number of reduced non-convertible positions (can't be converted by replacing one number while maintaining product reduction)
- Number of convertible positions (can be converted to winning positions)

## Analysis Details

The script performs the following analysis:
1. Generates all valid positions with the given count and max value
2. Filters out positions where the product is congruent to 1 modulo the prime number (losing positions)
3. Identifies positions that cannot be converted to winning positions by:
   - Reducing any single number
   - Replacing any number with another while maintaining the product reduction constraint
4. Provides detailed information about each type of position and its characteristics

## License

MIT License - see LICENSE file for details
