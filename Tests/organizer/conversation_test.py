# Standard library imports
from datetime import date
from typing import Dict, Any, List
# Local imports
from Src.components.io import IO
from Src.components.organizer import ConversationBuilder, SettingsBuilder,\
    Conversation, Settings, ConversationCreator, Meta, DataFile, Paths
from Tests.organizer.vardefs import *


############################### GLOBALS #####################################
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
        meta = Meta()
        meta.conversation_name = "test"
        return meta

    def create_data_files(self) -> List[DataFile]:
        return [DataFile()]

    def create_paths(self) -> Paths:
        return Paths()


############################### SETUP #######################################


########################## TEST DEFINITIONS #################################


def test_valid_conversation() -> None:
    builder = ConversationBuilder()
    builder.register_creator("custom", CustomConversationCreator())
    success, conv = builder.build_conversation(
        "custom", ['random'], {}, CustomSettings({
            "attr_1": None, "attr_2": None}))
    conv: Conversation
    assert conv.get_conversation_name() == "test"
