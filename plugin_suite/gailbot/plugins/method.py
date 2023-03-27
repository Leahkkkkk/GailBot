from typing import Dict, Union, Any, List, TypedDict
from pydantic import BaseModel 
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
    def __init__(self):
        data = dict()
        data["hello"] = [{"start": 0.0, "end": 1.4, "text": "hello", "speaker": "1"}] 
        # for i in range(10):
        #     l = list()
          
        #     for j in range(100):
        #         l.append(
        #             { "start":j, 
        #               "end": j+ 1, 
        #               "text": str(i + j) , 
        #               "speaker": f"speaker {j%3}"
        #               })
        #     data[str(i) + "audio"] = l
        self.data = data 
    
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
        return OUT_PATH
    
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