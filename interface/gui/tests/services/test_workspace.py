from gailbot.workspace.manager import WorkspaceManager
from gailbot.core.utils.general import is_directory
import logging
from .test_data import PATH

ROOT = "/Users/yike/Desktop"

def test_workspace():
    ws_manager = WorkspaceManager(ROOT)
    ws_manager.init_workspace()
    logging.info(ws_manager.setting_src)
    logging.info(ws_manager.log_file_space)
    logging.info(ws_manager.plugin_src)
    logging.info(ws_manager.tempspace_root)
    assert(is_directory(ws_manager.setting_src)) 
    assert(is_directory(ws_manager.log_file_space)) 
    assert(is_directory(ws_manager.plugin_src)) 
    assert(is_directory(ws_manager.tempspace_root))
    
    temp = ws_manager.get_file_temp_space("test") 
    assert(is_directory(temp.transcribe_ws))
    assert(is_directory(temp.data_copy))
    assert(is_directory(temp.format_ws))
    assert(is_directory(temp.analysis_ws))
    assert(is_directory(temp.root))
    
    output = ws_manager.get_output_space(PATH.OUTPUT_ROOT, "test")
    assert(is_directory(output.transcribe_result))
    assert(is_directory(output.root))
    assert(is_directory(output.media_file))
    assert(is_directory(output.format_result))
    assert(is_directory(output.analysis_result))
    
    # assert ws_manager.clear_temp_space("test")
    # assert not is_directory(temp.root)
    
    ws_manager.clear_temp_space(temp)
    assert not is_directory(temp.root)