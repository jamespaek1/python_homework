"""
Task 1: Writing and Testing a Decorator

This module defines a decorator called ``logger_decorator`` that logs
information about calls to decorated functions. It records the function
name, positional arguments, keyword arguments and return value in
``decorator.log``. Three sample functions demonstrate usage: one
without parameters, one accepting an arbitrary number of positional
arguments, and one accepting arbitrary keyword arguments. When run as
a script, each function is invoked so the log file shows example
entries.

To inspect the log after execution, open the ``decorator.log`` file
located in the same directory.
"""

import logging
from functools import wraps


def logger_decorator(func):
    """A decorator that logs details about function calls.

    The log includes the name of the function being called, a list of
    positional arguments, a dictionary of keyword arguments and the
    return value. All log entries are appended to ``decorator.log``.
    """

    # Configure a module‑specific logger once per decorated function
    logger = logging.getLogger(func.__name__ + "_parameter_log")
    # Avoid duplicating handlers if the decorator is applied multiple
    # times in the same interpreter session. Only add a handler if no
    # handlers exist.
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("decorator.log", mode="a")
        logger.addHandler(handler)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Prepare human‑readable strings for positional and keyword
        # arguments. Use 'none' if no arguments are supplied.
        pos_repr = list(args) if args else "none"
        kw_repr = kwargs if kwargs else "none"
        # Execute the original function and capture the return value.
        result = func(*args, **kwargs)
        # Build the log message. Each field is on its own line for
        # readability in the log file. Use repr() on the return value
        # to capture complex objects safely.
        log_message = (
            f"function: {func.__name__}\n"
            f"positional parameters: {pos_repr}\n"
            f"keyword parameters: {kw_repr}\n"
            f"return: {result!r}"
        )
        logger.log(logging.INFO, log_message)
        return result

    return wrapper


@logger_decorator
def hello_world():
    """Prints and returns a greeting."""
    greeting = "Hello, World!"
    print(greeting)
    return greeting


@logger_decorator
def always_true(*args):
    """Returns True regardless of the positional arguments passed."""
    # This function doesn't use its arguments but accepts any number of
    # positional arguments for demonstration purposes.
    return True


@logger_decorator
def return_decorator(**kwargs):
    """Returns the ``logger_decorator`` function itself.

    This demonstrates a decorated function that accepts arbitrary
    keyword arguments and returns a function. While contrived, it
    illustrates that the decorator captures keyword parameters and
    return types other than primitives.
    """
    # The keyword arguments are not used for anything here except to be
    # logged by the decorator. The return value is the decorator
    # function itself.
    return logger_decorator


if __name__ == "__main__":
    # Demonstration calls for logging. Pass some parameters to show how
    # different argument types are recorded.
    hello_world()
    always_true(1, 2, 3)
    return_decorator(foo="bar", baz=42)