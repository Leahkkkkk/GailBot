'''
UPDATED: 9/29/21
These tests have been removed because the architecture was changed/
'''

from typing import Dict, Any
from dataclasses import dataclass
# Local imports
from Src.Components.config import BlackBoard, Config, ConfigLoader


#################################### SETUP ##################################

@dataclass
class SystemBlackBoard(BlackBoard):
    pass


class SystemBlackBoardLoader(ConfigLoader):

    def load_blackboard(self, blackboard_data: Dict[str, Dict]) \
            -> SystemBlackBoard:
        return SystemBlackBoard()


########################## TEST DEFINITIONS ##################################

def test_add_loader() -> None:
    config = Config()
    loader = SystemBlackBoardLoader()
    config.add_loader(loader)
    assert loader in config.get_loaders()


def test_load_blackboard() -> None:
    config = Config()
    loader = SystemBlackBoardLoader()
    config.add_loader(loader)
    config.load_blackboard({})


def test_get_loaders() -> None:
    config = Config()
    loader = SystemBlackBoardLoader()
    loader2 = SystemBlackBoardLoader()
    config.add_loader(loader)
    assert loader in config.get_loaders()
    assert not loader2 in config.get_loaders()

# MOTE: These tests have been removed because they are old tests.

# def initialize_data() -> Dict[str, Any]:
#     return {"default_workspace_path": "I am a test string"}

# ########################## TEST DEFINITIONS ##################################


# def test_config_load_into_nonexistent_board() -> None:
#     """
#     Tests loading an invalid blackboard type in Config.

#     Tests:
#         1. Loads data into an undefined blackboard.
#         2. Confirms that load was unsucessful.

#     Result:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     config = Config()
#     assert not config.load_blackboard("notABoard", {"Key": "key"})


# def test_config_load_into_existent_board() -> None:
#     """
#     Tests sucessful load into a valid blackboard type in Config.

#     Tests
#         1. Loads valid data into a defined SystemBB.
#         2. Confirms that load was sucessful.

#     Result:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     config = Config()
#     assert config.load_blackboard("system_blackboard", initialize_data())


# def test_config_load_with_bad_data() -> None:
#     """
#     Tests unsucessful load with invalid data in a valid blackboard type in
#     Config.

#     Tests:
#         1. Loads invalid data into SystemBB.
#         2. Confirms that load was unsucessful.

#     Result:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     config = Config()
#     assert not config.load_blackboard("system_blackboard", {"bad data!"})


# def test_config_load_with_bad_key() -> None:
#     """
#     Tests unsuccessful load with invalid key data in a valid blackboard type in
#     Config.

#     Tests:
#         1. Loads invalid dictionary into SystemBB.
#         2. Confirms that load was unsucessful.

#     Result:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     config = Config()
#     assert not config.load_blackboard("system_blackboard", {"Bad_key": "key"})


# def test_config_get_nonexistent_board() -> None:
#     """
#     Tests get of invalid blackboard type in Config.

#     Tests:
#         1. Gets blackboard with invalid type.
#         2. Confirms get was unsucessful.

#     Result:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     config = Config()
#     assert config.get_blackboard("notABoard") == (False, None)


# def test_config_get_existent_unloaded_board() -> None:
#     """
#     Tests get of unloaded valid blackboard type in Config,

#     Tests:
#         1. Gets unloaded blackboard with valid type.
#         2. Confirms get was unsucessful.

#     Result:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     config = Config()
#     assert config.get_blackboard("system_blackboard") == (False, None)


# def test_config_get_loaded_board() -> None:
#     """
#     Tests sucessful get of loaded valid blackboard type in Config.

#     Tests:
#         1. Loads valid blackboard data in SystemBB.
#         2. Gets SystemBB.
#         3. Confirms get was sucessful and the board was set properly.

#     Result:
#         (bool): True if all the tests pass. False otherwise.
#     """
#     config = Config()
#     config.load_blackboard("system_blackboard", initialize_data())
#     success, system_bb = config.get_blackboard("system_blackboard")
#     assert success and \
#         system_bb.get(SystemBBAttributes.default_workspace_path) == (
#             True, "I am a test string")
