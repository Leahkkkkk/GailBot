# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-30 17:58:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:08:14
# Standard library imports
import subprocess
from copy import deepcopy
from enum import Enum
from typing import Tuple, Any, Dict, List
# Local imports
from gailbot.utils.threads import ThreadPool
# Third party imports

class ShellStatus(Enum):
    """
    Statuses that a Command object can have.
    """
    ready = "ready"
    running = "running"
    finished = "finished"
    error = "error"


class Command:
    """
    Stores all data associated with a command that can be run as a shell
    command.
    """

    def __init__(self, command: str) -> None:
        """
        Args:
            command (str): Command to run on a shell.

        Params:
            command (str): Command to run on a shell.
            status (ShellStatus): Current status of the command.
            Params (Dict): Stores the params associated with the command and
                            can be passed to subprocess.call
        """
        self.command = command
        self.status = ShellStatus.ready
        # Command flags
        self.params = {
            "shell": True,
            "stdout": None,
            "stdin": None}

    def set_status(self, status: ShellStatus) -> bool:
        """
        Set the current status of the command

        Args:
            status (ShellStatus)

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.status = status
        return True

    def set_flags(self, stdout: Any, stdin: Any) -> bool:
        """
        Set the flags for this command

        Args:
            stdout (Any): Stream for command output
            stdin (Any): Stream for command input.

        Returns:
            (bool): True if successfully set. False otherwise.
        """
        self.params.update({
            "stdout": stdout,
            "stdin": stdin})
        return True

    def get_status(self) -> ShellStatus:
        """
        Obtain the status the command

        Returns:
            (ShellStatus)
        """
        return self.status

    def get_flags(self) -> Dict:
        """
        Returns the flags associated with this command. Can be passed to a
        subprocess.call

        Returns:
            (Dict)
        """
        return deepcopy(self.params)

    def get_command(self) -> str:
        """
        Get the shell command associated with this Command

        Returns:
            (str): shell command associated with this Command
        """
        return self.command


class ShellIO:
    """
    Responsible for running shell commands as sub-processes.
    """

    def __init__(self) -> None:
        """
        Params:
            command (str): Command to run on a shell.
            num_threads (int): No. of threads used by the pool.
            thread_pool (ThreadPool)
        """
        # Needs to maintain reference to running processes.
        self.commands = dict()
        # Threads
        self.num_threads = 10
        self.thread_pool = ThreadPool(self.num_threads)
        self.thread_pool.spawn_threads()

    ################################ SETTERS ###############################

    def add_command(self, identifier: str, command: str,
                    stdout: Any = None, stdin: Any = None) -> bool:
        """
        Add a shell command.

        Args:
            identifier (str): Identifier for this command.
            command (str): Shell command
            stdout (Any): Stream for command output
            stdin (Any): Stream for command input
        """
        cmd = Command(command)
        cmd.set_flags(stdout, stdin)
        self.commands[identifier] = cmd
        return True

    ################################ GETTERS ###############################

    def get_status(self, identifier: str) -> Tuple[bool, ShellStatus]:
        """
        Obtain the status of the shell command associated with this identifier.

        Args:
            identifier (str)

        Returns:
            (Tuple[bool, ShellStatus]): True + status if identifier valid.
                                        False + None if identifier invalid.
        """
        if not identifier in self.commands:
            return (False, None)
        return (True, self.commands[identifier].get_status())

    ################################ OTHERS ###############################

    def run_command(self, identifier: str) -> bool:
        """
        Run the shell command associated with this identifier.

        Args:
            identifier (str)

        Returns:
            (bool): True if command successfully starts running. False otherwise.
        """
        if not identifier in self.commands:
            return False
        flags = self.commands[identifier].get_flags()
        command = self.commands[identifier].get_command()
        cmd = self.commands[identifier]
        self.thread_pool.add_task(
            self._run_command_check_call, [command, flags, [cmd]])
        return True

    ############################### PRIVATE METHODS ########################

    def _run_command_check_call(self, command: str, kwargs: Dict,
                                closure: List[Command]) -> None:
        """
        Run the shell command while checking for exceptions.
        Changes the state of Command object to running, runs the process, and
        changes the state to finished if successfull or error if an
        exception occurs.

        Args:
            command (str): Shell command
            kwargs (Dict): Key-word args for subprocess.check_call
            closure (List[Command]): Contains the Command object associated
                                    with this shell command.
        """
        try:
            closure[0].set_status(ShellStatus.running)
            subprocess.check_call(command, **kwargs)
            closure[0].set_status(ShellStatus.finished)
        except subprocess.CalledProcessError:
            closure[0].set_status(ShellStatus.error)
