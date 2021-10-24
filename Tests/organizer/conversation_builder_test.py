# Standard library imports
from typing import Dict, Any, List
# Local imports
from Src.components.io import IO
from Src.components.organizer import ConversationBuilder, Settings, \
    SettingsBuilder, Conversation, Meta, Paths, DataFile
from Src.components.organizer.conversation_builder import ConversationCreator
from Tests.organizer.vardefs import *

############################### GLOBALS #####################################

############################### SETUP #######################################


class CustomSettings(Settings):

    KEYS = ("attr_1", "attr_2")

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = dict()
        self.configured = False
        for k in self.KEYS:
            if k not in data:
                return
        for k, v in data.items():
            self.data[k] = v
        self.configured = True

    def is_configured(self) -> bool:
        return self.configured

    def has_attribute(self, attr: str) -> bool:
        return attr in self.data

    def set_value(self, attr: str, value: Any) -> bool:
        if attr in self.KEYS:
            self.data[attr] = value
            return True
        return False

    def get_value(self, attr: str) -> Any:
        if attr in self.data:
            return self.data[attr]


class CustomConversationCreator(ConversationCreator):

    def configure(self, test_arg: Any) -> bool:
        return True

    def create_meta(self) -> Meta:
        return Meta()

    def create_data_files(self) -> List[DataFile]:
        return [DataFile()]

    def create_paths(self) -> Paths:
        return Paths()

########################## TEST DEFINITIONS #################################


def test_register_creator() -> None:
    """
    Tests:
        1. Register and check creator
    """
    builder = ConversationBuilder()
    builder.register_creator("custom", CustomConversationCreator())
    assert builder.is_creator("custom")


def test_remove_creator() -> None:
    """
    Tests:
        1. Check that the ConversationCreator is removed.
    """
    builder = ConversationBuilder()
    builder.register_creator("custom", CustomConversationCreator())
    builder.remove_creator("custom")
    assert not builder.is_creator("custom")


def test_is_creator() -> None:
    """
    Tests:
        1. Check valid creator.
        2. Check invalid creator.
    """
    builder = ConversationBuilder()
    builder.register_creator("custom", CustomConversationCreator())
    assert builder.is_creator("custom")
    assert not builder.is_creator("invalid")


def test_build_conversation() -> None:
    """
    Tests:
        1. Register and build a conversation
    """
    builder = ConversationBuilder()
    builder.register_creator("custom", CustomConversationCreator())
    success, _ = builder.build_conversation(
        "custom", ['random'], {}, CustomSettings({
            "attr_1": None, "attr_2": None}))
    assert success
