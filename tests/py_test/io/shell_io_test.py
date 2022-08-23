# Standard library imports
import time
# Local imports
from Src.components.io import ShellIO, ShellStatus
from Tests.io.vardefs import *


############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################


def test_shell_io_add_command() -> None:
    """
    Tests the add_command method in ShellIO

    Tests:
        1. Add a valid command.

    Returns:
        (bool): True if successful. False otherwise.
    """
    shell = ShellIO()
    assert shell.add_command("command_1", "pwd", stdout=None, stdin=None)


def test_shell_io_get_status() -> None:
    """
    Tests the get_status method in ShellIO

    Tests:
        1. Add a valid command and check status

    Returns:
        (bool): True if successful. False otherwise.
    """
    shell = ShellIO()
    assert shell.add_command("command_1", "pwd") and \
        shell.get_status("command_1")[1] == ShellStatus.ready


def test_shell_io_run_command() -> None:
    """
    Tests the run_command method in ShellIO

    Tests:
        1. Run a valid command and check status
        3. Run a command that throws an error and check status.

    Returns:
        (bool): True if successful. False otherwise.
    """
    shell = ShellIO()
    shell.add_command("command_1", "pwd")
    _, ready_1 = shell.get_status("command_1")
    shell.run_command("command_1")
    time.sleep(1)
    _, finished_1 = shell.get_status("command_1")
    shell.add_command("command_2", "invalid")
    _, ready_2 = shell.get_status("command_2")
    shell.run_command("command_2")
    time.sleep(1)
    _, error_1 = shell.get_status("command_2")
    assert ready_1 == ShellStatus.ready and \
        finished_1 == ShellStatus.finished and \
        ready_2 == ShellStatus.ready and \
        error_1 == ShellStatus.error
