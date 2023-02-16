from typing import List, Dict

class SourceManager():
    """
    Holds and handles all functionality for managing all sources
    """
    def __init__(self) -> None:
        pass

    def remove_source() -> bool:
        raise NotImplementedError()
    
    def is_source() -> bool:
        raise NotImplementedError()

    def source_names() -> List[str]:
        raise NotImplementedError()

    def get_source() -> Source:
        raise NotImplementedError()

    def map_sources() -> Dict:
        raise NotImplementedError()

    def get_source_details() -> Dict:
        raise NotImplementedError()

    def apply_setting_profile_to_source():
        raise NotImplementedError()