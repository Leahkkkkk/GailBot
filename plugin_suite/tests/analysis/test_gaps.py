from .test_fun import analysis_test
from gb_hilab_suite.src.analysis.gaps import GapPlugin
PAUSE_OUT_PATH = "/Users/yike/Desktop/plugin_output/gaps"

def test_pauses():
    utt       = [{"start": i, "end": i + 0.2, "speaker": i % 3, "text": f"word{i}"} for i in range(0,20,1)]
    pause_data   = {"test": utt}
    pause_plugin = GapPlugin()
    analysis_test(pause_data, pause_plugin, PAUSE_OUT_PATH)
