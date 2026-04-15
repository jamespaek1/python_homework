"""
Task 5: Extending a Class – Points and Vectors

This module defines a ``Point`` class representing a point in 2D space
with methods for equality comparison, string representation and
Euclidean distance to another point. It also defines a ``Vector``
class that inherits from ``Point`` but overrides the string
representation and implements vector addition via the ``+`` operator.

When run as a script, the module instantiates several points and
vectors, demonstrates the implemented methods and prints results.
"""

import math
from typing import Any


class Point:
    """Represent a point in 2D Cartesian space."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Any) -> bool:
        """Compare two points for equality.

        Points are considered equal if their x and y coordinates are
        identical. Non‑Point instances return ``NotImplemented`` to
        indicate the comparison is unsupported.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """Return a human‑readable string representation."""
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other: "Point") -> float:
        """Return the Euclidean distance to another point."""
        if not isinstance(other, Point):
            raise TypeError("distance_to requires another Point instance")
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)


class Vector(Point):
    """Represent a vector in 2D space, inheriting from Point."""

    def __str__(self) -> str:
        """Return a string representation distinguishing vectors."""
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        """Add two vectors component‑wise and return a new Vector."""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)


if __name__ == "__main__":
    # Demonstration of Point equality and distance
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    p3 = Point(1, 2)
    print(f"p1 == p2: {p1 == p2}")  # False
    print(f"p1 == p3: {p1 == p3}")  # True
    print(f"Distance from p1 to p2: {p1.distance_to(p2):.2f}")

    # Demonstration of Vector string representation and addition
    v1 = Vector(1, 0)
    v2 = Vector(0, 2)
    v3 = v1 + v2
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    print(f"v1 + v2 = {v3}")