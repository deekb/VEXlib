import math
from VEXLib.Math import MathUtil
from VEXLib.Geometry.Rotation2d import Rotation2d


def calculate_wheel_power_holonomic(
        movement_angle_rad: float, movement_speed: float, wheel_angle_rad: float
) -> float:
    """
    Calculate the necessary wheel power for a wheel pointing in the specified angle to move the robot toward the desired target
    This function must be run for all wheels in the drivetrain separately

    Args:
        movement_angle_rad: The angle to move the robot
        movement_speed: The speed to move at
        wheel_angle_rad: The angle of the wheel to calculate power for

    Returns:
        The calculated power for the wheel
    """

    if movement_speed < 0:
        raise ValueError("Speed may not be negative")

    return movement_speed * math.cos(wheel_angle_rad - movement_angle_rad)


class Wheel:
    def __init__(self, direction=Rotation2d.from_revolutions(0)):
        self.direction: Rotation2d = direction

    def wheel_contribution_coefficient(self, movement_angle_rad: float) -> float:
        """returns a coefficient from -1 to 1 representing how the movement of this wheel is correlated
         to the movement of the chassis
        """
        return MathUtil.cos(self.direction - movement_angle_rad)

    def wheel_speed(self, movement_angle_rad: float, movement_speed) -> float:
        return self.wheel_contribution_coefficient(movement_angle_rad) * movement_speed

# class Drivetrain:
#     def __init__(self, wheels=None):
#         if wheels is None:
#             wheels = []
#
#     def move(self, vector):
