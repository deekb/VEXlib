from vex import Brain


class RobotBase:
    """
    This is the basic representation of a robot
    It has a brain and methods to be called when it's state changes
    """

    def __init__(self, brain: Brain):
        self.brain = brain

    """one-shot callbacks (each is run a maximum of once whenever the robot changes state)"""

    def on_setup(self):
        """Run when the robot first starts up before any other callbacks are scheduled"""

    def on_enable(self):
        """
        Run whenever the robot is enabled while in either autonomous or driver control mode
        This means that this method is also executed when the robot is enabled and is switched from autonomous to driver control mode or vice versa
        """

    def on_disable(self):
        """
        Run whenever the robot is disabled while in either autonomous or driver control mode
        This means that this method is also executed when the robot is disabled and is switched from autonomous to driver control mode or vice versa
        """

    def on_driver_control(self):
        """Run whenever the robot is enabled while in driver control mode or is enabled and switches from autonomous to driver control"""

    def on_driver_control_disable(self):
        """Run whenever the robot is disabled while in driver control mode or is disabled and switches from autonomous to driver control"""

    def on_autonomous(self):
        """Run whenever the robot is enabled while in autonomous mode or is enabled and switches from driver control to autonomous"""

    def on_autonomous_disable(self):
        """Run whenever the robot is disabled while in autonomous mode or is disabled and switches from driver control to autonomous"""

    """Periodic callbacks"""

    def periodic(self):
        """Run periodically approximately 50 times a second (20ms between ticks) no matter the competition mode"""

    def driver_control_periodic(self):
        """Run periodically approximately 50 times a second (20ms between ticks) while driver control is enabled"""

    def autonomous_periodic(self):
        """Run periodically approximately 50 times a second (20ms between ticks) while autonomous is enabled"""

    def enabled_periodic(self):
        """Run periodically approximately 50 times a second (20ms between ticks) while the robot is enabled in either autonomous or driver control mode"""

    def disabled_periodic(self):
        """Run periodically approximately 50 times a second (20ms between ticks) while the robot is disabled in either autonomous or driver control mode"""
