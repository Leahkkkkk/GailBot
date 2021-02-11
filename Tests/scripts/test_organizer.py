"""
Testing for the organizer component
"""
# Standard library imports 

# Local imports 
from Src.Components.organizer import Paths, PathsAttributes, Settings, \
        SettingsAttributes, SettingsBuilder, DataFile ,DataFileAttributes, \
        DataFileTypes, Meta, MetaAttributes
from ..suites import TestSuite
# Third party imports 

############################### GLOBALS #####################################
WAV_FILE_PATH = "Test_files/Media/test2a.wav"
RESULT_DIR_PATH = "Test_files"
TMP_DIR_PATH = "Test_files/Others/Test-directory"

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
        settings.get(SettingsAttributes.sample_attribute_1)[1] == "1"

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
        meta.get(MetaAttributes.total_speakers)[1] == 1  

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

#########################  Conversation tests

######################### Organizer tests 


####################### TEST SUITE DEFINITION ################################

def define_organizer_test_suite() -> TestSuite:
    """
    Creates a test suite for io and adds tests to the suite.

    Returns:
        (TestSuite): Suite containing network tests
    """
    suite = TestSuite()

    #### Paths tests 
    # suite.add_test("paths_create_valid_data", (), True, True, 
    #     paths_create_valid_data)
    # suite.add_test("paths_create_invalid_data", (), True, True, 
    #     paths_create_invalid_data)
    # suite.add_test("paths_get_valid", (), True, True, 
    #     paths_get_valid)
    # suite.add_test("paths_get_invalid", (), True, True, 
    #     paths_get_invalid)

    # ### Settings tests
    # suite.add_test("settings_create_valid_data", (), True, True, 
    #     settings_create_valid_data)
    # suite.add_test("settings_create_invalid_data", (), True, True, 
    #     settings_create_invalid_data)
    # suite.add_test("settings_set_attribute_manually", (), True, True, 
    #     settings_set_attribute_manually)
    # suite.add_test("settings_get_valid", (), True, True, 
    #     settings_get_valid)
    # suite.add_test("settings_get_invalid", (), True, True, 
    #     settings_get_invalid)
    # suite.add_test("settings_builder_create_settings_valid", (), True, True, 
    #     settings_builder_create_settings_valid)
    # suite.add_test("settings_builder_create_settings_invalid", (), True, True, 
    #     settings_builder_create_settings_invalid)
    # suite.add_test("settings_builder_copy_settings", (), True, True, 
    #     settings_builder_copy_settings)
    # suite.add_test("settings_builder_change_settings_valid", (), True, True, 
    #     settings_builder_change_settings_valid)
    # suite.add_test("settings_builder_change_settings_invalid", (), True, True, 
    #     settings_builder_change_settings_invalid)

    #### Data file tests.
    # suite.add_test("create_data_file_valid", (), True, True, 
    #     create_data_file_valid)
    # suite.add_test("create_data_file_invalid", (), True, True, 
    #     create_data_file_invalid)
    # suite.add_test("data_file_get_valid", (), True, True, 
    #     data_file_get_valid)
    # suite.add_test("data_file_get_invalid", (), True, True, 
    #     data_file_get_invalid)
    # suite.add_test("data_file_set_valid", (), True, True, 
    #     data_file_set_valid)
    # suite.add_test("data_file_set_invalid", (), True, True, 
    #     data_file_set_invalid)

    #### Meta tests
    # suite.add_test("create_meta_valid", (), True, True, 
    #     create_meta_valid)
    # suite.add_test("create_meta_invalid", (), True, True, 
    #     create_meta_invalid)
    # suite.add_test("meta_get_valid", (), True, True, 
    #     meta_get_valid)
    # suite.add_test("meta_get_invalid", (), True, True, 
    #     meta_get_invalid)
    # suite.add_test("meta_set_valid", (), True, True, 
    #     meta_set_valid)
    # suite.add_test("meta_set_invalid", (), True, True, 
    #     meta_set_invalid)


    
    return suite

