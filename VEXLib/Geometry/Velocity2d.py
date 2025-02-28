import math

import VEXLib.Units.Units as Units
from VEXLib.Math import MathUtil


class Velocity2d:
    """Represents a 1D velocity."""

    def __init__(self, x=0.0, y=0.0):
        """Initialize the Velocity2d object with x and y speeds"""
        self.x = x
        self.y = y

    def __add__(self, other):
        """Add two Velocity2d objects."""
        return Velocity2d(self.x + other.magnitude, self.y + other.y)

    def __sub__(self, other):
        """Subtract two Velocity1d objects."""
        return Velocity2d(self.x - other.magnitude, self.y - other.y)

    def __eq__(self, other):
        """Check if two Velocity1d objects are equal."""
        return self.x == other.magnitude and self.y == other.y

    def __mul__(self, scalar):
        """Multiply Velocity1d by a scalar."""
        return Velocity2d(self.x * scalar, self.y * scalar)

    def __str__(self):
        """Return the string representation of Velocity1d."""
        return str(self.x) + " m/s"

    @classmethod
    def from_meters_per_second(cls, x_meters_per_second, y_meters_per_second):
        return cls(x_meters_per_second, y_meters_per_second)

    @classmethod
    def from_centimeters_per_second(cls, x_centimeters_per_second, y_centimeters_per_second):
        return cls(Units.centimeters_to_meters(x_centimeters_per_second),
                   Units.centimeters_to_meters(y_centimeters_per_second))

    @classmethod
    def from_inches_per_second(cls, x_inches_per_second):
        return cls(Units.inches_to_meters(x_inches_per_second))

    @classmethod
    def from_feet_per_second(cls, x_feet_per_second, y_feet_per_second):
        return cls(Units.feet_to_meters(x_feet_per_second), Units.feet_to_meters(y_feet_per_second))

    def to_meters_per_second(self):
        return self.x, self.y

    def to_centimeters_per_second(self):
        return Units.meters_to_centimeters(self.x), Units.meters_to_centimeters(self.y)

    def to_inches_per_second(self):
        return Units.meters_to_inches(self.x), Units.meters_to_inches(self.y)

    @property
    def angle_rad(self):
        return math.atan2(self.y, self.x)

    @angle_rad.setter
    def angle_rad(self, angle):
        length = self.get_length()
        self.x = length * math.cos(angle)
        self.y = length * math.sin(angle)

    def get_length(self):
        return MathUtil.hypotenuse(self.x, self.y)


Speed2d = Velocity2d
