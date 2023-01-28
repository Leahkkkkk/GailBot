
import pytest
from gailbot.configs.utils import WATSON_DATA, SETTING_DATA
from gailbot.configs.conf_path import ENGINE_PATH, SETTING_PATH, WORKSPACE_PATH 

def test_paths():
    print(ENGINE_PATH)
    print(SETTING_PATH)
    print(WORKSPACE_PATH)

def test_data():
    print(WATSON_DATA)
    print(SETTING_DATA)