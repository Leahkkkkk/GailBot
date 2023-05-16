from typing import Dict, Union, Any, List, TypedDict
from pydantic import BaseModel 
import os
OUT_PATH = "/Users/yike/Desktop/plugin_output"

class UttObj(BaseModel):
    start: float 
    end: float 
    speaker: str 
    text: str
class UttDict(TypedDict):
    start: float 
    end: float 
    speaker: str 
    text: str
class Methods():
    def __init__(self) -> None:
        raise NotImplementedError

class GBPluginMethods(Methods):
    def __init__(self, utt_data = None, output_path = None):
        pause_utt = [{"start":  i, "end": i + 0.91, "speaker": 1, "text": f"word{i}"} for i in range(0, 20, 1)]
        gap_utt =   [{"start":  i, "end": i + 0.5, "speaker": (0 + i) % 4, "text": f"word{i}"} for i in range(20, 60, 1)]
        overlap_utt = [{"start": i, "end": i + 4, "speaker": (0 + i) % 2, "text": f"word{i}"} for i in range(60, 80, 1)]
        data = dict()
        data["test"] = pause_utt + gap_utt + overlap_utt
        if utt_data:
            self.data = utt_data
        else:
            self.data = data 
        
        if output_path:
            self.output = output_path
            os.makedirs(output_path, exist_ok=True)
        else:
            self.output = OUT_PATH
    
    @property
    def filenames(self) -> List[str]:
        return list(self.data.keys())
     
    @property
    def audios(self) -> Dict[str,str]:
        """
        Returns a dictionary that maps the audio name to the audio source
        """
        return "audios"

    @property
    def utterances(self) -> Dict[str,List[UttDict]]:
        """ 
        Accesses and returns the utterance data

        Returns:
            Dict[str,Dict]: return dictionary that maps audio name to the 
                            transcription result  
        """
        return self.data
                
    @property
    def temp_work_path(self) -> str:
        """
        Accesses and returns the temporary workspace path

        Returns:
            String containing the temporary workspace path
        """
        return "temp"
   
    @property
    def output_path(self) -> str:
        """
        Accesses and returns the output path

        Returns:
            String containing the output path
        """
        return self.output
    
    def get_utterance_objects(self) -> Dict[str, List[UttObj]]: 
        """ 
        Access and return the utterance data as utterance object 
        """
        res = dict()
        for key, uttlist in self.data.items(): 
            newlist = list()
            for utt in uttlist:
                newlist.append(UttObj(**utt))
            res[key] = newlist
        return res
    
    
    def save_item(self, 
                  data: Union [Dict[str, Any], List],
                  name: str, 
                  temporary: bool = True, 
                  format: str = "json", 
                  fun: callable = None,
                  kwargs = None) -> bool :
       raise NotImplementedError