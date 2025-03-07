from VEXLib.Threading.SafeList import SafeList
from .Constants import FILE_TERMINATION_CHARACTER
from vex import *
import sys

brain = Brain()


class SerialCommunicationProtocol:
    def __init__(self):
        self.incoming_messages = SafeList()
        self.outgoing_messages = SafeList()

        Thread(self.get_loop)
        Thread(self.send_loop)

    def get_loop(self):
        while True:
            self.incoming_messages.append(sys.stdin.readline().strip("\n"))

    def send_loop(self):
        while True:
            if self.has_outgoing_messages():
                sys.stdout.write(str(self.outgoing_messages.pop(0)) + "\n")

    def has_incoming_messages(self):
        return bool(self.incoming_messages)

    def has_outgoing_messages(self):
        return bool(self.outgoing_messages)

    def send(self, message):
        self.outgoing_messages.append(message)

    def receive(self, blocking=False):
        if blocking:
            while not self.has_incoming_messages():
                pass
        if self.has_incoming_messages():
            return self.incoming_messages.pop(0)
        return None

    def peek(self, blocking=False):
        if blocking:
            while not self.has_incoming_messages():
                pass
        if self.has_incoming_messages():
            try:
                return self.incoming_messages[0]
            except IndexError:
                return None
        return None

    def read_file(self):
        file_contents = ""
        self.send("Ready to receive file, waiting for filename")
        while not self.has_incoming_messages():
            pass
        filename = self.receive()
        brain.screen.print("Receiving file: " + filename)
        brain.screen.next_row()
        self.send("Receiving file: " + filename)

        while True:
            chunk = self.receive(True)
            brain.screen.print("Read chunk: " + chunk)
            brain.screen.next_row()

            if FILE_TERMINATION_CHARACTER not in chunk:
                file_contents += chunk + "\n"
            else:
                break
        return filename, file_contents


class HalfDuplexUARTCommunicationProtocol:
    def __init__(self):
        self.incoming_messages = SafeList()
        self.outgoing_messages = SafeList()

        self.file_handle = open("/dev/port20", "rw")
        self.TOKEN_CHARACTER = "TKN"
        self.has_token = False

        Thread(self.get_loop)
        Thread(self.send_loop)

    def get_loop(self):
        while True:
            got = self.file_handle.readline()
            if self.TOKEN_CHARACTER in got:
                self.has_token = True
            if got:
                self.incoming_messages.append(got)

    def send_loop(self):
        while True:
            if self.has_token and self.has_outgoing_messages():
                self.file_handle.write(str(self.outgoing_messages.pop(0)) + self.TOKEN_CHARACTER + "\n")

    def has_incoming_messages(self):
        return bool(self.incoming_messages)

    def has_outgoing_messages(self):
        return bool(self.outgoing_messages)

    def send(self, message):
        self.outgoing_messages.append(message)

    def receive(self, blocking=False):
        if blocking:
            while not self.has_incoming_messages():
                pass
        if self.has_incoming_messages():
            return self.incoming_messages.pop(0)
        return None

    def peek(self, blocking=False):
        if blocking:
            while not self.has_incoming_messages():
                pass
        if self.has_incoming_messages():
            try:
                return self.incoming_messages[0]
            except IndexError:
                return None
        return None

    # def read_file(self):
    #     file_contents = ""
    #     self.send("Ready to receive file, waiting for filename")
    #     while not self.has_incoming_messages():
    #         pass
    #     filename = self.receive()
    #     brain.screen.print("Receiving file: " + filename)
    #     brain.screen.next_row()
    #     self.send("Receiving file: " + filename)
    #
    #     while True:
    #         chunk = self.receive(True)
    #         brain.screen.print("Read chunk: " + chunk)
    #         brain.screen.next_row()
    #
    #         if FILE_TERMINATION_CHARACTER not in chunk:
    #             file_contents += chunk + "\n"
    #         else:
    #             break
    #     return filename, file_contents


class Telemetry:
    def __init__(self):
        # self.serial = SerialCommunicationProtocol()
        self.serial = HalfDuplexUARTCommunicationProtocol()

        self.telemetry_entries: list[TelemetryEntry] = []

    def register_entry(self, entry):
        self.telemetry_entries.append(entry)

    def update(self):
        self.send_message("ROBOT_HEARTBEAT")
        # for entry in self.telemetry_entries:
        #     self.serial.send("TELEMETRY:" + str(entry.name) + "|" + str(entry.get_value()))

    def get_message(self):
        return self.serial.receive(blocking=False)

    def send_message(self, message):
        self.serial.send(message)


class TelemetryEntry:
    def __init__(self, name):
        self.name = name
        self.value = None

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Integer(TelemetryEntry):
    def __init__(self, integer, name):
        super().__init__(name)
        self.value = integer

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return "TelemetryInteger(" + str(self.value) + ")"


class MotorEntry(TelemetryEntry):
    def __init__(self, motor, name):
        super().__init__(name)
        self.motor = motor

    def set_value(self, value):
        raise NotImplementedError("Can't set the value of a Motor entry")

    def get_value(self):
        if self.motor.installed():
            return "Motor running at speed: " + str(self.motor.velocity(PERCENT))
        return "Motor unplugged"


class InertialEntry(TelemetryEntry):
    def __init__(self, inertial, name):
        super().__init__(name)
        self.inertial = inertial

    def set_value(self, value):
        raise NotImplementedError("Can't set the value of an Inertial entry")

    def get_value(self):
        if self.inertial.installed():
            return "Inertial: pitch: " + str(self.inertial.pitch(DEGREES)) + " roll: " + str(self.inertial.roll(DEGREES)) + " yaw: " + str(self.inertial.yaw(DEGREES))
        return "Inertial unplugged"
