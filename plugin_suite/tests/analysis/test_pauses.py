from .test_fun import analysis_test
from gb_hilab_suite.src.analysis.pauses import PausePlugin
PAUSE_OUT_PATH = "/Users/yike/Desktop/plugin_output/pauses"

def test_pauses():
    utt       = [{"start": i, "end": i + 0.99, "speaker": 1, "text": f"word{i}"} for i in range(0,20,1)]
    micro_pause  = [{"start": i, "end": i + 0.40, "speaker": 1, "text": f"word{i}"} for i in range(20, 40, 1)]
    long_pause   = [{"start": i, "end": i + 0.10, "speaker": 1, "text": f"word{i}"} for i in range(40, 60, 2)]
    medium_pause = [{"start": i, "end": i + 1.4, "speaker": 1, "text": f"word{i}"} for i in range(60, 80, 2)]
    pause_data   = {"test": utt + micro_pause + long_pause + medium_pause}
    pause_plugin = PausePlugin()
    analysis_test(pause_data, pause_plugin, PAUSE_OUT_PATH)

def test_latch():
    utt  = [{"start": i, "end": i + 0.92, "speaker": 1, "text": f"word{i}"} for i in range(0,20,1)]
    utt2 = [{"start": i, "end": i + 0.92, "speaker": 2, "text": f"word{i}"} for i in range(20,40,1)]
    utt3 = [{"start": i, "end": i + 0.92, "speaker": 1, "text": f"word{i}"} for i in range(20,40,1)]
    data = {"test": utt + utt2 + utt3}
    pause_plugin = PausePlugin()
    analysis_test(data, pause_plugin, PAUSE_OUT_PATH + "patch")

def test_pause():
    utt  = [{"start": i, "end": i + 0.77, "speaker": 1, "text": f"word{i}"} for i in range(0,20,1)]
    data = {"test": utt}
    pause_plugin = PausePlugin()
    analysis_test(data, pause_plugin, PAUSE_OUT_PATH + "pause")
    
def test_micro_pause():
    utt  = [{"start": i, "end": i + 0.85, "speaker": 1, "text": f"word{i}"} for i in range(0,20,1)]
    data = {"test": utt}
    pause_plugin = PausePlugin()
    analysis_test(data, pause_plugin, PAUSE_OUT_PATH + "micro_pause")
    
def test_large_pause():
    utt  = [{"start": i, "end": i + 1, "speaker": 1, "text": f"word{i}"} for i in range(0,50,3)]
    data = {"test": utt}
    pause_plugin = PausePlugin()
    analysis_test(data, pause_plugin, PAUSE_OUT_PATH + "large_pause")