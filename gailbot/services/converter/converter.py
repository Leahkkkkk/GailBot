from .payload import (
    load_transcribed_dir_payload, 
    load_audio_payload, 
    load_conversation_dir_payload,
    PayLoadObject)
from typing import Dict, List, Union
from gailbot.core.utils.logger import makelogger
from ..organizer.source import SourceObject

logger = makelogger("congerter")
class Converter: 
    payloads_dict: Dict[str, PayLoadObject] = dict() 
    
    loaders = [
        load_conversation_dir_payload, 
        load_audio_payload, 
        load_transcribed_dir_payload] 
    
    """ mapping payload name to payloadObject """
    def load_source(self, source: SourceObject) -> bool:
        for loader in self.loaders:
            try: 
                payloads: List [PayLoadObject] = loader(source)
                if isinstance(payloads, PayLoadObject):
                    self.payloads_dict[source.name] = payloads
                    return True 
            except Exception as e:
                logger.error(e) 
        raise False

    
    def __call__(self, sources: List[SourceObject]) -> Union[bool, List[PayLoadObject]]:
        try:
            for source in sources:
                self.load_source(source)
            return list(self.payloads_dict.values())
        except Exception as e: 
            logger.error(e)
            return False
        
                
        