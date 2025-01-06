import math
from vex import Motor as vexMotor, GearSetting, DEGREES, RPM, VOLT, Thread
from ..Algorithms.PID import PIDController
from ..Util import time as time
from .Constants import *


class Motor:
    def __init__(self, port, gear_ratio=18,  direction=FORWARD, run_mode=NONE):
        # We are running all motors at 18:1 gear ratio and compensating for it in the get_position and get_velocity methods
        self.port = port
        self._motor = vexMotor(port, GearSetting.RATIO_18_1, FORWARD)
        self.gear_ratio = gear_ratio
        self.direction = direction
        self.run_type = run_mode
        self._encoder_offset = 0
        self._velocity_setpoint = 0
        self._position_setpoint = 0
        self.position_pid = PIDController(0, 0, 0, 0.05)
        self.velocity_pid = PIDController(0, 0, 0, 0.05)
        Thread(self.update_loop)

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def set_target_velocity(self, velocity):
        if abs(velocity) > 1:
            raise ValueError("Velocity must be between -1 and 1")
        self._velocity_setpoint = velocity

    def set_target_position(self, position):
        self._position_setpoint = position

    def update_loop(self):
        while True:
            time.sleep(0.05)
            self.update_pid()

    def update_pid(self):
        if self.run_type == PID_VELOCITY_CONTROL:
            # TODO: Get this working
            speed = self.velocity_pid.update(self.get_velocity_rotations_per_minute())
        elif self.run_type == PID_POSITION_CONTROL:
            speed = self.position_pid.update(self.get_position_degrees())

        else:
            speed = self._velocity_setpoint

        self._motor.set_velocity(speed * (-100 if self.direction == REVERSE else 100))

    def set_voltage(self, voltage):
        if abs(voltage) > 12:
            raise ValueError("Voltage must be between -12 and 12")
        self._motor.spin(FORWARD, voltage * (-1 if self.direction == REVERSE else 1), VOLT)

    def reset_encoder(self):
        self._encoder_offset = self.get_position_degrees()

    def set_encoder_position_degrees(self, position):
        self._encoder_offset = self.get_position_degrees() + position

    def get_position_degrees(self):
        return self._motor.position(DEGREES) - self._encoder_offset

    def get_position_turns(self):
        return self.get_position_degrees() / 360

    def get_position_radians(self):
        return math.radians(self.get_position_degrees())

    def get_velocity_rotations_per_minute(self):
        return (self._motor.velocity(RPM) / (1 / 18)) / self.gear_ratio

    def get_velocity_rotations_per_second(self):
        return self.get_velocity_rotations_per_second() / 60

    def get_velocity_degrees_per_second(self):
        return self.get_velocity_rotations_per_second() * 360

    def get_velocity_radians_per_second(self):
        return math.radians(self.get_velocity_degrees_per_second())
