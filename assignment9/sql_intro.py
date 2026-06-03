"""
Assignment 9: Introduction to Databases and SQL
Tasks 1-4

Run from the python_homework/assignment9 folder:
    python sql_intro.py

This script creates ../db/magazines.db, defines the required tables,
populates them without duplicates, and prints the required queries.
"""

import sqlite3
from pathlib import Path

DB_PATH = "../db/magazines.db"


def safe_execute(cursor, sql, params=()):
    """Run one SQL statement with exception handling."""
    try:
        cursor.execute(sql, params)
        return cursor
    except sqlite3.Error as error:
        print(f"SQL error: {error}")
        print(f"Problem statement: {sql.strip()}")
        return None


def print_rows(title, rows):
    """Print query output in a simple readable format."""
    print(f"\n{title}")
    print("-" * len(title))
    if not rows:
        print("No rows found.")
        return

    for row in rows:
        print(row)


def create_tables(cursor):
    """Create the database tables required for the assignment."""
    safe_execute(
        cursor,
        """
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
        """,
    )

    safe_execute(
        cursor,
        """
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id)
        )
        """,
    )

    safe_execute(
        cursor,
        """
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            UNIQUE (name, address)
        )
        """,
    )

    safe_execute(
        cursor,
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            UNIQUE (subscriber_id, magazine_id),
            FOREIGN KEY (subscriber_id) REFERENCES subscribers (subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (magazine_id)
        )
        """,
    )

    print("Tables created successfully.")


def get_publisher_id(cursor, publisher_name):
    result = safe_execute(
        cursor,
        "SELECT publisher_id FROM publishers WHERE name = ?",
        (publisher_name,),
    )
    if result is None:
        return None

    row = result.fetchone()
    return row[0] if row else None


def get_magazine_id(cursor, magazine_name):
    result = safe_execute(
        cursor,
        "SELECT magazine_id FROM magazines WHERE name = ?",
        (magazine_name,),
    )
    if result is None:
        return None

    row = result.fetchone()
    return row[0] if row else None


def get_subscriber_id(cursor, subscriber_name, subscriber_address):
    result = safe_execute(
        cursor,
        """
        SELECT subscriber_id
        FROM subscribers
        WHERE name = ? AND address = ?
        """,
        (subscriber_name, subscriber_address),
    )
    if result is None:
        return None

    row = result.fetchone()
    return row[0] if row else None


def add_publisher(cursor, name):
    """Add one publisher if it does not already exist."""
    existing_id = get_publisher_id(cursor, name)
    if existing_id is not None:
        print(f"Publisher already exists: {name}")
        return existing_id

    result = safe_execute(
        cursor,
        "INSERT INTO publishers (name) VALUES (?)",
        (name,),
    )
    if result is not None:
        print(f"Added publisher: {name}")
        return result.lastrowid
    return None


def add_magazine(cursor, name, publisher_name):
    """Add one magazine if it does not already exist."""
    existing_id = get_magazine_id(cursor, name)
    if existing_id is not None:
        print(f"Magazine already exists: {name}")
        return existing_id

    publisher_id = get_publisher_id(cursor, publisher_name)
    if publisher_id is None:
        print(f"Cannot add magazine '{name}' because publisher '{publisher_name}' was not found.")
        return None

    result = safe_execute(
        cursor,
        "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
        (name, publisher_id),
    )
    if result is not None:
        print(f"Added magazine: {name}")
        return result.lastrowid
    return None


def add_subscriber(cursor, name, address):
    """Add one subscriber if the same name/address combination does not already exist."""
    existing_id = get_subscriber_id(cursor, name, address)
    if existing_id is not None:
        print(f"Subscriber already exists: {name}, {address}")
        return existing_id

    result = safe_execute(
        cursor,
        "INSERT INTO subscribers (name, address) VALUES (?, ?)",
        (name, address),
    )
    if result is not None:
        print(f"Added subscriber: {name}")
        return result.lastrowid
    return None


def add_subscription(cursor, subscriber_name, subscriber_address, magazine_name, expiration_date):
    """Add one subscription if that subscriber is not already subscribed to that magazine."""
    subscriber_id = get_subscriber_id(cursor, subscriber_name, subscriber_address)
    if subscriber_id is None:
        print(f"Cannot add subscription because subscriber '{subscriber_name}' was not found.")
        return None

    magazine_id = get_magazine_id(cursor, magazine_name)
    if magazine_id is None:
        print(f"Cannot add subscription because magazine '{magazine_name}' was not found.")
        return None

    existing = safe_execute(
        cursor,
        """
        SELECT subscription_id
        FROM subscriptions
        WHERE subscriber_id = ? AND magazine_id = ?
        """,
        (subscriber_id, magazine_id),
    )
    if existing is None:
        return None

    if existing.fetchone() is not None:
        print(f"Subscription already exists: {subscriber_name} -> {magazine_name}")
        return None

    result = safe_execute(
        cursor,
        """
        INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
        VALUES (?, ?, ?)
        """,
        (subscriber_id, magazine_id, expiration_date),
    )
    if result is not None:
        print(f"Added subscription: {subscriber_name} -> {magazine_name}")
        return result.lastrowid
    return None


def populate_tables(cursor):
    """Populate all four tables with sample data."""
    add_publisher(cursor, "Code Monthly Publishing")
    add_publisher(cursor, "Global Tech Press")
    add_publisher(cursor, "Learning House")

    add_magazine(cursor, "Python Weekly", "Code Monthly Publishing")
    add_magazine(cursor, "SQL Today", "Code Monthly Publishing")
    add_magazine(cursor, "AI Review", "Global Tech Press")
    add_magazine(cursor, "Education Matters", "Learning House")

    add_subscriber(cursor, "Alice Johnson", "100 Main Street")
    add_subscriber(cursor, "Bob Smith", "200 Oak Avenue")
    add_subscriber(cursor, "Charlie Lee", "300 Pine Road")

    add_subscription(cursor, "Alice Johnson", "100 Main Street", "Python Weekly", "2027-01-15")
    add_subscription(cursor, "Alice Johnson", "100 Main Street", "SQL Today", "2027-02-20")
    add_subscription(cursor, "Bob Smith", "200 Oak Avenue", "AI Review", "2026-12-31")
    add_subscription(cursor, "Charlie Lee", "300 Pine Road", "Education Matters", "2027-03-10")
    add_subscription(cursor, "Charlie Lee", "300 Pine Road", "Python Weekly", "2027-04-05")


def run_queries(cursor):
    """Run and print the required SQL queries."""
    subscribers_query = safe_execute(cursor, "SELECT * FROM subscribers")
    if subscribers_query is not None:
        print_rows("All subscriber information", subscribers_query.fetchall())

    magazines_query = safe_execute(cursor, "SELECT * FROM magazines ORDER BY name")
    if magazines_query is not None:
        print_rows("All magazines sorted by name", magazines_query.fetchall())

    publisher_name = "Code Monthly Publishing"
    magazines_by_publisher_query = safe_execute(
        cursor,
        """
        SELECT publishers.name AS publisher_name, magazines.name AS magazine_name
        FROM publishers
        JOIN magazines ON publishers.publisher_id = magazines.publisher_id
        WHERE publishers.name = ?
        ORDER BY magazines.name
        """,
        (publisher_name,),
    )
    if magazines_by_publisher_query is not None:
        print_rows(
            f"Magazines published by {publisher_name}",
            magazines_by_publisher_query.fetchall(),
        )


def main():
    Path("../db").mkdir(exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        print("Database created and connected successfully.")

        try:
            conn.execute("PRAGMA foreign_keys = 1")
            print("Foreign key support turned on.")
        except sqlite3.Error as error:
            print(f"Could not enable foreign keys: {error}")

        cursor = conn.cursor()
        create_tables(cursor)
        populate_tables(cursor)

        try:
            conn.commit()
            print("Changes committed successfully.")
        except sqlite3.Error as error:
            print(f"Commit failed: {error}")

        run_queries(cursor)

    except sqlite3.Error as error:
        print(f"Database connection error: {error}")
    finally:
        if conn is not None:
            conn.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
