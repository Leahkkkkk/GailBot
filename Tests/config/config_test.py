'''
UPDATED: 9/29/21
These tests have been removed because the architecture was changed/
'''

from typing import Dict, Any
from dataclasses import dataclass
# Local imports
from Src.components.config import BlackBoard, Config, ConfigLoader


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
    """
    Tests:
        1. Add a valid loader and check if it exists.
    """
    config = Config()
    loader = SystemBlackBoardLoader()
    config.add_loader(loader)
    assert loader in config.get_loaders()


def test_load_blackboard() -> None:
    """
    Tests:
        1. Load data using an existing loader.
    """
    config = Config()
    loader = SystemBlackBoardLoader()
    config.add_loader(loader)
    config.load_blackboard({})


def test_get_loaders() -> None:
    """
    Tests:
        1. Get and verify all existing loaders.
    """
    config = Config()
    loader = SystemBlackBoardLoader()
    loader2 = SystemBlackBoardLoader()
    config.add_loader(loader)
    assert loader in config.get_loaders()
    assert not loader2 in config.get_loaders()
