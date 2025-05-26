"""
Multiplicative Nim Analysis

This module provides functions for analyzing multiplicative Nim games.
"""

import csv
import argparse
import sys
import numpy as np
import itertools

def count_combinations(n, m):
    """
    Calculate the total number of combinations of length n with elements from 1 to m.
    Uses the combinatorial formula for combinations with repetition:
    C(n + m - 1, m - 1) = (n + m - 1)! / (n! * (m - 1)!)
    
    Args:
        n (int): Length of each combination
        m (int): Maximum value for each element (1 to m)
        
    Returns:
        int: Total number of combinations
    """
    from math import comb
    return comb(n + m - 1, m - 1)

def generate_positions(count, max_value, prime):
    """
    Generate all positions of length count with elements from 1 to max_value,
    excluding multiples of prime.
    This function generates positions WITH repetition, ensuring:
    - Each tuple is sorted in non-decreasing order
    - Order doesn't matter (no permutations)
    
    Args:
        count (int): Number of elements in each position
        max_value (int): Maximum value for each element (1 to max_value)
        prime (int): Prime number for filtering
        
    Returns:
        list: List of all positions (with repetition allowed)
    """
    if count <= 0 or max_value <= 0:
        raise ValueError("count and max_value must be positive integers")
    
    # If max_value < prime, all numbers are valid since they can't be multiples of prime
    if max_value < prime:
        valid_numbers = list(range(1, max_value + 1))
    else:
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

def filter_by_prime(positions, prime):
    """
    Filter positions where the product of elements is congruent to 1 modulo prime.
    
    Args:
        positions (list): List of tuples to filter
        prime (int): Prime number for filtering
        
    Returns:
        list: List of filtered positions
    """
    return [position for position in positions if np.prod(position) % prime == 1 and not any(x % prime == 0 for x in position)]

def find_non_convertible(positions, prime):
    """
    Find positions that cannot be converted to satisfy the prime condition.
    A position is non-convertible if reducing any number cannot make its product congruent to 1 modulo prime.
    
    Args:
        positions (list): List of tuples to analyze
        prime (int): Prime number for checking conversion
        
    Returns:
        list: List of non-convertible positions
    """
    non_convertible = []
    
    for position in positions:
        # Skip if already satisfies prime condition
        if np.prod(position) % prime == 1:
            continue
            
        # Try reducing each number
        can_convert = False
        for i in range(len(position)):
            if position[i] > 1:
                # Try reducing this number by 1
                reduced = list(position)
                reduced[i] -= 1
                reduced_tuple = tuple(sorted(reduced))  # Keep sorted for consistency
                
                # Check if the reduced combination satisfies prime condition
                if np.prod(reduced_tuple) % prime == 1 and not any(x % prime == 0 for x in reduced_tuple):
                    can_convert = True
                    break
        if can_convert:
            continue
            
        # If no reduction could make it satisfy prime condition, it's non-convertible
        if not can_convert:
            non_convertible.append(position)
    
    return non_convertible

def find_reduced_non_convertible(non_convertible, all_positions, prime, max_value):
    """
    Find positions that cannot be converted to satisfy the prime condition even after
    replacing any number of numbers with other valid numbers while maintaining product reduction.
    
    Args:
        non_convertible (list): List of non-convertible positions
        all_positions (list): List of all valid positions
        prime (int): Prime number for checking conversion
        max_value (int): Maximum value for each element
        
    Returns:
        list: List of reduced non-convertible positions
    """
    reduced_non_convertible = []
    
    # Get all filtered positions (where product % prime == 1)
    filtered_positions = filter_by_prime(all_positions, prime)
    
    print("\nFiltered positions:")
    for filtered_position in filtered_positions:
        print(f"Filtered position: {filtered_position}, product: {np.prod(filtered_position)}")
    
    for combo in non_convertible:
        original_product = np.prod(combo)
        
        # Calculate the target product
        m = original_product % prime
        target_product = original_product - m + 1
        
        print(f"\nChecking {combo} for reduction:")
        print(f"Original product: {original_product}, prime: {prime}, m: {m}, target: {target_product}")
        
        # Check if any filtered combination has the target product
        can_convert = False
        for filtered_combo in filtered_combinations:
            if np.prod(filtered_combo) == target_product:
                print(f"Found conversion: {combo} can be converted to {filtered_combo} with product {target_product}")
                can_convert = True
                break
        
        if not can_convert:
            print(f"No conversion found for {combo}")
            reduced_non_convertible.append(combo)
    
    print("\nReduced non-convertible combinations:")
    for rnc in reduced_non_convertible:
        print(f"Reduced non-convertible: {rnc}, product: {np.prod(rnc)}")
    
    return reduced_non_convertible

def export_to_csv(positions, filename):
    """
    Export positions to a CSV file.
    
    Args:
        positions (list): List of tuples to export
        filename (str): Name of the output CSV file
    """
    # Create header based on tuple length
    header = [f"value{i+1}" for i in range(len(combinations[0]))]
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(combinations)
    
    print(f"Combinations have been saved to {filename}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate combinations for multiplicative Nim analysis')
    parser.add_argument('--count', type=int, help='Number of elements in each combination', required=True)
    parser.add_argument('--max_value', type=int, help='Maximum value for each element', required=True)
    parser.add_argument('--prime', type=int, help='Prime number for filtering', required=True)
    parser.add_argument('--generate', action='store_true', help='Generate combinations')
    parser.add_argument('--debug', action='store_true', help='Show debug information')
    args = parser.parse_args()
    
    # Validate inputs
    if args.count <= 0 or args.max_value <= 0:
        print("Error: count and max_value must be positive integers")
        sys.exit(1)
    
    count = args.count
    max_value = args.max_value
    
    # Calculate number of combinations first
    total_combinations = count_combinations(count, max_value)
    print(f"\nYou are about to generate combinations with:")
    print(f"Number of elements (count): {count}")
    print(f"Maximum value: {max_value}")
    print(f"Total combinations: {total_combinations}")

    if not args.generate:
        print("\nUse --generate flag to proceed with generation")
        print("Example: python multiplicative_nim.py 3 4 --generate")
        return

    print(f"\nGenerating all combinations with {count} elements and max value {max_value}")
    print("(Each combination is sorted and unique)\n")

    # Generate all positions (excluding multiples of prime)
    all_positions = generate_positions(count, max_value, args.prime)

    # Process positions
    filtered_positions = filter_by_prime(all_positions, args.prime) if args.prime else []
    non_convertible_positions = find_non_convertible(all_positions, args.prime) if args.prime else []
    reduced_non_convertible = find_reduced_non_convertible(non_convertible_positions, all_positions, args.prime, args.max_value) if args.prime else []
    
    # Calculate counts
    filtered_count = len(filtered_combinations)
    non_convertible_count = len(non_convertible_combinations)
    reduced_non_convertible_count = len(reduced_non_convertible)
    convertible_count = len(all_combinations) - filtered_count - non_convertible_count - reduced_non_convertible_count

    # Print summary
    print("\nCounts summary:")
    print(f"Total combinations: {len(all_combinations)}")
    print(f"Filtered combinations (product % {args.prime} = 1): {filtered_count}")
    print(f"Non-convertible combinations: {non_convertible_count}")
    print(f"Reduced non-convertible combinations: {reduced_non_convertible_count}")
    print(f"Convertible combinations: {convertible_count}")

    # Sort combinations by sum for better readability
    filtered_combinations.sort(key=sum)
    non_convertible_combinations.sort(key=sum)

    # Print results
    print("\nNon-convertible combinations (can't be converted by reducing one number):")
    print(f"Found {len(non_convertible_combinations)} combinations (sorted by sum)")
    for combo in non_convertible_combinations:
        print(f"{combo} (count: {args.count}, max_value: {args.max_value}, product: {np.prod(combo)}, sum: {sum(combo)})")

    # Print reduced non-convertible combinations
    print("\nReduced non-convertible combinations (can't be converted by replacing one number):")
    print(f"Found {len(reduced_non_convertible)} combinations (sorted by sum)")
    for combo in reduced_non_convertible:
        print(f"{combo} (count: {args.count}, max_value: {args.max_value}, product: {np.prod(combo)}, sum: {sum(combo)})")

    # Print debug information for reduced non-convertible combinations
    if reduced_non_convertible:
        print("\nDebug information for reduced non-convertible combinations:")
        for combo in reduced_non_convertible:
            product = np.prod(combo)
            m = product % args.mod
            target_product = product - m + 1
            print(f"\nFor combination {combo}:")
            print(f"Original product: {product}")
            print(f"Modulo: {args.mod}")
            print(f"m: {m}")
            print(f"Target product: {target_product}")

    # Export to CSV files
    if filtered_positions:
        print(f"\nExporting filtered positions to positions_count{count}_max{max_value}_prime{args.prime}.csv...")
        export_to_csv(filtered_positions, f"positions_count{count}_max{max_value}_prime{args.prime}.csv")
        print("Done!")

    if non_convertible_positions:
        print(f"\nExporting non-convertible positions to non_convertible_positions_count{count}_max{max_value}_prime{args.prime}.csv...")
        export_to_csv(non_convertible_positions, f"non_convertible_positions_count{count}_max{max_value}_prime{args.prime}.csv")
        print("Done!")

    if reduced_non_convertible:
        print(f"\nExporting reduced non-convertible positions to reduced_non_convertible_positions_count{count}_max{max_value}_prime{args.prime}.csv...")
        export_to_csv(reduced_non_convertible, f"reduced_non_convertible_positions_count{count}_max{max_value}_prime{args.prime}.csv")
        print("Done!")

if __name__ == "__main__":
    main()
