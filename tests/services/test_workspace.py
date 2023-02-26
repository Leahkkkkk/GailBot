from gailbot.services.workspace import WorkspaceManager
import logging
from gailbot.core.utils.general import is_directory
from .test_data import PATH

def test_workspace():
    WorkspaceManager.init_workspace()
    logging.info(WorkspaceManager.setting_src)
    logging.info(WorkspaceManager.log_file_space)
    logging.info(WorkspaceManager.plugin_src)
    logging.info(WorkspaceManager.tempspace_root)
    assert(is_directory(WorkspaceManager.setting_src)) 
    assert(is_directory(WorkspaceManager.log_file_space)) 
    assert(is_directory(WorkspaceManager.plugin_src)) 
    assert(is_directory(WorkspaceManager.tempspace_root))
    
    temp = WorkspaceManager.get_file_temp_space("test") 
    assert(is_directory(temp.transcribe_ws))
    assert(is_directory(temp.data_copy))
    assert(is_directory(temp.format_ws))
    assert(is_directory(temp.analysis_ws))
    assert(is_directory(temp.root))
    
    output = WorkspaceManager.get_output_space(PATH.OUTPUT_ROOT, "test")
    assert(is_directory(output.transcribe_result))
    assert(is_directory(output.root))
    assert(is_directory(output.media_file))
    assert(is_directory(output.format_result))
    assert(is_directory(output.analysis_result))
    
    # assert WorkspaceManager.clear_temp_space("test")
    # assert not is_directory(temp.root)
    
    WorkspaceManager.clear_temp_space(temp)
    assert not is_directory(temp.root)