from .test_fun import analysis_test
from gb_hilab_suite.src.analysis.overlaps import OverlapPlugin
PAUSE_OUT_PATH = "/Users/yike/Desktop/plugin_output/overlap"

def test_pauses():
    utt       = [{"start": i, "end": i + 1.5, "speaker": i % 3, "text": f"word{i}"} for i in range(0,20,1)]
    utt2       = [{"start": i, "end": i + 1.2, "speaker": i % 3, "text": f"word{i}"} for i in range(20,40,1)]
    pause_data   = {"test": utt + utt2}
    pause_plugin = OverlapPlugin()
    analysis_test(pause_data, pause_plugin, PAUSE_OUT_PATH)
