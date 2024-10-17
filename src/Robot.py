import json

from VEXLib.Geometry.Rotation2d import Rotation2d
from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Translation1d import Translation1d
from VEXLib.Robot.TelemteryRobot import TelemetryRobot
from VEXLib.Robot.TimedRobot import TimedRobot
from VEXLib.Util import time
from Drivetrain import Drivetrain
from MobileGoalClamp import MobileGoalClamp
from ScoringMechanism import ScoringMechanism
from WallStakeMechanism import WallStakeMechanism
from Constants import Preferences
from SerialData import Frame
from CRC import crc_bytes
from vex import *


class Robot(TimedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.controller = Controller(PRIMARY)
        self.drivetrain = Drivetrain()
        self.left_distance_sensor = Distance(Ports.PORT5)
        self.right_distance_sensor = Distance(Ports.PORT4)
        self.i = 0
        self.mobile_goal_clamp = MobileGoalClamp()
        self.scoring_mechanism = ScoringMechanism()
        self.wall_stake_mechanism = WallStakeMechanism()

    def debug_wait(self):
        while not self.controller.buttonA.pressing():
            pass
        while self.controller.buttonA.pressing():
            pass

    def red_negative_auto(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
        self.mobile_goal_clamp.release_mobile_goal()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), 90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), 60, ramp_down=False)
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(-100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), 60, ramp_up=False, turn_first=True)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), 5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), -83)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-5), -83)
        time.sleep(5)

    def blue_negative_auto(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(-90)
        self.mobile_goal_clamp.release_mobile_goal()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-25), -90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-70), -60, ramp_down=False)
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(-100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-20), -60, ramp_up=False)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(55), -5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 83)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-5), 83)
        time.sleep(5)

    def red_positive_auto(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(80, DEGREES, wait=False)

        self.mobile_goal_clamp.release_mobile_goal()
        # self.debug_wait()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-32), 90)
        # self.debug_wait()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-80), 120, ramp_down=False)
        # self.debug_wait()
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(-100)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(45), 180)
        time.sleep(3)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(140), 0)
        time.sleep(5)

    def skills_auto(self):
        self.drivetrain.odometry.starting_offset = Rotation2d.from_degrees(90)
        self.mobile_goal_clamp.release_mobile_goal()
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-27), 90)
        self.wall_stake_mechanism.motor.set_velocity(50, PERCENT)
        self.wall_stake_mechanism.motor.spin_to_position(650, DEGREES, wait=True)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(20), 90)
        self.wall_stake_mechanism.motor.spin_to_position(80, DEGREES, wait=False)
        time.sleep(0.5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-26), 90)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-60), 0)
        self.mobile_goal_clamp.clamp_mobile_goal()
        self.scoring_mechanism.spin_motor_at_speed(-100)
        time.sleep(0.5)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(100), 230)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(-5), 230)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(70), 90)
        time.sleep(1)
        self.drivetrain.move_distance_towards_direction_trap(Translation1d.from_centimeters(30), 90)


    # def on_autonomous(self):
    #     self.red_positive_auto()

    def on_autonomous_disable(self):
        self.wall_stake_mechanism.motor.set_velocity(0, PERCENT)
        self.wall_stake_mechanism.motor.spin(FORWARD)


    def setup(self):
        # self.register_telemetry()
        self.controller.buttonB.pressed(self.mobile_goal_clamp.toggle_clamp)
        self.controller.buttonR1.pressed(self.wall_stake_mechanism.start_scoring)
        self.controller.buttonR1.released(self.wall_stake_mechanism.stop)

        self.controller.buttonL1.pressed(self.wall_stake_mechanism.start_docking)
        self.controller.buttonL1.released(self.wall_stake_mechanism.stop)

        self.controller.buttonX.pressed(self.trigger_restart)

    def periodic(self):
        # message = b"This is a test message"
        #
        # frame = Frame(frame_header=[0xEB, 0x90], frame_type=0x3, data_length=len(message), frame_id=1,
        #               data=message, crc_function=crc_bytes)
        # frame_bytearray = frame.get_bytearray()
        # self.output_buffer.append(frame_bytearray + b"\n")
        # self.output_buffer.append(frame_bytearray.hex().upper().encode() + b"\n")

        # print(frame_bytearray + b"\n")


        scoring_mechanism_speed = 0

        if self.controller.buttonR2.pressing():
            scoring_mechanism_speed = -100
        elif self.controller.buttonL2.pressing():
            scoring_mechanism_speed = 100

        if Preferences.ARCADE_CONTROL:
            forward_speed = self.controller.axis3.position()
            turn_speed = self.controller.axis4.position()
            left_speed = forward_speed - turn_speed
            right_speed = forward_speed + turn_speed
        else:
            left_speed = self.controller.axis3.position()
            right_speed = self.controller.axis2.position()

        if self.controller.buttonA.pressing():
            self.skills_auto()


        self.drivetrain.set_speed_percent(left_speed, right_speed)

        self.drivetrain.update_motor_voltages()
        self.drivetrain.update_odometry()

        if Preferences.PRINT_POSE:
            print(self.drivetrain.odometry.get_pose())

        self.scoring_mechanism.spin_motor_at_speed(scoring_mechanism_speed)
