from payload import PayLoadObject
from typing import Dict
class Loader: 
    """ TODO: store all payload """
    payloads_dict: Dict[str, PayLoadObject] = dict() 
    """ mapping payload name to payloadObject """
    def load_source(self, sources) -> PayLoadObject:
        raise NotImplementedError
    
    def check_status(self, name:str):
        raise NotImplementedError()

    