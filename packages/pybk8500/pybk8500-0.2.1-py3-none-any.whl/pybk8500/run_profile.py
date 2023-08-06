import sys
import time
from collections import namedtuple
from dynamicmethod import dynamicmethod
from pybk8500.send_cmd import CommunicationManager
from pybk8500 import commands


__all__ = ['parse_number', 'ProfileManager', 'ProfileRow', 'Profile']


SetRemoteOperation = commands.SetRemoteOperation
LoadSwitch = commands.LoadSwitch
ReadInputVoltageCurrentPowerState = commands.ReadInputVoltageCurrentPowerState


UNIT_CONVERT = {
    'T': 10**12, 'Terra': 10**12,
    'G': 10**9, 'Giga': 10**9,
    'M': 10**6, 'Mega': 10**6,
    'k': 10**3, 'kilo': 10**3,
    'c': 10**-2, 'centi': 10**-2,
    'm': 10**-3, 'milli': 10**-3,
    'µ': 10**-6, 'micro': 10**-6,
    'n': 10**-9, 'nano': 10**-9,
    'p': 10**-12, 'pico': 10**-12,
    }


def parse_number(value):
    """Convert the given value to a number"""
    modifier = 1
    unit = ''
    try:
        num, modifier, unit = value.split(' ', 2)
    except (ValueError, TypeError, Exception):
        try:
            num, modifier = value.split(' ', 1)
            modifier, unit = modifier[:-1], modifier[-1]  # Convert ms to m s
        except (ValueError, TypeError, Exception):
            num = value

    # Get the modifier
    modifier = UNIT_CONVERT.get(modifier, modifier)

    # Get the value
    try:
        num = int(num)
    except (ValueError, TypeError, Exception):
        try:
            num = float(num)
        except (ValueError, TypeError, Exception):
            pass

    # Convert the value to normal units
    try:
        num = num * modifier
    except (ValueError, TypeError, Exception):
        pass

    if not isinstance(num, str):
        value = num
    return value, unit


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
        return parse_number(value)[0]

    @classmethod
    def parse_timeout(cls, value):
        timeout = parse_number(value)[0]
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
    def start_remote(self):
        """Start the remote operation and set the load switch to off."""
        # Set to remote (Must start with this command for running remote)
        cmd = SetRemoteOperation(operation='Remote')  # or operation=1
        self.send_wait(cmd, timeout=1, print_recv=True)

        # Set the load Off
        cmd = LoadSwitch(operation='Off')  # or operation=0
        self.send_wait(cmd, timeout=1, print_recv=True)

    def stop_remote(self):
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
            self.start_remote()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_connected():
            self.stop_remote()
        return super().__exit__(exc_type, exc_val, exc_tb)

    def __init__(self, connection=None, parser=None, com=None, baudrate=None, **kwargs):
        super().__init__(connection=connection, parser=parser, com=com, baudrate=baudrate, **kwargs)

        self.INTERNAL_COMMANDS = self.__class__.INTERNAL_COMMANDS
        self.saved_results = [None] * 2**24
        self.saved_index = 0
        self.profile = Profile()

        # Internal variables
        self.sample_time = 0.1

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
                    # Set the load
                    cmd = LoadSwitch(operation=1)
                    self.send_wait(cmd, timeout=1)

                    # Run and wait for messages
                    self.wait_print_input(row.timeout, self.sample_time)

    def set_sample_rate(self, value, **kwargs):
        self.sample_time = 1/value

    def set_sample_time(self, value, **kwargs):
        self.sample_time = value

    def set_baudrate(self, value, **kwargs):
        with self.change_connection():
            self.connection.baudrate = value

    def set_com(self, value, **kwargs):
        with self.change_connection():
            self.connection.port = value

        if not self.is_connected():
            try:
                self.connect()
                self._enter_connected = True
            except Exception as err:
                print('Warning: Could not connect! {}'.format(err), file=sys.stderr)

    set_port = set_com


ProfileManager.register_internal_command('Connect', ProfileManager.connect)
ProfileManager.register_internal_command('SampleRate', ProfileManager.set_sample_rate)
ProfileManager.register_internal_command('SampleTime', ProfileManager.set_sample_time)
ProfileManager.register_internal_command('BaudRate', ProfileManager.set_baudrate)
ProfileManager.register_internal_command('Com', ProfileManager.set_com)
ProfileManager.register_internal_command('Port', ProfileManager.set_port)


@ProfileManager.register_internal_command('Print')
def print_status(mngr, value, **kwargs):
    print(value)


def main(filename, out=None, com=None, baudrate=None):
    """Run the given profile."""
    if out is not None:
        out = open(out, 'w')
        sys.stdout = out

    with ProfileManager(com=com, baudrate=baudrate) as mngr:
        mngr.load_profile(filename)
        mngr.run_profile()

    try:
        sys.stdout = sys.__stdout__
    except (AttributeError, Exception):
        pass
    try:
        out.close()
    except (AttributeError, Exception):
        pass


if __name__ == '__main__':
    import argparse
    P = argparse.ArgumentParser('Run a profile.')
    P.add_argument('filename', type=str, help='Profile to read and execute.')
    P.add_argument('-o', '--out', type=str, default=None, help='Output filename to save to. If None print results.')
    P.add_argument('--com', '-c', type=str, default=None, help='Com port to connect to.')
    P.add_argument('--baudrate', '-b', type=int, default=None, help='Baud rate to connect with.')
    ARGS = P.parse_args()

    main(ARGS.filename, out=ARGS.out, com=ARGS.com, baudrate=ARGS.baudrate)
