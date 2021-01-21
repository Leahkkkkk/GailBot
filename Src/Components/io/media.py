# Standard library imports 
from typing import Any, Tuple
import os
# Local imports 
from ...utils.exceptions import ExceptionInvalid
from .audio import AudioIO
from .video import VideoIO
# Third party imports


class Media:

    def __init__(self) -> None:
        # Params
        self.audio = AudioIO()
        self.video = VideoIO()

    def extract_audio(self, file_path : str) -> Tuple[bool,Any]:
        if not self._does_file_exist(file_path):
            return (False, None)

    def extract_video(self) -> None:
        pass 

    def convert_to_format(self) -> None:
        pass 

    def overlay_audio(self) -> None:
        pass 

    def chunk_audio(self) -> None:
        pass 

    def crop(self) -> None:
        pass 

    def increase_volume(self) -> None:
        pass 

    def decrease_volume(self) -> None:
        pass 


    ############################# PRIVATE METHODS ###########################

    def _does_file_exist(self, file_path : str) -> bool:
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def _get_file_extension(self, file_path : str) -> str:
        return os.path.splitext(file_path.strip())[1][1:]








