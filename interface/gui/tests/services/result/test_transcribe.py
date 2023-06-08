from gailbot.services.workspace import WorkspaceManager
from ..test_data import PATH
from gailbot.services.converter.result import UttResult
import logging 
output = WorkspaceManager.get_output_space(PATH.OUTPUT_ROOT, "test_transcribe_result")
temporary_ws = WorkspaceManager.get_file_temp_space("test_transcribe_result")

utt_data = [ {"speaker": "speaker" + str(i),  
              "start_time": str(i), 
              "end_time": str(i), 
              "text": "Hello!" + str(i)} for i in range(10)]

utt_dict = { "utt_result" + str(i): utt_data for i in range(2) }


def test_utt_result():
    Utt_obj = UttResult(temporary_ws.transcribe_ws)
    Utt_obj.save_data(utt_dict)
    logging.info(Utt_obj.get_data())
    Utt_obj.output(output.transcribe_result)
    
    temporary_ws2 = WorkspaceManager.get_file_temp_space("test_transcribe_result2")
    Utt_obj2 = UttResult(temporary_ws2.transcribe_ws)
    Utt_obj2.load_result(output.transcribe_result)
    logging.info(Utt_obj2.get_data())