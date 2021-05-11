# Standard library imports
from datetime import date
# Local imports
from Src.Components.io import IO
from Src.Components.organizer import Organizer, SettingsAttributes

############################### GLOBALS #####################################
WAV_FILE_PATH = "TestData/media/test2a.wav"
RESULT_DIR_PATH = "TestData"
TMP_DIR_PATH = "TestData/workspace"
CONVERSATION_DIR_PATH = "TestData/media/conversation"

############################### SETUP #####################################

def test_organizer_create_settings_valid() -> None:
    """
    Tests the create_settings method of Organizer.

    Tests:
        1. Create a settings object from valid data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    organizer = Organizer(IO())
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    success , settings = organizer.create_settings(data)
    assert success and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"

def test_organizer_create_settings_invalid() -> None:
    """
    Tests the create_settings method of Organizer.

    Tests:
        1. Attempt to make settings from data with invalid settings data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    organizer = Organizer(IO())
    data_1 = {
        "sample_attribute_1" : "1"}
    data_2 = {
        "sample_attribute_1" : "1",
        "invalid" : 2 }
    assert not organizer.create_settings(data_1)[0] and \
        not organizer.create_settings(data_2)[0]

def test_organizer_copy_settings() -> None:
    """
    Tests the copy_settings method of Organizer.

    Tests:
        1. Copy a valid settings object.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    organizer = Organizer(IO())
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    _ , settings = organizer.create_settings(data)
    copied_settings = organizer.copy_settings(settings)
    assert copied_settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        copied_settings.get(SettingsAttributes.sample_attribute_2)[1] == "2" and \
        settings != copied_settings

def test_organizer_change_settings_valid() -> None:
    """
    Tests the change_settings method of Organizer.

    Tests:
        1. Change a valid settings object and check values.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    organizer = Organizer(IO())
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    changed_data = {
        "sample_attribute_1" : "3",
        "sample_attribute_2" : "4"}
    _ , settings = organizer.create_settings(data)
    assert organizer.change_settings(settings,changed_data) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "3" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "4"

def test_organizer_change_settings_invalid() -> None:
    """
    Tests the change_settings method of Organizer.

    Tests:
        1. Attempt to change settings with invalid data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    organizer = Organizer(IO())
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    changed_data = {
        "sample_attribute_1" : "3",
        "sample_attribute_2" : "4",
        "invalid_key" : "5"}
    _ , settings = organizer.create_settings(data)
    assert not organizer.change_settings(settings,changed_data) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"

def test_organizer_create_conversation_valid() -> None:
    """
    Tests the create_conversation method of Organizer.

    Tests:
        1. Create a conversation with valid data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    organizer = Organizer(IO())
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    _ , settings = organizer.create_settings(data)
    success_1,_ = organizer.create_conversation(
        CONVERSATION_DIR_PATH, "conversation_dir",2,TMP_DIR_PATH,TMP_DIR_PATH,
        settings)
    assert success_1

def test_organizer_apply_settings_to_conversation_valid() -> None:
    """
    Tests the apply_settings_to_conversation method of Organizer.

    Tests:
        1. Create a conversation with valid data.

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    organizer = Organizer(IO())
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"}
    _ , settings = organizer.create_settings(data)
    _, conversation = organizer.create_conversation(
        CONVERSATION_DIR_PATH, "conversation_dir",2,TMP_DIR_PATH,TMP_DIR_PATH,
        settings)
    data_new = {
        "sample_attribute_1" : "3",
        "sample_attribute_2" : "4"}
    _ , settings_new = organizer.create_settings(data_new)
    conversation_new = organizer.apply_settings_to_conversation(
        conversation,settings_new)
    assert conversation_new != conversation