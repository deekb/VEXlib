from VEXLib.Algorithms.TrapezoidProfile import *
from VEXLib.Algorithms.PIDF import PIDController
from VEXLib.Util import time


class ProfiledPIDController(PIDController):
    def __init__(
        self,
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        t: float = 0.05,
        integral_limit: float = 1.0,
        max_acceleration: float = 1.0,
        max_velocity: float = 1.0
    ):
        super().__init__(kp, ki, kd, t, integral_limit)
        self.constraints = Constraints(max_velocity, max_acceleration)
        self.profile = TrapezoidProfile(self.constraints)
        self.last_time = None
        self.target_state = State()
        self.current_state = State()

    def set_target_state(self, target_position, target_velocity):
        self.target_state = State(target_position, target_velocity)
        self.last_time = None  # Reset the time when a new target is set
        self.profile.goal = self.target_state
        self.current_state = State()

    def update(self, current_value: float) -> float:
        current_time = time.time()
        if self.last_time is None:
            self.last_time = current_time

        elapsed_time = current_time - self.last_time
        self.last_time = current_time

        # Calculate the current state using the trapezoid profile
        self.current_state = self.profile.calculate(elapsed_time, self.current_state, self.target_state)

        # Update the PIDF target value to the current position
        self.setpoint = self.current_state.position

        # Calculate the PID output
        pid_output = super().update(current_value)

        return pid_output

    def is_finished(self):
        current_time = time.time()
        elapsed_time = current_time - (self.last_time if self.last_time else 0)
        return self.profile.is_finished(elapsed_time)
