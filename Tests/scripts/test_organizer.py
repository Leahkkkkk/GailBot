"""
Testing for the organizer component
"""
# Standard library imports 
from datetime import date, datetime
# Local imports 
from Src.Components.io import IO
from Src.Components.organizer import Paths, PathsAttributes, Settings, \
        SettingsAttributes, SettingsBuilder, DataFile ,DataFileAttributes, \
        DataFileTypes, Meta, MetaAttributes, ConversationBuilder, Conversation,\
        Organizer
from ..suites import TestSuite
# Third party imports 

############################### GLOBALS #####################################
WAV_FILE_PATH = "Test_files/Media/test2a.wav"
RESULT_DIR_PATH = "Test_files"
TMP_DIR_PATH = "Test_files/Others/Test-directory"
CONVERSATION_DIR_PATH = "Test_files/Media/Conversation"

########################## TEST DEFINITIONS ##################################


######################### Paths tests

def paths_create_valid_data() -> bool:
    """
    Tests the paths object. 

    Tests:
        1. Create a paths object with valid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    paths_data = {
        "result_dir_path" : RESULT_DIR_PATH,
        "source_path" : WAV_FILE_PATH, 
        "data_file_paths" : [],
        "temp_dir_path" : TMP_DIR_PATH}
    paths = Paths(paths_data)
    return paths.is_configured()

def paths_create_invalid_data() -> bool:
    """
    Tests the paths object. 

    Tests:
        1. Create a paths object with invalid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise   
    """
    paths_data = {
        "result_dir_path" : RESULT_DIR_PATH,
        "source_path" : WAV_FILE_PATH}
    paths = Paths(paths_data)
    return not paths.is_configured() 

def paths_get_valid() -> bool:
    """
    Tests the get method of Paths

    Tests:
        1. Obtain a valid attribute data 

    Returns:
        (bool): True if all tests pass. False otherwise 
    """
    paths_data = {
        "result_dir_path" : RESULT_DIR_PATH,
        "source_path" : WAV_FILE_PATH, 
        "data_file_paths" : [],
        "temp_dir_path" : TMP_DIR_PATH}
    paths = Paths(paths_data)
    return paths.is_configured() and \
        paths.get(PathsAttributes.result_dir_path)[1] == RESULT_DIR_PATH and \
        paths.get(PathsAttributes.temp_dir_path)[1] == TMP_DIR_PATH

def paths_get_invalid() -> bool:
    """
    Tests the get method of Paths

    Tests:
        1. Obtain an invalid attribute data 

    Returns:
        (bool): True if all tests pass. False otherwise 
    """
    paths_data = {
        "result_dir_path" : RESULT_DIR_PATH,
        "source_path" : WAV_FILE_PATH, 
        "data_file_paths" : [],
        "temp_dir_path" : TMP_DIR_PATH}
    paths = Paths(paths_data)
    return paths.is_configured() and \
        not paths.get("invalid")[0] 


#########################  Settings tests

def settings_create_valid_data() -> bool:
    """
    Tests the settings object. 

    Tests:
        1. Create a settings object with valid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise   
    """
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    settings = Settings(data)
    return settings.is_configured()

def settings_create_invalid_data() -> bool:
    """
    Tests the settings object. 

    Tests:
        1. Create a settings object with invalid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise   
    """
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None,
        "bad_attribute_1" : None} 
    settings = Settings(data)
    return settings.is_configured()

def settings_create_invalid_data_missing_keys() -> bool:
    """
    Tests the settings object.

    Test:
        1. Create a settings object with invalid missing keys data and 
           confirm it is not configured

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "sample_attribute_1" : None}
    settings = Settings(data)
    return not settings.is_configured()

def settings_create_invalid_data_misnamed_keys() -> bool:
    """
    Tests the settings object.

    Test:
        1. Create a settings object with misnamed keys data and 
           confirm it is not configured

    Returns:
        (bool): True if all tests pass. False otherwise
    """
    data = {
        "sample_attribute_1" : None,
        "sample_attribute" : None}
    settings = Settings(data)
    return not settings.is_configured()

def settings_set_attribute_manually() -> bool:
    """
    Tests the set method for settings. 

    Tests:
        1. Attempt to set a settings attribute, which should not be possible.

    Returns:
        (bool): True if all tests pass. False otherwise. 
    """
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    settings = Settings(data)
    return not settings.set(SettingsAttributes,None) and \
          not settings.set("invalid", "1")    

def settings_get_valid() -> bool:
    """
    Tests the get method of Settings

    Tests:
        1. Obtain an valid attribute data 

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"} 
    settings = Settings(data)
    return settings.is_configured() and \
        settings.get(SettingsAttributes.sample_attribute_1)[0] and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[0] and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"

def settings_get_invalid() -> bool:
    """
    Tests the get method of Settings

    Tests:
        1. Obtain an invalid attribute data 

    Returns:
        (bool): True if all tests pass. False otherwise 
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"} 
    settings = Settings(data)
    return settings.is_configured() and \
        not settings.get("invalid")[0]


######################### Settings builder tests

def settings_builder_create_settings_valid() -> bool:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes valid data to the builder.
        2. Check the constructed object for data. 
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"} 
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    return success and \
        type(settings) == Settings and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"


def settings_builder_create_settings_invalid() -> bool:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid data to the builder
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data_1 = {
        "sample_attribute_1" : "1"} 
    data_2 = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2",
        "additional" : "3"} 
    builder = SettingsBuilder()
    success_1, settings_1 = builder.create_settings(data_1)
    success_2, settings_2 = builder.create_settings(data_2)
    return not success_1 and \
        not success_2 and \
        settings_1 == None and \
        settings_2 == None

def settings_builder_create_settings_invalid_missing_keys() -> bool:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid missing keys data to the builder
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1"} 
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    return not success and settings == None

def settings_builder_create_settings_invalid_extra_keys() -> bool:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid extra keys data to the builder
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2",
        "additional" : "3"} 
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    return not success and settings == None

def settings_builder_create_settings_invalid_misnamed_keys() -> bool:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid misnamed keys data to the builder
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute" : "2"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    return not success and settings == None

def settings_builder_create_settings_invalid_empty() -> bool:
    """
    Tests the create_settings method in SettingsBuilder

    Tests:
        1. Passes invalid empty data to the builder
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    return not success and settings == None

def settings_builder_copy_settings() -> bool:
    """
    Tests the copy_settings method in SettingsBuilder

    Tests:
        1. Copy the settings object and check attributes for equality. 

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"} 
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    copied_settings = builder.copy_settings(settings) 
    return success and \
        settings != copied_settings and \
        settings.get(SettingsAttributes.sample_attribute_1) == \
            copied_settings.get(SettingsAttributes.sample_attribute_1) and \
        settings.get(SettingsAttributes.sample_attribute_2) == \
            copied_settings.get(SettingsAttributes.sample_attribute_2)

def settings_builder_copy_settings_not_configured() -> bool:
    """
    Tests the copy_settings method in SettingsBuilder

    Tests:
        1. Copy the settings object after settings is not configured, confirms
           the create does no succeed and the copied settings does not throw
           error

    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : "1"}
    builder = SettingsBuilder()
    success, settings = builder.create_settings(data)
    copied_settings = builder.copy_settings(settings)
    return not success and \
        copied_settings == None 

def settings_builder_change_settings_valid() -> bool:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Change settings of only some attributes.
        2. Chaneg settings of all attributes. 
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """ 
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"} 
    new_data_1 = {
        "sample_attribute_1" : "3"}
    new_data_2 = {
        "sample_attribute_1" : "4",
        "sample_attribute_2" : "5"}
    builder = SettingsBuilder()
    _, settings = builder.create_settings(data)
    copied_1 = builder.copy_settings(settings)
    copied_2 = builder.copy_settings(settings)
    builder.change_settings(copied_1, new_data_1)
    builder.change_settings(copied_2, new_data_2)
    return copied_1 != copied_2 and \
        copied_1.get(SettingsAttributes.sample_attribute_1)[1] == "3" and \
        copied_1.get(SettingsAttributes.sample_attribute_2)[1] == "2" and \
        copied_2.get(SettingsAttributes.sample_attribute_1)[1] == "4" and \
        copied_2.get(SettingsAttributes.sample_attribute_2)[1] == "5"    

def settings_builder_change_settings_invalid() -> bool:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Pass data with all invalid keys 
        2. Pass data with some invalid keys. 
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """ 
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"} 
    invalid_data_1 = {
        "sample_attribute_1" : "1",
        "invalid" : None}
    invalid_data_2 = {
        "invalid" : None }
    builder = SettingsBuilder()
    _, settings = builder.create_settings(data)
    return not builder.change_settings(settings, invalid_data_1) and \
        not builder.change_settings(settings,invalid_data_2) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"

def settings_builder_change_settings_empty() -> bool:
    """
    Tests the change_settings method in SettingsBuilder

    Tests:
        1. Pass empty data to change settings
        2. Confirm no data is changed
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """ 
    data = {
        "sample_attribute_1" : "1",
        "sample_attribute_2" : "2"} 
    invalid_data = {}
    builder = SettingsBuilder()
    _, settings = builder.create_settings(data)
    return builder.change_settings(settings, invalid_data) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"

######################### Datafile tests

def create_data_file_valid() -> bool:
    """
    Tests the DataFile object. 

    Tests:
        1. Create a paths object with valid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : DataFileTypes.audio, 
        "path" : "test_path",
        "size_bytes": 0}
    data_file = DataFile(data)
    return data_file.is_configured()


def create_data_file_invalid() -> bool:
    """
    Tests the DataFile object. 

    Tests:
        1. Create a paths object with invalid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    data_1 = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : "blah",
        "path" : "test_path",
        "size_bytes": 0}
    data_2 = {
        "name" : "test_name"}
    data_3 = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : "blach", 
        "path" : "test_path",
        "size_bytes": 0,
        "extra" : None}
    data_file_1 = DataFile(data_1)
    data_file_2 = DataFile(data_2)
    data_file_3 = DataFile(data_3)
    return not data_file_1.is_configured() and \
        not data_file_2.is_configured() and \
        not data_file_3.is_configured()

def create_data_file_invalid_bad_file_type() -> bool:
    """
    Tests the DataFile object. 

    Tests:
        1. Create a paths object with invalid bad file type data and 
           determine if it is configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : "blah",
        "path" : "test_path",
        "size_bytes": 0}
    data_file = DataFile(data)
    return not data_file.is_configured()

def create_data_file_invalid_missing_keys() -> bool:
    """
    Tests the DataFile object. 

    Tests:
        1. Create a paths object with invalid missing keys data and determine 
           if it is configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    data = {
        "name" : "test_name"}
    data_file = DataFile(data)
    return not data_file.is_configured()

def create_data_file_invalid_extra_keys() -> bool:
    """
    Tests the DataFile object. 

    Tests:
        1. Create a paths object with invalid extra keys data and 
           determine if it is configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : "blach", 
        "path" : "test_path",
        "size_bytes": 0,
        "extra" : None}
    data_file = DataFile(data)
    return not data_file.is_configured()

def create_data_file_invalid_empty() -> bool:
    """
    Tests the DataFile object. 

    Tests:
        1. Create a paths object with invalid empty data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    data = {}
    data_file = DataFile(data)
    return not data_file.is_configured()

def data_file_get_valid() -> bool:
    """
    Tests the get method in DataFile. 

    Tests:
        1. Get a valid attribute 

    Returns:
        (bool): True if all tests pass. False otherwise    
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : DataFileTypes.audio,
        "path" : "test_path",
        "size_bytes": 0}
    data_file = DataFile(data)
    return data_file.get(DataFileAttributes.name)[1] == "test_name" and \
        data_file.get(DataFileAttributes.extension)[1] == "wav" and \
        data_file.get(DataFileAttributes.file_type)[1] == DataFileTypes.audio and \
        data_file.get(DataFileAttributes.path)[1] == "test_path" and \
        data_file.get(DataFileAttributes.size_bytes)[1] == 0

def data_file_get_invalid() -> bool:
    """
    Tests the get method in DataFile. 

    Tests:
        1. Get a invalid attribute 

    Returns:
        (bool): True if all tests pass. False otherwise.  
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : DataFileTypes.audio,
        "path" : "test_path", 
        "size_bytes": 0}
    data_file = DataFile(data)
    return not data_file.get("invalid")[0]

def data_file_set_valid() -> bool:
    """
    Test the set method in DataFile.

    Tests:
        1. Set a valid attribute and check result. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : DataFileTypes.audio,
        "path" : "test_path", 
        "size_bytes": 0}
    data_file = DataFile(data)
    return  data_file.set(DataFileAttributes.name,"new_name") and \
        data_file.get(DataFileAttributes.name)[1] == "new_name"

def data_file_set_invalid() -> bool:
    """
    Test the set method in DataFile.

    Tests:
        1. Set an invalid attribute and check results. 
        2. Set an invalid type for file_type. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : DataFileTypes.audio, 
        "path" : "test_path",
        "size_bytes": 0}
    data_file = DataFile(data)
    return  not data_file.set("invalid", None) and \
        not data_file.set(DataFileAttributes.file_type,"audio")

def data_file_set_invalid_bad_key() -> bool:
    """
    Test the set method in DataFile.

    Tests:
        1. Set an invalid attribute and check results. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : DataFileTypes.audio, 
        "path" : "test_path",
        "size_bytes": 0}
    data_file = DataFile(data)
    return not data_file.set("invalid", None)

def data_file_set_invalid_file_type() -> bool:
    """
    Test the set method in DataFile.

    Tests:
        1. Set an invalid type for file_type. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "name" : "test_name", 
        "extension" : "wav", 
        "file_type" : DataFileTypes.audio, 
        "path" : "test_path",
        "size_bytes": 0}
    data_file = DataFile(data)
    return not data_file.set(DataFileAttributes.file_type,"audio") and \
        data_file.get(DataFileAttributes.file_type)[1] == DataFileTypes.audio

######################### Meta tests

def create_meta_valid() -> bool:
    """
    Tests the Meta object. 

    Tests:
        1. Create a meta object with valid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """ 
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    return meta.is_configured()

def create_meta_invalid() -> bool:
    """
    Tests the Meta object. 

    Tests:
        1. Create a meta object with invalid data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data_1 = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    data_2 = {
        "conversation_name" : "test_conversation"}
    data_3 = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1,
        "extra" : None}
    meta_1 = Meta(data_1)
    meta_2 = Meta(data_2)
    meta_3 = Meta(data_3)
    return meta_1.is_configured() and \
        not meta_2.is_configured() and \
        not meta_3.is_configured()

def create_meta_invalid_missing_keys():
    """
    Tests the Meta object. 

    Tests:
        1. Create a meta object with invalid missing data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation"}
    meta = Meta(data)
    return not meta.is_configured()

def create_meta_invalid_extra_keys():
    """
    Tests the Meta object. 

    Tests:
        1. Create a meta object with invalid extra data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1,
        "extra" : None}
    meta = Meta(data)
    return not meta.is_configured()

def create_meta_invalid_empty():
    """
    Tests the Meta object. 

    Tests:
        1. Create a meta object with invalid empty data and determine if it is 
            configured.
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    data = {}
    meta = Meta(data)
    return not meta.is_configured()

def meta_get_valid() -> bool:
    """
    Tests the get method in Meta.

    Tests:
        1. Get a valid attribute 

    Returns:
        (bool): True if all tests pass. False otherwise   
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    return meta.get(MetaAttributes.conversation_name)[1] == "test_conversation" and \
        meta.get(MetaAttributes.total_size_bytes)[1] == 0 and \
        meta.get(MetaAttributes.total_speakers)[1] == 1 and \
        meta.get(MetaAttributes.source_type)[1] == "file" and \
        meta.get(MetaAttributes.transcription_status)[1] =="not_transcribed" and \
        meta.get(MetaAttributes.transcription_date)[1] == None and \
        meta.get(MetaAttributes.transcription_time)[1] == None

def meta_get_invalid() -> bool:
    """
    Tests the get method in Meta. 

    Tests:
        1. Get a invalid attribute 

    Returns:
        (bool): True if all tests pass. False otherwise.  
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    return not meta.get("invalid")[0] 

def meta_set_valid() -> bool:
    """
    Test the set method in Meta

    Tests:
        1. Set a valid attribute and check result. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    return meta.set(MetaAttributes.total_speakers, 10) and \
        meta.get(MetaAttributes.total_speakers)[1] == 10 

def meta_set_invalid() -> bool:
    """
    Test the set method in Meta.

    Tests:
        1. Set an invalid attribute and check results. 
        2. Set an invalid type for file_type. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "conversation_name" : "test_conversation",
        "total_size_bytes" : 0,
        "num_data_files" : 0,
        "source_type" : "file", 
        "transcription_date" : None,
        "transcription_status" : "not_transcribed",
        "transcription_time" : None,
        "total_speakers" : 1}
    meta = Meta(data)
    return not meta.set("invalid", None) 

#########################  Conversation builder tests

def builder_set_conversation_source_path_valid() -> bool:
    """
    Tests the set_conversation_source_path method in ConversationBuilder

    Tests:
        1. Set a valid file path.
        2. Set a valid directory path.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    return builder.set_conversation_source_path(WAV_FILE_PATH) and \
        builder.set_conversation_source_path(CONVERSATION_DIR_PATH)

def builder_set_conversation_source_path_invalid() -> bool:
    """
    Tests the set_conversation_source_path method in ConversationBuilder

    Tests:
        1. Set an invalid path.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    return not builder.set_conversation_source_path("Not a path")

def builder_set_conversation_name() -> bool:
    """
    Tests the set_conversation_name method in ConversationBuilder

    Tests:
        1. Set any random name. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())
    return builder.set_conversation_name("conversation_1")
 
def builder_set_result_directory_path_valid() -> bool:
    """
    Tests the set_result_directory_path method in ConversationBuilder

    Tests:
        1. Set a valid directory path.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())  
    return builder.set_result_directory_path(TMP_DIR_PATH)

def builder_set_result_directory_path_invalid() -> bool:
    """
    Tests the set_result_directory_path method in ConversationBuilder

    Tests:
        1. Set a file path as directory.
        2. Set an invalid path. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())  
    return not builder.set_result_directory_path(WAV_FILE_PATH) and \
        not builder.set_result_directory_path("invalid/")

def builder_set_temporary_directory_path_valid() -> bool:
    """
    Tests the set_temporary_directory_path method in ConversationBuilder

    Tests:
        1. Set a valid directory path.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())  
    return builder.set_temporary_directory_path(TMP_DIR_PATH)

def builder_set_temporary_directory_path_invalid() -> bool:
    """
    Tests the set_temporary_directory_path method in ConversationBuilder

    Tests:
        1. Set a file path as directory.
        2. Set an invalid path. 

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())  
    return not builder.set_temporary_directory_path(WAV_FILE_PATH) and \
        not builder.set_temporary_directory_path("invalid/")

def builder_set_number_of_speakers_valid() -> bool:
    """
    Tests the set_number_of_speakers method in ConversationBuilder

    Tests:
        1. Set a positive number of speakers.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())  
    return builder.set_number_of_speakers(10)


def builder_set_number_of_speakers_invalid() -> bool:
    """
    Tests the set_number_of_speakers method in ConversationBuilder

    Tests:
        1. Set 0 as number of speakers.
        2. Set a negative number of speakers.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    builder = ConversationBuilder(IO())  
    return not builder.set_number_of_speakers(0) and \
        not builder.set_number_of_speakers(-10) 

def builder_set_conversation_settings_valid() -> bool:
    """
    Tests the set_conversation_settings method in ConversationBuilder

    Tests:
        1. Set a settings object that has all attributes set.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    settings = Settings(data)
    builder = ConversationBuilder(IO())  
    return builder.set_conversation_settings(settings)

def builder_set_conversation_settings_invalid() -> bool:
    """
    Tests the set_conversation_settings method in ConversationBuilder

    Tests:
        1. Set a settings object that is not configured.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    data = {
        "sample_attribute_1" : None} 
    settings = Settings(data)
    builder = ConversationBuilder(IO())  
    return not builder.set_conversation_settings(settings)

def builder_build_conversation_valid() -> bool:
    """
    Tests the build_conversation method in ConversationBuilder

    Tests:
        1. Call method after setting all attributes with valid data.

    Returns:   
        (bool): True if all tests pass. False otherwise.
    """
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())  
    builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    builder.set_conversation_name("conversation_1")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_conversation_settings(settings)
    return builder.build_conversation()
    
def builder_build_conversation_invalid() -> bool:
    """
    Tests the build_conversation method of ConversationBuilder.

    Tests:
        1. Build a conversation without setting any attributes.
        2. Build a conversation after setting only some attributes. 
        3. Build a conversation after clearing configurations.
        4. Build a conversation after building a valid conversation.

    Returns:   
        (bool): True if all tests pass. False otherwise.   
    """
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())  

    return not builder.build_conversation() and \
        builder.get_conversation() == None and \
        builder.set_conversation_source_path(CONVERSATION_DIR_PATH) and \
        builder.set_conversation_name("only some attributes set") and \
        not builder.build_conversation() and \
        builder.get_conversation() == None and \
        builder.clear_conversation_configurations() and \
        builder.set_conversation_source_path(CONVERSATION_DIR_PATH) and \
        builder.set_conversation_name("conversation_1") and \
        builder.set_result_directory_path(TMP_DIR_PATH) and \
        builder.set_temporary_directory_path(TMP_DIR_PATH) and \
        builder.set_number_of_speakers(2) and \
        builder.set_conversation_settings(settings) and \
        builder.build_conversation() and \
        builder.get_conversation() != None and \
        builder.clear_conversation_configurations() and \
        not builder.build_conversation() and \
        builder.get_conversation() == None

def builder_clear_conversation() -> bool:
    """
    Tests the builder clear conversation method

    Tests:
        1. Builds conversation
        2. Clear conversation
        3. Confirms conversation is cleared with a get
    
    Returns:
        (bool): True if all tests pass. False otherwise.
    """
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())  
    builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    builder.set_conversation_name("conversation_1")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_conversation_settings(settings)
    builder.build_conversation()
    return builder.clear_conversation_configurations() and builder.get_conversation() == None
 
#########################  Conversation tests

def build_valid_conversation_from_directory() -> Conversation:
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())  
    builder.set_conversation_source_path(CONVERSATION_DIR_PATH)
    builder.set_conversation_name("conversation_dir")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_conversation_settings(settings)
    builder.build_conversation()
    return builder.get_conversation()

def build_valid_conversation_from_file():
    settings_builder = SettingsBuilder()
    data = {
        "sample_attribute_1" : None,
        "sample_attribute_2" : None} 
    _,settings = settings_builder.create_settings(data)
    builder = ConversationBuilder(IO())  
    builder.set_conversation_source_path(WAV_FILE_PATH)
    builder.set_conversation_name("conversation_file")
    builder.set_result_directory_path(TMP_DIR_PATH)
    builder.set_temporary_directory_path(TMP_DIR_PATH)
    builder.set_number_of_speakers(2)
    builder.set_conversation_settings(settings)
    builder.build_conversation()
    return builder.get_conversation() 

def conversation_get_conversation_name() -> bool:
    """
    Tests the get_conversation_name method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Check value of the returned name.

     Returns:   
        (bool): True if all tests pass. False otherwise.   
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.get_conversation_name() == "conversation_dir" and \
        conversation_file.get_conversation_name() == "conversation_file"

def conversation_get_conversation_size() -> bool:
    """
    Tests the get_conversation_size method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Check value of the returned size.

     Returns:   
        (bool): True if all tests pass. False otherwise.   
    """
    io = IO()
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.get_conversation_size() == \
            io.get_size(CONVERSATION_DIR_PATH)[1] and \
        conversation_file.get_conversation_size() == io.get_size(WAV_FILE_PATH)[1]
     
def conversation_get_source_type() -> bool:
    """
    Tests the get_source_type method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Check value of the returned types.

     Returns:   
        (bool): True if all tests pass. False otherwise.   
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.get_source_type() == "directory" and \
        conversation_file.get_source_type() == "file"

def conversation_get_transcription_date() -> bool:
    """
    Tests the get_transcription_date method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the date is a valid date object. 

     Returns:   
        (bool): True if all tests pass. False otherwise.   
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.get_transcription_date() == date.today() and \
        conversation_file.get_transcription_date() == date.today()

def conversation_get_transcription_status() -> bool:
    """
    Tests the get_transcription_status method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the status is ready in both cases.

     Returns:   
        (bool): True if all tests pass. False otherwise.  
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.get_transcription_status() == "ready" and \
        conversation_file.get_transcription_status() == "ready"

def conversation_get_transcription_time() -> bool:
    """
    Tests the get_transcription_times method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the time is valid.

     Returns:   
        (bool): True if all tests pass. False otherwise.  
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return type(conversation_dir.get_transcription_time()) == str and \
        type(conversation_dir.get_transcription_time()) == str

def conversation_number_of_source_files() -> bool:
    """
    Tests the number_of_source_files method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the numbder of files is valid.

     Returns:   
        (bool): True if all tests pass. False otherwise.  
    """ 
    io = IO()
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.number_of_source_files() == \
            io.number_of_files_in_directory(CONVERSATION_DIR_PATH,["*"],False)[1] and \
        conversation_file.number_of_source_files() == 1

def conversation_number_of_speakers() -> bool:
    """
    Tests the number_of_speakers method of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the numbder of speakers is valid.

     Returns:   
        (bool): True if all tests pass. False otherwise.  
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.number_of_speakers() == 2 and \
        conversation_file.number_of_speakers() == 2  

def conversation_get_source_file_names() -> bool:
    """
    Tests the get_source_file_names of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the names are valid. 

     Returns:   
        (bool): True if all tests pass. False otherwise.  
    """
    io = IO()
    dir_paths = io.path_of_files_in_directory(CONVERSATION_DIR_PATH,["*"],False)[1]
    dir_names = [io.get_name(path) for path in dir_paths]
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file()
    return conversation_dir.get_source_file_names() == dir_names and \
        conversation_file.get_source_file_names() == [io.get_name(WAV_FILE_PATH)]
    
def conversation_get_source_file_paths() -> bool:
    """
    Tests the get_source_file_paths of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the paths are valid.

     Returns:   
        (bool): True if all tests pass. False otherwise.  
    """
    io = IO()
    dir_paths = io.path_of_files_in_directory(CONVERSATION_DIR_PATH,["*"],False)[1]
    dir_names = [io.get_name(path) for path in dir_paths]
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file() 
    return list(conversation_dir.get_source_file_paths().values()) == dir_paths and \
        list(conversation_dir.get_source_file_paths().keys()) == dir_names and \
        list(conversation_file.get_source_file_paths().values()) == [WAV_FILE_PATH] and \
        list(conversation_file.get_source_file_paths().keys()) == [io.get_name(WAV_FILE_PATH)]

def conversation_get_source_file_types() -> bool:
    """
    Tests the get_source_file_types of Conversation object returned by 
    ConversationBuilder.

    Tests:
        1. Make sure the types are valid.

    Returns:   
        (bool): True if all tests pass. False otherwise.  
    """
    conversation_dir = build_valid_conversation_from_directory()
    conversation_file = build_valid_conversation_from_file() 
    return list(conversation_dir.get_source_file_types().values()) == ["audio","audio"] and \
        list(conversation_file.get_source_file_types().values()) == ["audio"]
     
######################### Organizer tests 

def organizer_create_settings_valid() -> bool:
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
    return success and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"  

def organizer_create_settings_invalid() -> bool:
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
    return not organizer.create_settings(data_1)[0] and \
        not organizer.create_settings(data_2)[0]

def organizer_copy_settings() -> bool:
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
    return copied_settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        copied_settings.get(SettingsAttributes.sample_attribute_2)[1] == "2" and \
        settings != copied_settings

def organizer_change_settings_valid() -> bool:
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
    return organizer.change_settings(settings,changed_data) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "3" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "4"  

def organizer_change_settings_invalid() -> bool:
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
    return not organizer.change_settings(settings,changed_data) and \
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1" and \
        settings.get(SettingsAttributes.sample_attribute_2)[1] == "2"  

def organizer_create_conversation_valid() -> bool:
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
    return success_1

def organizer_apply_settings_to_conversation_valid() -> bool:
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
    return conversation_new != conversation

####################### TEST SUITE DEFINITION ################################

def define_organizer_test_suite() -> TestSuite:
    """
    Creates a test suite for io and adds tests to the suite.

    Returns:
        (TestSuite): Suite containing network tests
    """
    suite = TestSuite()

    #### Paths tests 
    suite.add_test("paths_create_valid_data", (), True, True, 
        paths_create_valid_data)
    suite.add_test("paths_create_invalid_data", (), True, True, 
        paths_create_invalid_data)
    suite.add_test("paths_get_valid", (), True, True, 
        paths_get_valid)
    suite.add_test("paths_get_invalid", (), True, True, 
        paths_get_invalid)

    # ### Settings tests
    suite.add_test("settings_create_valid_data", (), True, True, 
        settings_create_valid_data)
    suite.add_test("settings_create_invalid_data", (), True, True, 
        settings_create_invalid_data)
    suite.add_test("settings_create_invalid_data_missing_keys", (), True, True, 
        settings_create_invalid_data_missing_keys)
    suite.add_test("settings_create_invalid_data_misnamed_keys", (), True, True, 
        settings_create_invalid_data_misnamed_keys)
    suite.add_test("settings_set_attribute_manually", (), True, True, 
        settings_set_attribute_manually)
    suite.add_test("settings_get_valid", (), True, True, 
        settings_get_valid)
    suite.add_test("settings_get_invalid", (), True, True, 
        settings_get_invalid)

    #### Settings Builder tests
    suite.add_test("settings_builder_create_settings_valid", (), True, True, 
        settings_builder_create_settings_valid)
    suite.add_test("settings_builder_create_settings_invalid", (), True, True, 
        settings_builder_create_settings_invalid)
    suite.add_test("settings_builder_create_settings_invalid_missing_keys", (), True, True, 
        settings_builder_create_settings_invalid_missing_keys)
    suite.add_test("settings_builder_create_settings_invalid_extra_keys", (), True, True, 
        settings_builder_create_settings_invalid_extra_keys)
    suite.add_test("settings_builder_create_settings_invalid_misnamed_keys", (), True, True, 
        settings_builder_create_settings_invalid_misnamed_keys)
    suite.add_test("settings_builder_create_settings_invalid_empty", (), True, True, 
        settings_builder_create_settings_invalid_empty)
    suite.add_test("settings_builder_copy_settings", (), True, True, 
        settings_builder_copy_settings)
    suite.add_test("settings_builder_copy_settings_not_configured", (), True, True, 
        settings_builder_copy_settings_not_configured)
    suite.add_test("settings_builder_change_settings_valid", (), True, True, 
        settings_builder_change_settings_valid)
    suite.add_test("settings_builder_change_settings_invalid", (), True, True, 
        settings_builder_change_settings_invalid)
    suite.add_test("settings_builder_change_settings_empty", (), True, True, 
        settings_builder_change_settings_empty)

    #### Data file tests.
    suite.add_test("create_data_file_valid", (), True, True, 
        create_data_file_valid)
    suite.add_test("create_data_file_invalid", (), True, True, 
        create_data_file_invalid)
    suite.add_test("create_data_file_invalid_bad_file_type", (), True, True, 
        create_data_file_invalid_bad_file_type)
    suite.add_test("create_data_file_invalid_missing_keys", (), True, True, 
        create_data_file_invalid_missing_keys)
    suite.add_test("create_data_file_invalid_extra_keys", (), True, True, 
        create_data_file_invalid_extra_keys)
    suite.add_test("create_data_file_invalid_empty", (), True, True, 
        create_data_file_invalid_empty)
    suite.add_test("data_file_get_valid", (), True, True, 
        data_file_get_valid)
    suite.add_test("data_file_get_invalid", (), True, True, 
        data_file_get_invalid)
    suite.add_test("data_file_set_valid", (), True, True, 
        data_file_set_valid)
    suite.add_test("data_file_set_invalid", (), True, True, 
        data_file_set_invalid)
    suite.add_test("data_file_set_invalid_bad_key", (), True, True, 
        data_file_set_invalid_bad_key)
    suite.add_test("data_file_set_invalid_file_type", (), True, True, 
        data_file_set_invalid_file_type)

    #### Meta tests
    suite.add_test("create_meta_valid", (), True, True, 
        create_meta_valid)
    suite.add_test("create_meta_invalid", (), True, True, 
        create_meta_invalid)
    suite.add_test("create_meta_invalid_missing_keys", (), True, True, 
        create_meta_invalid_missing_keys)
    suite.add_test("create_meta_invalid_extra_keys", (), True, True, 
        create_meta_invalid_extra_keys)
    suite.add_test("create_meta_invalid_empty", (), True, True, 
        create_meta_invalid_empty)
    suite.add_test("meta_get_valid", (), True, True, 
        meta_get_valid)
    suite.add_test("meta_get_invalid", (), True, True, 
        meta_get_invalid)
    suite.add_test("meta_set_valid", (), True, True, 
        meta_set_valid)
    suite.add_test("meta_set_invalid", (), True, True, 
        meta_set_invalid)

    #### ConversationBuilder tests 
    suite.add_test("builder_set_conversation_source_path_valid", (), True, 
        True, builder_set_conversation_source_path_valid)
    suite.add_test("builder_set_conversation_source_path_invalid", (), True, 
        True, builder_set_conversation_source_path_invalid)
    suite.add_test("builder_set_conversation_name", (), True, True, 
        builder_set_conversation_name)
    suite.add_test("builder_set_result_directory_path_valid", (), True, True, 
        builder_set_result_directory_path_valid)
    suite.add_test("builder_set_result_directory_path_invalid", (), True, True, 
        builder_set_result_directory_path_invalid)
    suite.add_test("builder_set_temporary_directory_path_valid", (), True, True, 
        builder_set_temporary_directory_path_valid)
    suite.add_test("builder_set_temporary_directory_path_invalid", (), True, True, 
        builder_set_temporary_directory_path_invalid)
    suite.add_test("builder_set_number_of_speakers_valid", (), True, True, 
        builder_set_number_of_speakers_valid)
    suite.add_test("builder_set_number_of_speakers_invalid", (), True, True, 
        builder_set_number_of_speakers_invalid)
    suite.add_test("builder_set_conversation_settings_valid", (), True, True, 
        builder_set_conversation_settings_valid)
    suite.add_test("builder_set_conversation_settings_invalid", (), True, True, 
        builder_set_conversation_settings_invalid)
    suite.add_test("builder_build_conversation_valid", (), True, True, 
        builder_build_conversation_valid)
    suite.add_test("builder_build_conversation_invalid", (), True, True, 
        builder_build_conversation_invalid)
    suite.add_test("builder_clear_conversation", (), True, True, 
        builder_clear_conversation)

    #### Conversation tests
    suite.add_test("conversation_get_conversation_name", (), True, True, 
        conversation_get_conversation_name)
    suite.add_test("conversation_get_conversation_size", (), True, True, 
        conversation_get_conversation_size)
    suite.add_test("conversation_get_source_type", (), True, True, 
        conversation_get_source_type)
    suite.add_test("conversation_get_transcription_date", (), True, True, 
        conversation_get_transcription_date)
    suite.add_test("conversation_get_transcription_status", (), True, True, 
        conversation_get_transcription_status)
    suite.add_test("conversation_get_transcription_time", (), True, True, 
        conversation_get_transcription_time)
    suite.add_test("conversation_number_of_source_files", (), True, True, 
        conversation_number_of_source_files)
    suite.add_test("conversation_number_of_speakers", (), True, True, 
        conversation_number_of_speakers)
    suite.add_test("conversation_get_source_file_names", (), True, True, 
        conversation_get_source_file_names)
    suite.add_test("conversation_get_source_file_paths", (), True, True, 
        conversation_get_source_file_paths)
    suite.add_test("conversation_get_source_file_types", (), True, True, 
        conversation_get_source_file_types)

    #### Organizer tests
    suite.add_test("organizer_create_settings_valid", (), True, True, 
        organizer_create_settings_valid)
    suite.add_test("organizer_create_settings_invalid", (), True, True, 
        organizer_create_settings_invalid)
    suite.add_test("organizer_copy_settings", (), True, True, 
        organizer_copy_settings)
    suite.add_test("organizer_change_settings_valid", (), True, True, 
        organizer_change_settings_valid)
    suite.add_test("organizer_change_settings_invalid", (), True, True, 
        organizer_change_settings_invalid)
    suite.add_test("organizer_create_conversation_valid", (), True, True, 
        organizer_create_conversation_valid)
    suite.add_test("organizer_apply_settings_to_conversation_valid", (), True, 
        True, organizer_apply_settings_to_conversation_valid)

    return suite

