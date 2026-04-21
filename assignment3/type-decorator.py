"""
Task 2: A Decorator that Takes an Argument

This script defines a decorator factory ``type_converter`` that takes a
type (e.g., ``str``, ``int`` or ``float``) and returns a decorator. The
decorator converts the return value of the decorated function to the
specified type. If the conversion is not possible, a standard
``ValueError`` will be raised by the built‑in type constructor.

Two example functions illustrate usage. ``return_int`` returns the
integer 5 but is decorated to convert its return value to a string. As
a result, the type of the result printed is ``str``. ``return_string``
returns the string "not a number" and is decorated to convert its
return value to an integer. Converting this particular string to
int will raise a ``ValueError``, which is caught and handled in the
mainline code.
"""

from functools import wraps


def type_converter(type_of_output):
    """Return a decorator that converts a function's return value.

    :param type type_of_output: A type or callable used to convert
        return values. For example, ``str``, ``int`` or ``float``.
    :returns: A decorator that converts the wrapped function's return
        value to ``type_of_output`` before returning it to the caller.
    :rtype: callable
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Call the original function and capture its return value.
            result = func(*args, **kwargs)
            # Convert and return the result using the specified type.
            return type_of_output(result)
        return wrapper
    return decorator


@type_converter(str)
def return_int():
    """Return an integer value that will be converted to a string."""
    return 5


@type_converter(int)
def return_string():
    """Return a non‑numeric string that will cause int() to fail."""
    return "not a number"


if __name__ == "__main__":
    # Demonstration of the decorator. When return_int() is called,
    # its return value 5 is converted to a string, so the printed
    # type name should be 'str'. When return_string() is called, the
    # conversion to int will raise ValueError, which we catch.
    y = return_int()
    print(type(y).__name__)
    try:
        y = return_string()
        # If no exception is raised, this line would run, which it
        # should not for the given implementation and input.
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")