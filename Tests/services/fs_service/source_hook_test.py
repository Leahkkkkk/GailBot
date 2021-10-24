# Standard library imports
from typing import Dict
# Local imports
from Src.components.io import IO
from Src.components.services import SourceHook
from Tests.services.vardefs import *


############################### SETUP #####################################
SOURCE_NAME = "source"

########################## TEST DEFINITIONS ##################################


def test_save() -> None:
    """
    Tests:
        1. Add one file and save the hook.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    io = IO()
    io.write(
        "{}/{}.txt".format(hook.get_temp_directory_path(), "test"), ["Apple"],
        False)
    hook.save()


def test_cleanup() -> None:
    """
    Tests:
        1. Cleanup a messy environment.
    """
    hook = SourceHook(SOURCE_DIR_PATH, SOURCE_NAME, EMPTY_DIR_PATH)
    io = IO()
    io.write(
        "{}/{}.txt".format(hook.get_temp_directory_path(), "test"), ["Apple"],
        False)
    hook.save()
    hook.cleanup()
