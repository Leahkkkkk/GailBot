from gb_hilab_suite.src.analysis.syllable_rate import SyllableRatePlugin
from .test_fun import analysis_test
SYLLABLE_RATE_OUT_PATH = "/Users/yike/Desktop/plugin_output/syllable_rate"

def test_syllable_rate():
    fast_utt             = [{"start": i, "end": i + 0.99, "speaker": 1, "text": f"word{i}"} for i in range(0,20,1)]
    slow_utt             = [{"start": i, "end": i + 0.20, "speaker": 1, "text": f"word{i}"} for i in range(20, 40, 1)]
    normal_utt           = [{"start": i, "end": i + 0.50, "speaker": 1, "text": f"word{i}"} for i in range(40, 60, 1)]
    syllable_rate_data   = {"test": fast_utt + slow_utt + normal_utt}
    plugin = SyllableRatePlugin()
    analysis_test(syllable_rate_data, plugin, SYLLABLE_RATE_OUT_PATH + "fast_slow")


def test_zero_gap():
    zero_gap             = [{"start": i, "end": i, "speaker": 1, "text": f"word{i}"} for i in range(1, 10, 1)]
    slow_utt             = [{"start": i, "end": i + 0.20, "speaker": 2, "text": f"word{i}"} for i in range(20, 40, 1)]
    normal_utt           = [{"start": i, "end": i + 0.50, "speaker": 3, "text": f"word{i}"} for i in range(40, 60, 1)]
    syllable_rate_data   = {"test": zero_gap + slow_utt + normal_utt}
    syllable_rate_data   = {"test": zero_gap }
    plugin = SyllableRatePlugin()
    analysis_test(syllable_rate_data, plugin, SYLLABLE_RATE_OUT_PATH + "zero_gap")


