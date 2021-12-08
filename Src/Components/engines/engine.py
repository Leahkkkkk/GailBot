# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:13:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-08 11:33:43
# Standard library imports
from abc import ABC, abstractmethod
from typing import Any, Dict, List
# Local imports
from ..shared_models import Utt
from ..io import IO
# Third party imports


class Engine(ABC):
    """
    Template for all speech to text engines.

    Inherits:
        (ABC)
    """
    @abstractmethod
    def __init__(self, io: IO) -> None:
        pass

    @abstractmethod
    def configure(self, *args, **kwargs) -> bool:
        """
        Configure core attributes of the engine.

        Returns:
            (bool): True if successfully configured. False otherwise.
        """
        pass

    @abstractmethod
    def get_configurations(self) -> Dict[str, Any]:
        """
        Obtain all core configurations of the engine/

        Returns:
            (Dict[str,Any]): Mapping from core configuration to the values.
        """
        pass

    @abstractmethod
    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.

        Returns:
            (str): Name of the engine.
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        Obtain a list of audio file formats that are supported.

        Returns:
            (List[str]): Supported audio file formats.
        """
        pass

    @abstractmethod
    def is_file_supported(self, file_path: str) -> bool:
        """
        Determine if the given file is supported by the engine.

        Args:
            file_path (str)

        Returns:
            (bool): True if file is supported. False otherwise.
        """
        pass

    @abstractmethod
    def transcribe(self) -> List[Utt]:
        """
        Transcribe the audio file that can be added through the configure method
        """
        pass

    @abstractmethod
    def was_transcription_successful(self) -> bool:
        """
        Determine whether the transcription was successful.

        Returns:
            (bool): True if transcription was successful. False otherwise.
        """
        pass
