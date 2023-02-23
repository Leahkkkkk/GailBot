from payload import (PayLoadObject, 
                     load_audio_payload, 
                     load_transcribed_directory_payload, 
                     load_directory_payload, 
                     load_video_payload)
from typing import Dict, List
from ..organizer.source import SourceObject
class Converter: 
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
                payloads: List [PayLoadObject] = loader(source)
                # TODO: another for loop 
                if isinstance(payloads, PayLoadObject):
                    self.payloads_dict[source.name] = payloads
                    return True
                
            except Exception as e:
                pass 
        raise False

    
    def get_payloads(self, sources: List [SourceObject]):
        raise NotImplementedError()
    
    def __call__(self, sources: List[SourceObject]) :
        raise NotImplementedError()
        