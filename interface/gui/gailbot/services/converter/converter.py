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
    """
    provide function that converts the sourceObject to payload and 
    keeps track of the converted payloads 
    """ 
    loaders = [
        load_audio_payload, 
        load_transcribed_dir_payload,
        load_conversation_dir_payload]
    
    """ mapping payload name to payloadObject """
    def __init__(self) -> None:
        self.payloads_dict: Dict[str, PayLoadObject] = dict()
        
    def load_source(self, source: SourceObject) -> bool:
        for loader in self.loaders:
            try: 
                payloads: List [PayLoadObject] = loader(source)
                logger.info(payloads)
                if isinstance(payloads, list):
                    self.payloads_dict[source.name] = payloads
                    return True 
            except Exception as e:
                logger.error(e) 
        return False

    
    def __call__(
        self, sources: List[SourceObject]) -> Union[bool, List[PayLoadObject]]:
        """ given a list of the source files, and convert them into a list of 
           payload objects 

        Args:
            sources (List[SourceObject]): a list of source object

        Returns:
            Union[bool, List[PayLoadObject]]: a list of payload object that are 
            successfully converted by the converter
        """
        logger.info("converter is called")
        logger.info(sources)
        self.payloads_dict = dict()
        try:
            for source in sources:
                logger.info(source)
                self.load_source(source)
            logger.info(self.payloads_dict)
            return sum(list(self.payloads_dict.values()), [])
        
        except Exception as e: 
            logger.error(e)
            return False
        
                
        