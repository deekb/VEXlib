from VEXLib.Robot.TickBasedRobot import TickBasedRobot
from VEXLib.Util import time
from VEXLib.Math import MathUtil
from VEXLib.Robot.Constants import *


class TimedRobot(TickBasedRobot):
    """
    This class represents a robot with timed control periods.
    It inherits from TickBasedRobot and provides methods to get information about the runtime
    of the robot's control periods and the remaining time for each control period.
    """

    def __init__(self, brain):
        super().__init__(brain)

    def time_since_enable(self):
        """
        Get the elapsed time in seconds from when the robot was last enabled in either driver or autonomous control

        Returns:
            enabled_runtime (float | None): the elapsed time since the robot was last enabled
        """
        return time.time() - self._last_enable_time

    def time_since_disable(self):
        """
        Get the elapsed time in seconds from when the robot was last disabled in either driver or autonomous control

        Returns:
            disabled_runtime (float | None): the elapsed time since the robot was last disabled
        """
        return time.time() - self._last_disable_time

    def get_autonomous_control_runtime(self):
        """
        Get the elapsed time in seconds from the start of autonomous control
        returns None if autonomous is not currently enabled

        Returns:
            autonomous_control_runtime (float | None): the elapsed time since the start of autonomous control, or None if it is not running
        """
        enabled_runtime = self.time_since_enable()
        if self.is_autonomous_control() and self.is_enabled():
            return enabled_runtime
        return None

    def get_driver_control_runtime(self):
        """
        Get the elapsed time in seconds from the start of driver control
        returns None if driver control is not currently enabled

        Returns:
            driver_control_runtime (float | None): the elapsed time since the start of driver control, or None if it is not running
        """
        enabled_runtime = self.time_since_enable()
        if self.is_driver_control() and self.is_enabled():
            return enabled_runtime
        return None

    def get_remaining_driver_control_time(self):
        """
        Get the amount of time remaining in driver control
        returns None if driver control is not currently enabled


        Returns:
            driver_control_time_remaining (float | None): The time remaining in driver control, (0 if no time remains)
        """
        driver_control_runtime = self.get_driver_control_runtime()
        if self.is_driver_control() and self.is_enabled():
            return MathUtil.clamp(DRIVER_CONTROL_TIME_IN_SECONDS - driver_control_runtime, 0.0,
                                  DRIVER_CONTROL_TIME_IN_SECONDS)
        return None

    def get_remaining_autonomous_control_time(self):
        """
        Get the amount of time remaining in autonomous control
        returns None if autonomous is not currently enabled

        Returns:
            autonomous_control_time_remaining (float | None): The time remaining in autonomous control, (0 if no time remains)
        """
        autonomous_control_runtime = self.get_autonomous_control_runtime()
        if self.is_autonomous_control() and self.is_enabled():
            return MathUtil.clamp(AUTONOMOUS_TIME_IN_SECONDS - autonomous_control_runtime, 0.0,
                                  AUTONOMOUS_TIME_IN_SECONDS)
        return None

    def get_remaining_skills_time(self):
        """
        Get the amount of time remaining in a skills run (driver skills or autonomous skills).
        There is no way of determining if skills is running (because it can be either driver control or autonomous)
        so this method will only return None if the robot is disabled

        Returns:
            skills_run_time_remaining (float | None): The time remaining in a skills run, (0 if no time remains) or None if the robot is disabled
        """
        enabled_time = self.time_since_enable()
        if self.is_enabled():
            return MathUtil.clamp(SKILLS_TIME_IN_SECONDS - enabled_time, 0.0, SKILLS_TIME_IN_SECONDS)
        return None
