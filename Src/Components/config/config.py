# Standard imports 
import os 
from typing import Dict, Tuple
from copy import deepcopy
# Local imports 
from .blackboard import BlackBoard 
from .attributes import BlackBoardAttributes
# Third party imports 
import json 

class Config:
    """
    Responsible for collecting all information that is needed by an object of
    class BlackBoard. 
    """

    def __init__(self) -> None:
        """
        Params:
            config_file_formats (List[str]): All acceptable configuration file 
                                            formats.
            blackboard (BlackBoard): Object that is loaded with env. variables 
                                    and eventually returned from this class
        """
        # Acceptable config file formats 
        self.config_file_formats = ("JSON")
        # Params
        self.blackboard = BlackBoard()

    def load_from_file(self, config_filename : str, format : str) -> bool:
        """
        Loads env. vars for the server from a configuration file
        
        Args:
            config_filename (str): Path to the configuration file
            format (str): Format the configuration file is in. 
                        Must be on config_file_formats
        
        Returns:
            (bool): True if environment is loaded successfully. False otherwise.
        """
        if format in self.config_file_formats:
            env, is_successful = self._parse_config_file(
                config_filename, format)
            if is_successful:
                self._set_blackboard(env)
                return True 
            else:
                return False 
        return False 


    def get_blackboard(self) -> BlackBoard:
        """
        Returns an instance of the blackboard object containing the environment.
        
        Returns:
            (BlackBoard)
        """
        return deepcopy(self.blackboard)

    ################################## PRIVATE METHODS ######################
    def _set_blackboard(self, env : Dict) -> None:
        """
        Sets all the attributes for the blackboard from the environment
        
        Args:
            env (Dict): Environment containing all the key-value pairs 
                        required for configuration
        """
        all_blackboard_attrs = [v for v in BlackBoardAttributes]
        for attr in all_blackboard_attrs:
            self.blackboard.set(attr,env[attr]) 

    def _parse_config_file(self, filename: str, format : str) -> \
            Tuple[Dict, bool]:
        """
        Parses the configuration file into an environment dictionary.
        
        Args:
            filename (str): configuration file path
            format (str): Format the configuration file is in. 
                        Must be on config_file_formats
        
        Returns:
            (Dict): Environment read from the configuration file.
            (bool): True if environment read successfully. False otherwise.
        
        Notes:
            Structure of the input json file should be:
            {
               
            }
        """
        # TODO: Define the expected file structure in the docstring.
        env = {}
        loaders = {
            "JSON" : self._load_json
        }
        # File does not exist 
        if not os.path.exists(filename):
            return (env,False)
        # Getting data if the file does exist
        try:
            data = loaders[format](filename)
            ### Reading data into local environment to ensure syntax/naming 
            # consistency b/w Blackboard and filename
            # TODO: Load the environment here and use the data variable
            env[BlackBoardAttributes.Test_key] = data["Test_key"]
            return (env,True)
        except (KeyError, TypeError):
            return (env,False)

    def _load_json(self, filename : str) ->Dict:
        """
        Loads a json file and returns a dictionary of all data in the file

        Args:
            filename (str): json file path
        
        Returns:
            (Dict): Data in the json file
        """
        try:
            with open(filename) as f:
                return json.load(f)
        except:
            pass 