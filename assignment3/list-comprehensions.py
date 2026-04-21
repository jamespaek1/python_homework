"""
Task 3: List Comprehensions Practice

This script demonstrates how to read data from a CSV file and process
it using list comprehensions. It expects a CSV file located one
directory up in ``csv/employees.csv`` relative to this script. The
CSV should have a header row with at least ``first_name`` and
``last_name`` columns, followed by employee data.

The program performs two operations:
    1. It reads the file into a list of lists using the ``csv`` module.
    2. It constructs a list of full names (``first_name`` + space
       + ``last_name``) using a list comprehension. The header row is
       skipped.
    3. It constructs another list of names containing the letter
       'e' (case‑insensitive) using another list comprehension.

If the expected CSV file is missing, a message will be printed and
execution stops.
"""

import csv
import os


def read_employees_csv(path):
    """Read employees.csv into a list of lists.

    :param str path: Path to the CSV file.
    :returns: List of rows, each itself a list of column values.
    :rtype: list[list[str]]
    :raises FileNotFoundError: If the specified file does not exist.
    """
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]
    return data


def main():
    # Construct the path relative to this file: ../csv/employees.csv.
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, '..', 'csv', 'employees.csv')
    try:
        rows = read_employees_csv(csv_path)
    except FileNotFoundError:
        print(f"CSV file not found at {csv_path}. Please ensure it exists.")
        return
    if not rows:
        print("No data found in the CSV file.")
        return
    # Assume the first row is the header
    header = rows[0]
    # Build a mapping of column names to indices for first_name and last_name
    try:
        first_index = header.index('first_name')
        last_index = header.index('last_name')
    except ValueError:
        print("CSV header must contain 'first_name' and 'last_name' columns.")
        return
    # List comprehension to build full names, skipping the header row
    names = [row[first_index] + ' ' + row[last_index] for row in rows[1:]]
    print("All names:", names)
    # List comprehension to select names containing the letter 'e' (case‑insensitive)
    names_with_e = [name for name in names if 'e' in name.lower()]
    print("Names containing 'e':", names_with_e)


if __name__ == '__main__':
    main()