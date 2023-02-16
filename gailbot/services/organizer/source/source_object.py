from typing import Dict

class Source():
    """
    Holds and handles all functionality for a single source object
    TODO: workspace attribute does not have a final design
    """
    def __init__(self) -> None:
        source_path : str
        settings : SettingProfile
        workspace : str

    def workspace():
        raise NotImplementedError()

    def to_dict() -> Dict:
        raise NotImplementedError()

    def configured() -> bool:
        raise NotImplementedError()