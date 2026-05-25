"""
Assignment 9: Introduction to Databases and SQL
Task 5

Run from the python_homework/assignment9 folder:
    python sql_intro_2.py

Before running this file, run load_db.py from the python_homework folder
so that ../db/lesson.db exists.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = "../db/lesson.db"
OUTPUT_PATH = "order_summary.csv"

SQL_STATEMENT = """
SELECT
    line_items.line_item_id,
    line_items.quantity,
    line_items.product_id,
    products.product_name,
    products.price
FROM line_items
JOIN products ON line_items.product_id = products.product_id;
"""


def main():
    if not Path(DB_PATH).exists():
        print(f"Could not find {DB_PATH}.")
        print("Run load_db.py from the python_homework folder first, then run this script again.")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(SQL_STATEMENT, conn)
    except (sqlite3.Error, pd.errors.DatabaseError) as error:
        print(f"Could not read data from the database: {error}")
        return

    print("\nFirst 5 rows from the SQL query")
    print(df.head())

    df["total"] = df["quantity"] * df["price"]

    print("\nFirst 5 rows after adding the total column")
    print(df.head())

    summary_df = (
        df.groupby("product_id")
        .agg(
            times_ordered=("line_item_id", "count"),
            total=("total", "sum"),
            product_name=("product_name", "first"),
        )
        .reset_index()
    )

    print("\nFirst 5 rows after grouping by product_id")
    print(summary_df.head())

    summary_df = summary_df.sort_values("product_name")

    try:
        summary_df.to_csv(OUTPUT_PATH, index=False)
        print(f"\nOrder summary written to {OUTPUT_PATH}")
    except OSError as error:
        print(f"Could not write {OUTPUT_PATH}: {error}")


if __name__ == "__main__":
    main()
