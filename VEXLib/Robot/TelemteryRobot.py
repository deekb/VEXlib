from VEXLib.Network.Telemetry import Telemetry
from VEXLib.Robot.TickBasedRobot import TickBasedRobot


class TelemetryRobot(TickBasedRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.telemetry = Telemetry()
        self.telemetry_PID_controllers = {}

    def tick_telemetry(self):
        self.telemetry.update()

    # def register_telemetry(self):
    #     objects = self.__dict__
    #     print(objects.items())
    #     for name, _object in objects.items():
    #         if name.startswith("_") or callable(_object):
    #             # Ignore callables and hidden objects
    #             continue
    #         if isinstance(_object, Motor):
    #             self.telemetry.register_entry(MotorEntry(_object, "motor " + name))
    #             motor_port = str(_object)[6:8]
    #             print("Discovered motor: " + name + " on port " + motor_port)
    #         else:
    #             print("Object: " + name + " is of type: " + str(type(_object)))
    #
    # def find_PIDs(self):
    #     objects = self.__dict__
    #     for name, _object in objects.items():
    #         if name.startswith("_") or callable(_object):
    #             # Ignore callables and hidden objects
    #             continue
    #         if isinstance(_object, (PIDController, PIDFController)):
    #             self.telemetry.send_message("Found a compatible PID or PIDF controller, use PID:SET:" + name + ":<property>:<value> to interact with it")
    #             self.telemetry_PID_controllers[name] = _object
    #
    # def set_PID_property(self, PID_name, PID_property_name, PID_property_value):
    #     if PID_name not in self.telemetry_PID_controllers:
    #         self.find_PIDs()
    #         if PID_name not in self.telemetry_PID_controllers:
    #             self.telemetry.send_message("No compatible PID or PIDF controller, named: " + PID_name)
    #             return
    #     PID_controller = self.telemetry_PID_controllers[PID_name]
    #     setattr(PID_controller, PID_property_name, PID_property_value)
    #     self.telemetry.send_message("Successfully set PID or PIDF controller parameter")


