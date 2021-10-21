# # Standard library imports
# from typing import Dict, Any, Callable
# # Local imports
# from Src.Components.io import IO
# from Src.Components.organizer import Organizer, Settings
# from Tests.organizer.vardefs import *

# ############################### GLOBALS #####################################

# ############################### SETUP #######################################


# class CustomSettings(Settings):

#     ATTRS = ("attr_1", "attr_2")

#     def __init__(self, data: Dict[str, Any]) -> None:
#         super().__init__(attrs=self.ATTRS)
#         self._parse_data(data)

#     def get_attr_1(self) -> Any:
#         return self.get("attr_1")[1]

#     def get_attr_2(self) -> Any:
#         return self.get("attr_2")[1]

#     def _parse_data(self, data: Dict[str, Any]) -> bool:
#         if not all([k in data.keys() for k in self.ATTRS]):
#             return False
#         for k, v in data.items():
#             self._set_value(k, v)
#         return True


# def settings_creator() -> Callable[[], Settings]:
#     return lambda data: CustomSettings(data)


# ############################### SETUP #####################################

# def test_organizer_register_settings_type() -> None:
#     """
#     Test:
#         1. Register a setting creator.
#         2. Attempt to register the same creator twice.
#     """
#     organizer = Organizer(IO())
#     assert organizer.register_settings_type("custom", settings_creator())
#     assert not organizer.register_settings_type("custom", settings_creator())


# def test_organizer_get_registered_settings_types() -> None:
#     """
#     Test:
#         1. Ensure a registered creator is in list.
#         2. Ensure that the list is empty if nothing is registered.
#     """
#     organizer = Organizer(IO())
#     assert len(organizer.get_registered_settings_types().keys()) == 0
#     assert organizer.register_settings_type("custom", settings_creator())
#     assert "custom" in organizer.get_registered_settings_types().keys()


# def test_organizer_create_settings_valid() -> None:
#     """
#     Tests the create_settings method of Organizer.

#     Tests:
#         1. Create a settings object from valid data.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     organizer = Organizer(IO())
#     organizer.register_settings_type("custom", settings_creator())
#     data = {
#         "attr_1": "1",
#         "attr_2": "2"}
#     success, settings = organizer.create_settings("custom", data)
#     assert success and \
#         settings.get("attr_1")[1] == "1" and \
#         settings.get("attr_2")[1] == "2"


# def test_organizer_create_settings_invalid() -> None:
#     """
#     Tests the create_settings method of Organizer.

#     Tests:
#         1. Attempt to make settings from data with invalid settings data.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     organizer = Organizer(IO())
#     organizer.register_settings_type("custom", settings_creator())
#     data_1 = {
#         "attr_1": "1"}
#     data_2 = {
#         "attr_1": "1",
#         "invalid": 2}
#     assert not organizer.create_settings("custom", data_1)[0] and \
#         not organizer.create_settings("custom", data_2)[0]


# def test_organizer_copy_settings() -> None:
#     """
#     Tests the copy_settings method of Organizer.

#     Tests:
#         1. Copy a valid settings object.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     organizer = Organizer(IO())
#     organizer.register_settings_type("custom", settings_creator())
#     data = {
#         "attr_1": "1",
#         "attr_2": "2"}
#     _, settings = organizer.create_settings("custom", data)
#     copied_settings = organizer.copy_settings(settings)
#     assert copied_settings.get("attr_1")[1] == "1" and \
#         copied_settings.get("attr_2")[1] == "2" and \
#         settings != copied_settings


# def test_organizer_change_settings_valid() -> None:
#     """
#     Tests the change_settings method of Organizer.

#     Tests:
#         1. Change a valid settings object and check values.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     organizer = Organizer(IO())
#     organizer.register_settings_type("custom", settings_creator())
#     data = {
#         "attr_1": "1",
#         "attr_2": "2"}
#     changed_data = {
#         "attr_1": "3",
#         "attr_2": "4"}
#     _, settings = organizer.create_settings("custom", data)
#     assert organizer.change_settings(settings, changed_data) and \
#         settings.get("attr_1")[1] == "3" and \
#         settings.get("attr_2")[1] == "4"


# def test_organizer_change_settings_invalid() -> None:
#     """
#     Tests the change_settings method of Organizer.

#     Tests:
#         1. Attempt to change settings with invalid data.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     organizer = Organizer(IO())
#     organizer.register_settings_type("custom", settings_creator())
#     data = {
#         "attr_1": "1",
#         "attr_2": "2"}
#     changed_data = {
#         "attr_1": "3",
#         "invaid": "4"}
#     _, settings = organizer.create_settings("custom", data)
#     assert not organizer.change_settings(settings, changed_data)
#     assert settings.get("attr_1")[1] == "1"
#     assert settings.get("attr_2")[1] == "2"


# def test_organizer_create_conversation_valid() -> None:
#     """
#     Tests the create_conversation method of Organizer.

#     Tests:
#         1. Create a conversation with valid data.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     organizer = Organizer(IO())
#     organizer.register_settings_type("custom", settings_creator())
#     data = {
#         "attr_1": "1",
#         "attr_2": "2"}
#     _, settings = organizer.create_settings("custom", data)
#     success_1, _ = organizer.create_conversation(
#         CONVERSATION_DIR_PATH, "conversation_dir", 2, "NAME", TMP_DIR_PATH, TMP_DIR_PATH,
#         settings)
#     assert success_1


# def test_organizer_apply_settings_to_conversation_valid() -> None:
#     """
#     Tests the apply_settings_to_conversation method of Organizer.

#     Tests:
#         1. Create a conversation with valid data.

#     Returns:
#         (bool): True if all tests pass. False otherwise.
#     """
#     organizer = Organizer(IO())
#     organizer.register_settings_type("custom", settings_creator())
#     data = {
#         "attr_1": "1",
#         "attr_2": "2"}
#     _, settings = organizer.create_settings("custom", data)
#     _, conversation = organizer.create_conversation(
#         CONVERSATION_DIR_PATH, "conversation_dir", 2, "NAME", TMP_DIR_PATH, TMP_DIR_PATH,
#         settings)
#     data_new = {
#         "attr_1": "3",
#         "attr_2": "4"}
#     _, settings_new = organizer.create_settings("custom", data_new)
#     conversation_new = organizer.apply_settings_to_conversation(
#         conversation, settings_new)
#     assert conversation_new != conversation
