"""
Assignment 9 Task 6 starter: Web Scraping Capstone database code

Use this only for your capstone project CSV files.

Suggested setup:
1. Create a folder inside assignment9 called capstone_csvs.
2. Put your cleaned/transformed capstone CSV files in that folder.
3. Run this file from python_homework/assignment9:
       python capstone_database_starter.py

The script imports each CSV into ../db/capstone.db as a separate SQLite table.
Each table name is based on the CSV file name.
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

CSV_FOLDER = Path("capstone_csvs")
DB_PATH = Path("../db/capstone.db")


def make_table_name(file_path):
    """Convert a CSV file name into a safe SQLite table name."""
    name = file_path.stem.lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        name = "capstone_data"
    if name[0].isdigit():
        name = f"table_{name}"
    return name


def clean_dataframe(df):
    """Basic cleaning starter: trim text, remove duplicates, and drop fully empty rows."""
    before_rows = len(df)

    df = df.dropna(how="all")
    df = df.drop_duplicates()

    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].astype(str).str.strip()
        df[column] = df[column].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    after_rows = len(df)
    return df, before_rows, after_rows


def main():
    CSV_FOLDER.mkdir(exist_ok=True)
    DB_PATH.parent.mkdir(exist_ok=True)

    csv_files = sorted(CSV_FOLDER.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {CSV_FOLDER}.")
        print("Add your capstone CSV files to that folder, then run this script again.")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            for csv_file in csv_files:
                table_name = make_table_name(csv_file)

                try:
                    raw_df = pd.read_csv(csv_file)
                except (OSError, pd.errors.ParserError) as error:
                    print(f"Could not read {csv_file}: {error}")
                    continue

                clean_df, before_rows, after_rows = clean_dataframe(raw_df)
                clean_df.to_sql(table_name, conn, if_exists="replace", index=False)

                print(f"Imported {csv_file.name} into table '{table_name}'.")
                print(f"Rows before cleaning: {before_rows}")
                print(f"Rows after cleaning: {after_rows}")
                print("-" * 40)

            conn.commit()
            print(f"Capstone database created at {DB_PATH}")

    except sqlite3.Error as error:
        print(f"Database error: {error}")


if __name__ == "__main__":
    main()
