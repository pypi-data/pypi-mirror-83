import os
import sys
import time
from collections import namedtuple
from dynamicmethod import dynamicmethod

from pybk8500.utils import parse_number
from pybk8500.send_cmd import CommunicationManager
from pybk8500 import commands


__all__ = ['parse_number', 'ProfileManager', 'ProfileRow', 'Profile', 'main']


SetRemoteOperation = commands.SetRemoteOperation
LoadSwitch = commands.LoadSwitch
ReadInputVoltageCurrentPowerState = commands.ReadInputVoltageCurrentPowerState
SetMode = commands.SetMode
ReadMode = commands.ReadMode
CommandStatus = commands.CommandStatus


ProfileRow = namedtuple('ProfileRow', ['command', 'value', 'timeout'])


class Profile(list):
    """List of steps for the profile"""

    ProfileRow = ProfileRow
    HEADER = 'Command,Value,Run Time (s)'
    ROW_FORMAT = '{row.command},{row.value},{row.timeout}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.HEADER = self.__class__.HEADER  # Can modify
        self.port = 'COM1'  # Current Com port
        self.baudrate = 38400  # Current BaudRate
        self.sample_timeout = 0.1  # Current Sample timeout
        self.newline = '\r\n'

    def add(self, command, value, timeout=0):
        """Add a profile row."""
        command = self.parse_command(command)
        value = self.parse_value(value)
        timeout = self.parse_timeout(timeout)
        self.append(ProfileRow(command, value, timeout))

    @classmethod
    def parse_command(cls, cmd):
        if isinstance(cmd, str):
            return cmd
        return cmd.__class__.__name__
        # return getattr(commands, cmd, cmd)

    @classmethod
    def parse_value(cls, value):
        return parse_number(value)

    @classmethod
    def parse_timeout(cls, value):
        timeout = parse_number(value)
        if not timeout or isinstance(timeout, str):
            timeout = 0
        return timeout

    def load(self, filename):
        """Load the given profile file."""
        file = filename
        if isinstance(filename, str):
            file = open(filename, 'r')

        try:
            for line in file:
                if line.startswith('#') or line.startswith(';') or ',' not in line:
                    continue

                # Split and Check if header
                cmd, value, timeout = line.split(',', 2)
                if cmd == 'Command' and value == 'Value':
                    continue

                # Add the command row
                self.add(cmd, value, timeout.strip())

        finally:
            try:
                file.close()
            except (AttributeError, Exception):
                pass

    def save(self, filename):
        """Save this profile to a file."""
        file = filename
        if isinstance(filename, str):
            file = open(filename, 'r')

        try:
            file.write(self.HEADER + self.newline)
            for row in self:
                if isinstance(row, self.ProfileRow):
                    file.write(self.ROW_FORMAT.format(row=row) + self.newline)
        finally:
            try:
                file.close()
            except (AttributeError, Exception):
                pass


class ProfileManager(CommunicationManager):
    def setup_remote(self, *args, **kwargs):
        """Start the remote operation and set the load switch to off."""
        # Set to remote (Must start with this command for running remote)
        cmd = SetRemoteOperation(operation='Remote')  # or operation=1
        self.send_wait(cmd, timeout=1, print_recv=True)

        # Set the load Off
        cmd = LoadSwitch(operation='Off')  # or operation=0
        self.send_wait(cmd, timeout=1, print_recv=True)

    def teardown_remote(self, *args, **kwargs):
        """Stop the remote operation to the front panel and set the load switch to off."""
        # Set the load Off
        cmd = LoadSwitch(operation='Off')  # or operation=0
        self.send_wait(cmd, timeout=1, print_recv=True)

        # Set to front panel
        cmd = SetRemoteOperation(operation='Front Panel')  # or operation=1
        self.send_wait(cmd, timeout=1, print_recv=True)

    def __enter__(self):
        super().__enter__()
        if self.is_connected():
            self.setup_remote()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_connected():
            self.teardown_remote()
        return super().__exit__(exc_type, exc_val, exc_tb)

    def __init__(self, connection=None, parser=None, com=None, baudrate=None, **kwargs):
        super().__init__(connection=connection, parser=parser, com=com, baudrate=baudrate, **kwargs)

        self.INTERNAL_COMMANDS = self.__class__.INTERNAL_COMMANDS
        self.saved_results = [None] * 2**24
        self.saved_index = 0
        self.profile = Profile()

        # Internal variables
        self.sample_time = 0.1
        self.output = None

    def print_input(self, msg):
        """The message_parsed callback function that will print ReadInputVoltageCurrentPowerState messages."""
        self.save_ack(msg)

        if isinstance(msg, ReadInputVoltageCurrentPowerState):
            print('{} V, {} A, {} W'.format(msg.voltage, msg.current, msg.power))

    def save_input(self, msg):
        """The message_parsed callback function that will save ReadInputVoltageCurrentPowerState messages."""
        self.save_ack(msg)

        if isinstance(msg, ReadInputVoltageCurrentPowerState):
            if self.saved_index < len(self.saved_results):
                self.saved_results[self.saved_index] = msg
                self.saved_index += 1
            else:
                self.saved_results.append(msg)
                self.saved_index += 1

    def wait_print_input(self, timeout=1, time_delay=0.1):
        """Wait the given timeout while printing the input values.

        Args:
            timeout (float/int): Timeout in seconds
            time_delay (float/int): Time (in seconds) to wait until sending the next request for the input values.
        """
        read_values = ReadInputVoltageCurrentPowerState()

        start = time.time()
        with self.change_message_parsed(self.print_input):
            while (time.time() - start) < timeout:
                self.write(read_values)
                time.sleep(time_delay)

    def wait_save_input(self, timeout=1, time_delay=0.1):
        """Wait the given timeout while saving the results in a list.

        Args:
            timeout (float/int): Timeout in seconds
            time_delay (float/int): Time (in seconds) to wait until sending the next request for the input values.

        Returns:
            msgs (list): List of ReadInputVoltageCurrentPowerState messages.
        """
        read_values = ReadInputVoltageCurrentPowerState()
        self.saved_index = 0

        start = time.time()
        with self.change_message_parsed(self.save_input):
            while (time.time() - start) < timeout:
                self.write(read_values)
                time.sleep(time_delay)

        return self.saved_results[: self.saved_index]

    def load_profile(self, filename):
        """Load the profile"""
        self.profile.load(filename)

    def save_profile(self, filename):
        """Save the set profile."""
        self.profile.save(filename)

    INTERNAL_COMMANDS = {}

    @dynamicmethod
    def register_internal_command(self, command, func=None):
        """Register an internal command callback function.

        Args:
            command (str): Command name in the command column of the CSV.
            func (callable)[None]: Function to call. Function signature (profile_mngr, value, timeout=None)
        """
        if func is None:
            def decorator(f):
                return self.register_internal_command(command, f)
            return decorator

        self.INTERNAL_COMMANDS[command] = func
        return func

    def run_profile(self):
        """Run the set profile."""
        for row in self.profile:
            if row.command in self.INTERNAL_COMMANDS:
                cmd = self.INTERNAL_COMMANDS.get(row.command)
                if callable(cmd):
                    cmd(self, row.value, timeout=row.timeout)
            else:
                cmd_type = getattr(commands, row.command)
                if row.value or isinstance(row.value, int):
                    msg = cmd_type(value=row.value)
                else:
                    msg = cmd_type()
                self.send_wait(msg, timeout=1)

                if row.timeout:
                    self.run_mode(timeout=row.timeout, mode=cmd_type)

    def run_mode(self, value=None, timeout=None, mode=None, *args, **kwargs):
        """Run the given mode (or current mode) for the given timeout while reading the input values.

        If "output" is set save the read inputs to the output file. If no "output" then print the read inputs.

        Steps:
          * Check the current mode and change the mode if needed.
          * Turn on the load
          * Wait the timeout and read input with the set sample_time while saving or printing the output.
          * Turn off Load

        Args:
            value (object)[None]: Optional timeout if timeout is not given.
            timeout (int/float)[None]: Timeout to wait while reading the input.
            mode (str)[None]: Run in this mode. Mode command (Message, CC, CV, CW, CR) or string "CC", "CV", "CW", "CR".
        """
        if timeout is None:
            timeout = value

        try:
            mode = mode.MODE_TYPE
        except (AttributeError, Exception):
            pass

        # Check the current mode
        if isinstance(mode, str):
            current_mode = None
            msgs = self.send_wait(ReadMode(), msg_type=ReadMode, timeout=1, print_msg=False, print_recv=False)
            for msg in msgs:
                if isinstance(msg, ReadMode):
                    current_mode = msg.mode

            # Change the mode if needed
            if mode != current_mode:
                self.send_wait(SetMode(mode=mode), msg_type=CommandStatus, timeout=1, print_msg=False, print_recv=False)

        # Set the load On
        self.send_wait(LoadSwitch(operation=1), timeout=1)

        # Run and wait for messages
        if self.output:
            # If output was set save results to a file
            msgs = self.wait_save_input(timeout, self.sample_time)

            # Check path
            if not os.path.exists(os.path.dirname(self.output)):
                try:
                    os.makedirs(os.path.dirname(self.output), exist_ok=True)
                except:
                    pass

            # Save results
            with open(self.output, 'a') as f:
                f.write('Volts,Amps,Watts\n')
                for msg in msgs:
                    f.write('{} V, {} A, {} W\n'.format(msg.voltage, msg.current, msg.power))
        else:
            # If no output print
            self.wait_print_input(timeout, self.sample_time)

        # Set the load Off
        self.send_wait(LoadSwitch(operation=0), timeout=1)

    def get_sample_rate(self):
        """Return the sampling time delay in hz. The sample rate is (sample_time = 1/value)."""
        return 1/self.sample_time

    def set_sample_rate(self, value, *args, **kwargs):
        """Set the sampling time delay in hz. The sample rate is (sample_time = 1/value)."""
        self.sample_time = 1/value

    def get_sample_time(self):
        """Return the sampling time delay."""
        return self.sample_time

    def set_sample_time(self, value, *args, **kwargs):
        """Set the sampling time delay."""
        self.sample_time = value

    def get_output(self):
        """Return the output file."""
        return self.output

    def set_output(self, output, *args, **kwargs):
        """Set the output file."""
        self.output = output


# Custom internal commands
ProfileManager.register_internal_command('SetupRemote', ProfileManager.setup_remote)
ProfileManager.register_internal_command('TeardownRemote', ProfileManager.teardown_remote)
ProfileManager.register_internal_command('Run', ProfileManager.run_mode)
ProfileManager.register_internal_command('Connect', ProfileManager.connect)
ProfileManager.register_internal_command('SetRTS', ProfileManager.set_rts)
ProfileManager.register_internal_command('SetDTR', ProfileManager.set_dtr)
ProfileManager.register_internal_command('SampleRate', ProfileManager.set_sample_rate)
ProfileManager.register_internal_command('SampleTime', ProfileManager.set_sample_time)
ProfileManager.register_internal_command('BaudRate', ProfileManager.set_baudrate)
ProfileManager.register_internal_command('Com', ProfileManager.set_com)
ProfileManager.register_internal_command('Port', ProfileManager.set_port)
ProfileManager.register_internal_command('Output', ProfileManager.set_output)


@ProfileManager.register_internal_command('Print')
def print_status(mngr=None, value='', *args, **kwargs):
    """Print the Value string."""
    print(value)


def main(filename, com=None, baudrate=None, connection=None, parser=None):
    """Run the given profile."""
    with ProfileManager(com=com, baudrate=baudrate, connection=connection, parser=parser) as mngr:
        mngr.load_profile(filename)
        mngr.run_profile()


if __name__ == '__main__':
    import argparse
    P = argparse.ArgumentParser('Run a profile.')
    P.add_argument('filename', type=str, help='Profile to read and execute.')
    P.add_argument('--com', '-c', type=str, default=None, help='Com port to connect to.')
    P.add_argument('--baudrate', '-b', type=int, default=None, help='Baud rate to connect with.')
    ARGS = P.parse_args()

    main(ARGS.filename, com=ARGS.com, baudrate=ARGS.baudrate)
