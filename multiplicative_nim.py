"""
Multiplicative Nim Analysis

This module provides functions for analyzing multiplicative Nim games.
"""

import csv
import argparse
import sys
import numpy as np
from typing import List, Tuple, Optional

def count_positions(n: int, m: int) -> int:
    """
    Calculate the total number of positions of length n with elements from 1 to m.
    Uses the combinatorial formula for positions with repetition:
    C(n + m - 1, m - 1) = (n + m - 1)! / (n! * (m - 1)!)
    
    Args:
        n: Length of each combination
        m: Maximum value for each element (1 to m)
        
    Returns:
        Total number of positions
        
    Raises:
        ValueError: If n or m are not positive integers
    """
    if n <= 0 or m <= 0:
        raise ValueError("n and m must be positive integers")
    
    return comb(n + m - 1, m - 1)

def generate_positions(count: int, max_value: int, prime: int) -> List[Tuple[int, ...]]:
    """
    Generate all positions of length count with elements from 1 to max_value,
    excluding multiples of prime.
    This function generates positions WITH repetition, ensuring:
    - Each tuple is sorted in non-decreasing order
    - Order doesn't matter (no permutations)
    
    Args:
        count: Number of elements in each position
        max_value: Maximum value for each element (1 to max_value)
        prime: Prime number for filtering
        
    Returns:
        List of all positions (with repetition allowed)
        
    Raises:
        ValueError: If count, max_value, or prime are not positive integers
    """
    if count <= 0 or max_value <= 0 or prime <= 0:
        raise ValueError("count, max_value, and prime must be positive integers")
    
    # Generate valid numbers excluding multiples of prime
    valid_numbers = [i for i in range(1, max_value + 1) if i % prime != 0]
    
    if count == 1:
        return [(i,) for i in valid_numbers]
    
    # Recursive approach allowing repeats
    result = []
    for i in valid_numbers:
        # Generate all (count-1)-tuples with values from i to max_value
        # This ensures that each tuple is sorted
        smaller_tuples = generate_positions(count - 1, max_value, prime)
        # Add current value i to each smaller tuple
        for t in smaller_tuples:
            if t[0] >= i:
                result.append((i,) + t)
    
    return result

def filter_by_prime(positions: List[Tuple[int, ...]], prime: int) -> List[Tuple[int, ...]]:
    """
    Filter positions where the product of elements is congruent to 1 modulo prime.
    
    Args:
        positions: List of tuples to filter
        prime: Prime number for filtering
        
    Returns:
        List of losing positions
        
    Raises:
        ValueError: If prime is not a positive integer
    """
    if prime <= 0:
        raise ValueError("prime must be a positive integer")
    
    return [position for position in positions if np.prod(position) % prime == 1 and not any(x % prime == 0 for x in position)]

def find_non_convertible(positions: List[Tuple[int, ...]], prime: int, max_value: int) -> List[Tuple[int, ...]]:
    """
    Find positions that cannot be converted to satisfy the prime condition.
    A position is non-convertible if reducing any number cannot make its product congruent to 1 modulo prime.
    
    Args:
        positions: List of tuples to analyze
        prime: Prime number for checking conversion
        max_value: Maximum value for each element
        
    Returns:
        List of non-convertible positions
        
    Raises:
        ValueError: If prime or max_value are not positive integers
    """
    if prime <= 0 or max_value <= 0:
        raise ValueError("prime and max_value must be positive integers")
    
    non_convertible = []
    
    for position in positions:
        # Skip if already satisfies prime condition
        if np.prod(position) % prime == 1:
            continue
            
        # Try reducing each number by amounts between 1 and prime-1
        can_convert = False
        for i in range(len(position)):
            # Try reductions between 1 and prime-1
            for reduction in range(1, min(position[i], prime)):
                reduced = list(position)
                reduced[i] -= reduction
                
                # Ensure the reduced number is still valid (not a multiple of prime)
                if reduced[i] % prime == 0 or reduced[i] > max_value:
                    continue
                
                reduced_tuple = tuple(sorted(reduced))  # Keep sorted for consistency
                
                # Check if the reduced combination satisfies prime condition
                if np.prod(reduced_tuple) % prime == 1:
                    can_convert = True
                    break
            if can_convert:
                break
        
        # If no reduction could make it satisfy prime condition, it's non-convertible
        if not can_convert:
            non_convertible.append(position)
    
    return non_convertible

def find_reduced_non_convertible(non_convertible: List[Tuple[int, ...]], all_positions: List[Tuple[int, ...]], prime: int, max_value: int, count: int) -> List[Tuple[int, ...]]:
    """
    Find positions that cannot be converted to satisfy the prime condition even after
    replacing any number of numbers with other valid numbers while maintaining product reduction.
    
    Args:
        non_convertible: List of non-convertible positions
        all_positions: List of all valid positions
        prime: Prime number for checking conversion
        max_value: Maximum value for each element
        count: Number of elements in each position
        
    Returns:
        List of reduced non-convertible positions
        
    Raises:
        ValueError: If prime, max_value, or count are not positive integers
    """
    if prime <= 0 or max_value <= 0 or count <= 0:
        raise ValueError("prime, max_value, and count must be positive integers")
    
    reduced_non_convertible = []
    
    # Generate valid positions without multiples of prime
    valid_positions = generate_positions(count, max_value, prime)
    
    # Get losing positions from valid positions
    losing_positions = filter_by_prime(valid_positions, prime)
    
    for position in non_convertible:
        # Calculate the original product
        original_product = np.prod(position)
        
        # Calculate the target product
        m = original_product % prime
        target_product = original_product - m + 1
        
        # Check if any losing position has the target product
        can_convert = False
        for losing_position in losing_positions:
            if np.prod(losing_position) == target_product:
                can_convert = True
                break
        
        if not can_convert:
            reduced_non_convertible.append(position)
    
    return reduced_non_convertible

def export_to_csv(positions: List[Tuple[int, ...]], filename: str) -> None:
    """
    Export positions to a CSV file.
    
    Args:
        positions: List of tuples to export
        filename: Name of the output CSV file
        
    Raises:
        ValueError: If positions list is empty
    """
    if not positions:
        raise ValueError("positions list cannot be empty")
    
    # Create header based on tuple length
    header = [f"value{i+1}" for i in range(len(positions[0]))]
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(positions)
        print(f"Combinations have been saved to {filename}")
    except Exception as e:
        raise RuntimeError(f"Failed to write to CSV file: {e}") from e

def main():
    """
    Main entry point for the multiplicative Nim analysis tool.
    
    Parses command line arguments and performs the analysis.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Analyze multiplicative Nim games',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'count',
        type=int,
        help='Number of elements in each position'
    )
    parser.add_argument(
        'max_value',
        type=int,
        help='Maximum value for each element'
    )
    parser.add_argument(
        'prime',
        type=int,
        help='Prime number for filtering'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output CSV file name',
        default='multiplicative_nim_positions.csv'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    args = parser.parse_args()

    # Validate input parameters
    if args.count <= 0 or args.max_value <= 0 or args.prime <= 0:
        parser.error("count, max_value, and prime must be positive integers")

    # Generate all positions
    try:
        print(f"Generating positions with count={args.count}, max_value={args.max_value}, prime={args.prime}...")
        positions = generate_positions(args.count, args.max_value, args.prime)
        print(f"Generated {len(positions)} positions")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Find losing positions
    losing_positions = filter_by_prime(positions, args.prime)
    print(f"Found {len(losing_positions)} losing positions")

    # Find non-convertible positions
    non_convertible = find_non_convertible(positions, args.prime, args.max_value)
    print(f"Found {len(non_convertible)} non-convertible positions")

    # Find reduced non-convertible positions
    reduced_non_convertible = find_reduced_non_convertible(
        non_convertible, positions, args.prime, args.max_value, args.count
    )
    print(f"Found {len(reduced_non_convertible)} reduced non-convertible positions")

    # Export results to CSV if requested
    if args.output:
        try:
            export_to_csv(positions, args.output)
            if args.verbose:
                print(f"Exporting specialized results...")
                if losing_positions:
                    export_to_csv(losing_positions, f"losing_{args.output}")
                if non_convertible:
                    export_to_csv(non_convertible, f"non_convertible_{args.output}")
                if reduced_non_convertible:
                    export_to_csv(reduced_non_convertible, f"reduced_non_convertible_{args.output}")
        except RuntimeError as e:
            print(f"Error exporting CSV: {e}")
            sys.exit(1)
    if args.prime:
        losing_positions = filter_by_prime(positions, args.prime)
        non_convertible_positions = find_non_convertible(positions, args.prime, args.max_value)
        reduced_non_convertible = find_reduced_non_convertible(non_convertible_positions, positions, args.prime, args.max_value, args.count)
    
    # Calculate counts
    losing_count = len(losing_positions)
    non_convertible_count = len(non_convertible_positions)
    reduced_non_convertible_count = len(reduced_non_convertible)
    convertible_count = len(positions) - non_convertible_count - reduced_non_convertible_count

    # Print summary
    print("\nCounts summary:")
    print(f"Total positions: {len(positions)}")
    print(f"Losing positions (product % {args.prime} = 1): {losing_count}")
    print(f"Non-convertible positions: {non_convertible_count}")
    print(f"Reduced non-convertible positions: {reduced_non_convertible_count}")
    print(f"Convertible positions: {convertible_count}")

    # Sort positions by sum for better readability
    losing_positions.sort(key=sum)
    non_convertible_positions.sort(key=sum)

    # Print results
    print("\nNon-convertible positions (can't be converted by reducing one number):")
    print(f"Found {len(non_convertible_positions)} positions (sorted by sum)")
    for pos in non_convertible_positions:
        print(f"{pos} (count: {args.count}, max_value: {args.max_value}, product: {np.prod(pos)}, sum: {sum(pos)})")

    # Print reduced non-convertible positions
    print("\nReduced non-convertible positions (can't be converted by replacing one number):")
    print(f"Found {len(reduced_non_convertible)} positions (sorted by sum)")
    for combo in reduced_non_convertible:
        print(f"{combo} (count: {args.count}, max_value: {args.max_value}, product: {np.prod(combo)}, sum: {sum(combo)})")

    # Print debug information for reduced non-convertible positions
    if reduced_non_convertible:
        print("\nDebug information for reduced non-convertible positions:")
        for pos in reduced_non_convertible:
            product = np.prod(pos)
            m = product % args.prime
            target_product = product - m + 1
            print(f"\nFor combination {pos}:")
            print(f"Original product: {product}")
            print(f"Prime: {args.prime}")
            print(f"m: {m}")
            print(f"Target product: {target_product}")

    # Export to CSV files
    if losing_positions:
        print(f"\nExporting losing positions to positions_count{args.count}_max{args.max_value}_prime{args.prime}.csv...")
        export_to_csv(losing_positions, f"positions_count{args.count}_max{args.max_value}_prime{args.prime}.csv")
        print("Done!")
    if non_convertible_positions:
        print(f"\nExporting non-convertible positions to non_convertible_positions_count{args.count}_max{args.max_value}_prime{args.prime}.csv...")
        export_to_csv(non_convertible_positions, f"non_convertible_positions_count{args.count}_max{args.max_value}_prime{args.prime}.csv")
        print("Done!")
    if reduced_non_convertible:
        print(f"\nExporting reduced non-convertible positions to reduced_non_convertible_positions_count{args.count}_max{args.max_value}_prime{args.prime}.csv...")
        export_to_csv(reduced_non_convertible, f"reduced_non_convertible_positions_count{args.count}_max{args.max_value}_prime{args.prime}.csv")
        print("Done!")

if __name__ == "__main__":
    main()
