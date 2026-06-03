import os
import sqlite3
import traceback
from pathlib import Path


def find_database_path():
    """Find lesson.db whether this script is run from assignment10 or python_homework."""
    candidates = [
        os.environ.get("LESSON_DB_PATH"),
        "../db/lesson.db",   # expected when running from python_homework/assignment10
        "db/lesson.db",      # expected when running from python_homework
    ]

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate

    # Fall back to the normal assignment10 path so the error message is understandable.
    return "../db/lesson.db"


def print_rows(title, rows):
    print("\n" + title)
    print("-" * len(title))
    for row in rows:
        print(row)


def task_1_first_five_order_totals(cursor):
    # TASK 1: Complex JOINs with Aggregation
    # Find the total price of each of the first 5 orders.
    stmt = """
    SELECT o.order_id,
           ROUND(SUM(li.quantity * p.price), 2) AS total_price
    FROM orders AS o
    JOIN line_items AS li
      ON o.order_id = li.order_id
    JOIN products AS p
      ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()
    print_rows("TASK 1: First 5 order totals", rows)


def task_2_average_order_price_by_customer(cursor):
    # TASK 2: Understanding Subqueries
    # For each customer, find the average price of their orders.
    stmt = """
    SELECT c.customer_name,
           ROUND(AVG(order_totals.total_price), 2) AS average_total_price
    FROM customers AS c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b,
               o.order_id,
               SUM(li.quantity * p.price) AS total_price
        FROM orders AS o
        JOIN line_items AS li
          ON o.order_id = li.order_id
        JOIN products AS p
          ON li.product_id = p.product_id
        GROUP BY o.customer_id, o.order_id
    ) AS order_totals
      ON c.customer_id = order_totals.customer_id_b
    GROUP BY c.customer_id, c.customer_name
    ORDER BY c.customer_name;
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()
    print_rows("TASK 2: Average order price by customer", rows)


def task_3_insert_order_transaction(conn, cursor):
    # TASK 3: An Insert Transaction Based on Data
    # Create a new order for Perez and Sons, created by Miranda Harris.
    # The order contains quantity 10 of each of the 5 least expensive products.

    cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_name = ?;",
        ("Perez and Sons",),
    )
    customer_row = cursor.fetchone()
    if customer_row is None:
        raise ValueError("Could not find customer named 'Perez and Sons'.")
    customer_id = customer_row[0]

    cursor.execute(
        "SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?;",
        ("Miranda", "Harris"),
    )
    employee_row = cursor.fetchone()
    if employee_row is None:
        raise ValueError("Could not find employee named 'Miranda Harris'.")
    employee_id = employee_row[0]

    cursor.execute(
        """
        SELECT product_id
        FROM products
        ORDER BY price ASC, product_id ASC
        LIMIT 5;
        """
    )
    product_rows = cursor.fetchall()
    if len(product_rows) < 5:
        raise ValueError("Could not find 5 products in the products table.")

    product_ids = [row[0] for row in product_rows]

    try:
        conn.execute("BEGIN")

        cursor.execute(
            """
            INSERT INTO orders (employee_id, customer_id)
            VALUES (?, ?)
            RETURNING order_id;
            """,
            (employee_id, customer_id),
        )
        order_id = cursor.fetchone()[0]

        line_items_to_insert = [
            (order_id, product_id, 10)
            for product_id in product_ids
        ]

        cursor.executemany(
            """
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, ?);
            """,
            line_items_to_insert,
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    cursor.execute(
        """
        SELECT li.line_item_id,
               li.quantity,
               p.product_name
        FROM line_items AS li
        JOIN products AS p
          ON li.product_id = p.product_id
        WHERE li.order_id = ?
        ORDER BY li.line_item_id;
        """,
        (order_id,),
    )
    rows = cursor.fetchall()
    print_rows(f"TASK 3: Line items for new order {order_id}", rows)


def task_4_employees_with_more_than_five_orders(cursor):
    # TASK 4: Aggregation with HAVING
    # Find all employees associated with more than 5 orders.
    stmt = """
    SELECT e.employee_id,
           e.first_name,
           e.last_name,
           COUNT(o.order_id) AS order_count
    FROM employees AS e
    JOIN orders AS o
      ON e.employee_id = o.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    HAVING COUNT(o.order_id) > 5
    ORDER BY order_count DESC, e.last_name, e.first_name;
    """
    cursor.execute(stmt)
    rows = cursor.fetchall()
    print_rows("TASK 4: Employees with more than 5 orders", rows)


def main():
    db_path = find_database_path()
    print(f"Using database: {db_path}")

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("PRAGMA foreign_keys = 1")
            cursor = conn.cursor()

            task_1_first_five_order_totals(cursor)
            task_2_average_order_price_by_customer(cursor)
            task_3_insert_order_transaction(conn, cursor)
            task_4_employees_with_more_than_five_orders(cursor)

    except Exception as e:
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Stack trace:")
        traceback.print_exc()
    else:
        print("\nAll SQL operations completed.")


if __name__ == "__main__":
    main()
