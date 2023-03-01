import os 
from dataclasses import dataclass

@dataclass 
class PATH:
    OUTPUT_ROOT = "/Users/yike/Desktop/gailbot_result"
    INVALID_DATA_DIR = os.path.join(os.getcwd(), "data/dummy_invalid")
    DUMMY_AUDIO = os.path.join(os.getcwd(), "data/dummy_audio")
    TRANSCRIBED = os.path.join(os.getcwd(), "data/transcribed_dirs/test_dir")
    GB_TEST_SUITE = os.path.join(os.getcwd(), "data/gb_test_suite")