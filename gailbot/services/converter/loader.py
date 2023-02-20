from payload import (PayLoadObject, 
                     load_audio_payload, 
                     load_directory_payload, 
                     load_transcribed_directory_payload, 
                     load_video_payload)
from typing import Dict
from ..organizer.source import SourceObject
class Loader: 
    payloads_dict: Dict[str, PayLoadObject] = dict() 
    loaders = [
        load_video_payload, 
        load_audio_payload, 
        load_directory_payload, 
        load_transcribed_directory_payload]
    """ mapping payload name to payloadObject """
    def load_source(self, source: SourceObject) -> bool:
        for loader in self.loaders:
            try: 
                payload = loader(source)
                if isinstance(payload, PayLoadObject):
                    self.payloads_dict[source.name] = payload
                    return True
            except Exception as e:
                pass 
        raise False
    
    def check_status(self, name:str):
        if name in self.payloads_dict:
            return self.payloads_dict[name].status
        else: 
            return False
    