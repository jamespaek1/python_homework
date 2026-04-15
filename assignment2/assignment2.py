# Task 2: Read a CSV File
import csv
import os
import traceback
from datetime import datetime

import custom_module


def _print_exception(e):
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = []

    for trace in trace_back:
        stack_trace.append(
            f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}"
        )

    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")


def _read_csv_dict(file_path, tuple_rows=False):
    data = {}
    rows = []

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)

            for index, row in enumerate(reader):
                if index == 0:
                    data["fields"] = row
                else:
                    rows.append(tuple(row) if tuple_rows else row)

        data["rows"] = rows
        return data

    except Exception as e:
        _print_exception(e)
        return {"fields": [], "rows": []}


def read_employees():
    return _read_csv_dict("../csv/employees.csv")


employees = read_employees()


# Task 3: Find the Column Index
def column_index(column_name):
    return employees["fields"].index(column_name)


employee_id_column = column_index("employee_id")


# Task 4: Find the Employee First Name
def first_name(row_number):
    first_name_column = column_index("first_name")
    return employees["rows"][row_number][first_name_column]


# Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))
    return matches


# Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    matches = list(
        filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"])
    )
    return matches


# Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    last_name_column = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_column])
    return employees["rows"]


# Task 8: Create a dict for an Employee
def employee_dict(row):
    employee = {}

    for field, value in zip(employees["fields"], row):
        if field != "employee_id":
            employee[field] = value

    return employee


# Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    all_employees = {}

    for row in employees["rows"]:
        employee_id = row[employee_id_column]
        all_employees[employee_id] = employee_dict(row)

    return all_employees


# Task 10: Use the os Module
def get_this_value():
    return os.getenv("THISVALUE")


# Task 11: Creating Your Own Module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


# Task 12: Read minutes1.csv and minutes2.csv
def read_minutes():
    minutes1 = _read_csv_dict("../csv/minutes1.csv", tuple_rows=True)
    minutes2 = _read_csv_dict("../csv/minutes2.csv", tuple_rows=True)
    return minutes1, minutes2


minutes1, minutes2 = read_minutes()


# Task 13: Create minutes_set
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    return set1.union(set2)


minutes_set = create_minutes_set()


# Task 14: Convert to datetime
def create_minutes_list():
    minutes = list(minutes_set)
    converted = list(
        map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes)
    )
    return converted


minutes_list = create_minutes_list()


# Task 15: Write Out Sorted List
def write_sorted_list():
    minutes_list.sort(key=lambda item: item[1])

    converted = list(
        map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list)
    )

    with open("./minutes.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(minutes1["fields"])
        writer.writerows(converted)

    return converted