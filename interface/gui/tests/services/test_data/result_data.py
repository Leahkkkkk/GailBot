from dataclasses import dataclass

utt_data = [ {"speaker": "speaker" + str(i),  
            "start_time": str(i), 
            "end_time": str(i), 
            "text": "Hello!" + str(i)} for i in range(10)]
@dataclass
class UTT_RESULT:
    UTT_DICT = { "utt_result" + str(i): utt_data for i in range(2) }
    