from gailbot.services.organizer.source import SourceObject, SourceManager
# from gailbot.configs.confs.toplevel import 
from gailbot.core.utils.general import get_name

#TODO
SOURCE_PATH = None
OUTPUT_PATH = None

## test source object

def test_source_details():
    test_source_manager = SourceManager()
    test_source_manager.add_source(SOURCE_PATH, OUTPUT_PATH)
    name = get_name(SOURCE_PATH)
    test_source = test_source_manager.get_source(name)
    details = test_source.source_details(test_source)
    print (f"source_name: {details.source_name}, source_path: {details.source_path}, settings: {details.settings}" )

def test_configured():
    pass

def test_apply_setting():
    pass

## test source manager

def test_remove_source():
    pass

def test_is_source():
    pass

def test_source_names():
    #TODO make different source paths
    test_source_manager = SourceManager()
    test_source_manager.add_source(SOURCE_PATH, OUTPUT_PATH)
    test_source_manager = SourceManager()
    test_source_manager.add_source(SOURCE_PATH, OUTPUT_PATH)
    test_source_manager = SourceManager()
    test_source_manager.add_source(SOURCE_PATH, OUTPUT_PATH)
    names = test_source_manager.source_names(test_source_manager)

def test_get_source():
    # implicitly tested
    pass

def test_apply_setting_profile_to_source():
    pass

def test_get_sources_with_setting():
    pass