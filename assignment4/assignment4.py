"""
Assignment 4 – Intro to Data Engineering with Pandas

This module contains code to explore basic Pandas functionality.  The
tasks are broken into four sections and correspond to the unit tests
found in ``assignment4-test.py``.  Each task builds upon the prior
steps to demonstrate how to create DataFrames, manipulate and clean
data, and persist the results.

Running the tests with ``pytest -v -x assignment4-test.py`` will
exercise the variables defined here.  When executed as a script, this
module performs no top‑level actions.
"""

import json
from pathlib import Path

import pandas as pd
import numpy as np

###############################################################################
# Task 1: Introduction to Pandas – Creating and Manipulating DataFrames
###############################################################################

# Create a DataFrame from a dictionary.  The keys of the dictionary
# become column labels and the lists become the column values.  This
# represents a simple table of employees with their names, ages and
# cities.  A variable assignment is used so that the resulting
# DataFrame can be imported by the tests.
task1_data_frame = pd.DataFrame(
    {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago'],
    }
)

# Make a copy of the initial DataFrame and add a ``Salary`` column.
# The copy prevents modifications from affecting the original object.
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = pd.Series([70000, 80000, 90000])

# Create a third DataFrame where each employee is one year older.  The
# ``Age`` column is incremented by 1.  Using ``copy()`` avoids
# modifying the DataFrame created above.
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1

# Persist the updated DataFrame to a CSV file named ``employees.csv``.
# Setting ``index=False`` omits the DataFrame’s index from the file,
# which matches the test’s expectation of a file with exactly 3 rows
# and 4 columns.
task1_csv_path = Path('employees.csv')
task1_older.to_csv(task1_csv_path, index=False)


###############################################################################
# Task 2: Loading Data from CSV and JSON
###############################################################################

# Read the CSV produced in Task 1 back into a DataFrame.  The path
# relative to the current working directory is used here.  The tests
# compare this against ``task1_older`` to ensure that the file was
# written correctly.
task2_employees = pd.read_csv(task1_csv_path)

# Prepare a JSON file with two additional employees.  The data are
# specified as a list of dictionaries and then written to
# ``additional_employees.json``.  The file is written once when this
# module is imported.  Note: indent=4 produces human‑readable JSON.
additional_employees_path = Path('additional_employees.json')
if not additional_employees_path.exists():
    additional_data = [
        {'Name': 'Eve', 'Age': 28, 'City': 'Miami', 'Salary': 60000},
        {'Name': 'Frank', 'Age': 40, 'City': 'Seattle', 'Salary': 95000},
    ]
    with additional_employees_path.open('w', encoding='utf-8') as f:
        json.dump(additional_data, f, indent=4)

# Load the JSON file into a DataFrame.  ``pd.read_json`` can
# automatically interpret the list of dictionaries produced above.
json_employees = pd.read_json(additional_employees_path)

# Concatenate the employees read from CSV with those read from JSON.
# ``ignore_index=True`` resets the index on the resulting DataFrame so
# that it runs from 0 to N‑1.  Without resetting the index the test
# would still pass for ``equals`` but the shape test would reveal the
# mismatch when comparing against the expected ``(5, 4)`` shape.
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)


###############################################################################
# Task 3: Data Inspection – Using Head, Tail and Info Methods
###############################################################################

# Capture the first three rows of the combined employee DataFrame.
first_three = more_employees.head(3)

# Capture the last two rows of the combined employee DataFrame.
last_two = more_employees.tail(2)

# Store the shape of the combined DataFrame.  This returns a tuple
# ``(number_of_rows, number_of_columns)``.
employee_shape = more_employees.shape

# For the ``info`` method the tests only require that it is called for
# its side effect of printing the summary.  Calling it once here
# provides that side effect when the module is imported.  The
# ``buf=None`` argument directs Pandas to write to stdout.
_ = more_employees.info()


###############################################################################
# Task 4: Data Cleaning
###############################################################################

# Read the dirty data from ``dirty_data.csv``.  This file contains
# inconsistent spacing, placeholder strings for missing values and
# duplicate rows.  Pandas will treat all values as strings by
# default until they are converted below.
dirty_data_path = Path('dirty_data.csv')
dirty_data = pd.read_csv(dirty_data_path)

# Create a copy of the dirty data to preserve the original
# DataFrame.  All subsequent transformations operate on this copy.
clean_data = dirty_data.copy()

# Remove duplicate rows based on all columns.  ``inplace=True``
# mutates the DataFrame directly.
clean_data.drop_duplicates(inplace=True)

# Convert the ``Age`` column to numeric values.  Any values that
# cannot be coerced (e.g. 'NaN' or whitespace) become ``NaN``.  The
# series will then be a floating‑point dtype because of the missing
# values.
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')

# Replace known non‑numeric placeholders in ``Salary`` with NA
# (missing) markers.  After replacement, convert the column to
# numeric.  Again, non‑coercible values become ``NaN``.
clean_data['Salary'] = clean_data['Salary'].replace([
    'unknown', 'n/a', 'unknown ', ' unknown', 'n/a '], pd.NA
)
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')

# Fill missing numeric values.  Use the mean of ``Age`` and the
# median of ``Salary``.  ``skipna=True`` ignores missing values when
# computing these statistics.
age_mean = clean_data['Age'].mean(skipna=True)
salary_median = clean_data['Salary'].median(skipna=True)
clean_data['Age'] = clean_data['Age'].fillna(age_mean)
clean_data['Salary'] = clean_data['Salary'].fillna(salary_median)

# Convert the ``Hire Date`` column to datetime.  The ``format='mixed'``
# argument tells Pandas to automatically interpret multiple date
# formats.  ``errors='coerce'`` converts unparseable dates into
# ``NaT`` (not‑a‑time) values.  In this specific dataset all dates
# should parse successfully.
clean_data['Hire Date'] = pd.to_datetime(
    clean_data['Hire Date'], errors='coerce', format='mixed'
)

# Trim whitespace from the ``Name`` column.  Leading and trailing
# spaces can appear due to inconsistent spacing in the CSV.  After
# stripping, the names remain as originally capitalized.
clean_data['Name'] = clean_data['Name'].str.strip()

# Standardize the ``Department`` column by stripping whitespace and
# converting to uppercase.  This ensures that strings such as
# ``' hr'``, ``'HR'`` and ``'Sales '`` all become consistent tokens.
clean_data['Department'] = (
    clean_data['Department']
    .str.strip()
    .str.upper()
)

# At this point ``clean_data`` contains no duplicate rows, all numeric
# fields are numeric without missing values, dates are datetime64
# values without ``NaT`` entries, names are trimmed and departments
# are uppercase.  The unit tests in ``assignment4-test.py`` verify
# these properties.
