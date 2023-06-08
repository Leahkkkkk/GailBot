import logging
from ..test_data import PAYLOAD_OBJ
from gailbot.services.converter.plugin.pluginMethod import GBPluginMethods

def test_plugin_method():
    method = GBPluginMethods(PAYLOAD_OBJ.AUDIO)
    logging.info(method.payload)
    logging.info(method.audio_files)
    logging.info(method.work_path)
    logging.info(method.out_path)
    logging.info(method.temp_work_path)
    logging.info(method.out_path)
    