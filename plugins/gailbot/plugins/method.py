from typing import Dict, Union, Any, List

class Methods():
    def __init__(self) -> None:
        raise NotImplementedError

class GBPluginMethods(Methods):
    def __init__(self, payload):
        raise NotImplementedError
              
    @property
    def audios(self) -> Dict[str,str]:
        raise NotImplementedError

    @property
    def utterances(self) -> Dict[str,Dict]:
        """ 
        Accesses and returns the utterance data

        Returns:
            Dict[str,Dict]: return dictionary that maps audio name to the 
                            transcription result  
        """
        raise NotImplementedError
                
    @property
    def temp_work_path(self) -> str:
        """
        Accesses and returns the temporary workspace path

        Returns:
            String containing the temporary workspace path
        """
        raise NotImplementedError
   
    @property
    def output_path(self) -> str:
        """
        Accesses and returns the output path

        Returns:
            String containing the output path
        """
        raise NotImplementedError
    
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
        raise NotImplementedError