from VEXLib.Geometry.GeometryUtil import circle_circumference
from VEXLib.Geometry.RotationalVelocity import RotationalVelocity
from VEXLib.Geometry.Translation1d import Distance
from vex import Ports, GearSetting, Brain

MAIN_LOG_FILENAME = "main"
PRINT_LOG_FILENAME = "print"
ODOMETRY_LOG_FILENAME = "odometry"
COMPETITION_LOG_FILENAME = "competition_state"


class ControlStyles:
    TANK = 1
    ARCADE = 2
    SPLIT_ARCADE = 3


class DefaultPreferences:
    CONTROLLER_BINDINGS_STYLE = ControlStyles.TANK
    CUBIC_FILTER_LINEARITY = 1
    MAX_MOTOR_VOLTAGE = 12


class DirkPreferences(DefaultPreferences):
    controller_bindings_style = ControlStyles.TANK,
    cubic_filter_linearity = 1,


class DerekPreferences(DefaultPreferences):
    controller_bindings_style = ControlStyles.SPLIT_ARCADE,
    cubic_filter_linearity = 1


class AllisonPreferences(DefaultPreferences):
    controller_bindings_style = ControlStyles.SPLIT_ARCADE,
    cubic_filter_linearity = 1


class CarterPreferences(DefaultPreferences):
    controller_bindings_style = ControlStyles.TANK,
    cubic_filter_linearity = 1


class SmartPorts:
    """Drivetrain"""
    FRONT_LEFT_DRIVETRAIN_MOTOR = Ports.PORT17
    MIDDLE_LEFT_DRIVETRAIN_MOTOR = Ports.PORT11
    REAR_LEFT_DRIVETRAIN_MOTOR = Ports.PORT1

    FRONT_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT16
    MIDDLE_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT13
    REAR_RIGHT_DRIVETRAIN_MOTOR = Ports.PORT15

    SCORING_ELEVEN_WATT_MOTOR = Ports.PORT6
    SCORING_FIVE_POINT_FIVE_WATT_MOTOR = Ports.PORT3
    WALL_STAKE_MOTOR = Ports.PORT8

    INERTIAL_SENSOR = Ports.PORT11

    COLOR_SENSOR = Ports.PORT5


class ThreeWirePorts:
    """Scoring Mechanism"""
    brain = Brain()
    MOBILE_GOAL_CLAMP_PISTON = brain.three_wire_port.b
    DOINKER_PISTON = brain.three_wire_port.c
    WALL_STAKE_CALIBRATION_LIMIT_SWITCH = brain.three_wire_port.d
    del brain


class GearRatios:
    DRIVETRAIN = GearSetting.RATIO_6_1


class DrivetrainProperties:
    MAX_ACHIEVABLE_SPEED = RotationalVelocity.from_rotations_per_minute(600)
    MOTOR_TO_WHEEL_GEAR_RATIO = (36 / 60)
    ENCODER_TO_WHEEL_GEAR_RATIO = (12 / 60)
    TRACK_WIDTH = Distance.from_inches(13.5)
    WHEEL_DIAMETER = Distance.from_inches(3.235)
    WHEEL_CIRCUMFERENCE = circle_circumference(WHEEL_DIAMETER / 2)


class ScoringMechanismProperties:
    STARTUP_POSITION = 0
    DOCKED_POSITION = 0
    MAX_POSITION = 440
    SCORING_SPEED_PERCENT = 100
