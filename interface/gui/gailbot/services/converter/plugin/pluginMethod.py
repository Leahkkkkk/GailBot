from pydantic import BaseModel
from gailbot.plugins import Methods
from gailbot.core.utils.logger import makelogger
from gailbot.services.converter.result import UttDict
from ..payload.payloadObject import PayLoadObject
from typing import Dict, Union, List, Any
from gailbot.core.utils.general import (
    get_name, 
    is_directory, 
    make_dir,
    write_csv,
    write_json,
    write_toml,
    write_yaml,
    write_txt)
import os 


logger = makelogger("pluginMethod")


class UttObj(BaseModel):
    start: float 
    end: float 
    speaker: str 
    text: str

class GBPluginMethods(Methods):
    format_to_out_fun = {
        "csv" : write_csv,
        "toml": write_toml,
        "yaml": write_yaml,
        "json": write_json,
        "txt": write_txt
    }
    
    def __init__(self, payload: PayLoadObject):
        self.payload: PayLoadObject = payload
        
        self.work_path = self.payload.workspace.analysis_ws
        if not is_directory(self.work_path):
            make_dir(self.work_path)
        
        self.out_path = self.payload.out_dir.analysis_result
        if not is_directory(self.out_path):
            make_dir(self.out_path)
              
    def get_audio_path(self) -> Dict[str, str]:
        """
        Returns a dictionary that maps the audio name to the audio source
        """
        return {get_name(path): path for path in self.payload.data_files}
    
    @property
    def filenames(self) -> List[str]:
        return [get_name(file) for file in self.payload.data_files]

    @property
    def utterances(self) -> Dict[str,List[UttDict]]:
        """ 
        Accesses and returns the utterance data

        Returns:
            Dict[str,Dict]: return dictionary that maps audio name to the 
                            transcription result  
        """
        try:
            return self.payload.get_transcription_result()
        except Exception as e:
            logger.error(e, exc_info=e)
            return False
                
    @property
    def temp_work_path(self) -> str:
        """
        Accesses and returns the temporary workspace path

        Returns:
            String containing the temporary workspace path
        """
        return self.work_path
   
    @property
    def output_path(self) -> str:
        """
        Accesses and returns the output path

        Returns:
            String containing the output path
        """
        return self.out_path
    
    def get_utterance_objects(self) -> Dict[str, List[UttObj]]: 
        """ 
        Access and return the utterance data as utterance object 
        """
        res = dict()
        data = self.payload.get_transcription_result()
        for key, uttlist in data.items(): 
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
        """function provided for the plugin to save file

        Args:
            data (Union[Dict[str, Any], List]): the data that will be outputed
            name (str): the name of the output file
            temporary (bool, optional): if true, the file will be stored in 
                                        temporary folder and discarded once the 
                                        analysis process finishes. Defaults to True.
            format (str, optional): the format of the output file. Defaults to "json".
            fun (callable, optional): user defined function to write the 
                                      output. Defaults to None.
            kwargs (dict, optional): user defined key word arguments that will 
                                    be passed into user defined function. 
                                    Defaults to None.

        Returns:
            bool: _description_
        """
        logger.info("plugin method, saving item is called")
        logger.info(data)
        path = os.path.join(self.work_path, name + "." + format) if temporary else \
               os.path.join(self.out_path,  name + "." + format)
        if fun:
            try:
                fun(path, data, **kwargs)
                return True
            except Exception as e:
                logger.error(e, exc_info=e)
                return False
        if format not in self.format_to_out_fun:
            logger.error("the output format is not supported")
            return False 
        try:
            self.format_to_out_fun[format](path, data) 
            return True
        except Exception as e:
            logger.error(e, exc_info=e)
            return False