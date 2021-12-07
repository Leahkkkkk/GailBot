# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-07 12:47:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 12:47:35
# # Standard library imports
# # Local imports
# from typing import List, Any, Dict
# from ..engine import Engine
# from .core import GoogleCore
# from ...io import IO
# from ..utterance import Utterance, UtteranceAttributes

# # Third party imports

# class GoogleEngine(Engine):

#     def __init__(self, io = IO) -> None:
#         self.engine_name = "google"
#         self.io = io
#         self.core = GoogleCore(io)
#         self.is_ready_for_transcription = False

#     def configure(self, audio_path: str, sample_rate: int, speaker_count: int) -> bool:
#         """
#         Configure core attributes of the engine.

#         Returns:
#             (bool): True if successfully configured. False otherwise.
#         """
#         self.is_ready_for_transcription =  self.core.set_audio_path(audio_path) and \
#             self.core.set_sample_rate_hertz(sample_rate) and \
#             self.core.set_diarization_speaker_count(speaker_count)

#         return self.is_ready_for_transcription

#     def get_configurations(self) -> Dict[str,Any]:
#         """
#         Obtain all core configurations of the engine/

#         Returns:
#             (Dict[str,Any]): Mapping from core configuration to the values.
#         """
#         return {
#             "audio_path" : self.core.get_audio_path(),
#             "sample_rate_hertz" : self.core.get_sample_rate_hertz(),
#             "diarization_speaker_count" : self.core.get_diarization_speaker_count()
#         }

#     def get_engine_name(self) -> str:
#         """
#         Obtain the name of the current engine.

#         Returns:
#             (str): Name of the engine.
#         """
#         return self.engine_name

#     def get_supported_formats(self) -> List[str]:
#         """
#         Obtain a list of audio file formats that are supported.

#         Returns:
#             (List[str]): Supported audio file formats.
#         """
#         return self.core.get_supported_audio_formats()

#     def is_file_supported(self, file_path : str) -> bool:
#         """
#         Determine if the given file is supported by the engine.

#         Args:
#             file_path (str)

#         Returns:
#             (bool): True if file is supported. False otherwise.
#         """
#         return self.io.is_file(file_path) and \
#             self.io.get_file_extension(file_path)[1] \
#             in self.core.get_supported_audio_formats()

#     def transcribe(self) -> List[Utterance]:
#         """
#         Transcribe the audio file that can be added through the configure method

#         Returns:
#             List[Utterance]: Returns list of utterances on the word level from
#                 speech client response. Returns empty list if engine is not
#                 configured properly for transcription.
#         """
#         if not self.is_ready_for_transcription:
#             return []
#         utterances = self.core.transcribe_audio()
#         self.is_ready_for_transcription = False
#         self.core.reset_configurations()

#         return utterances

#     def was_transcription_successful(self) -> bool:
#         """
#         Determine whether the transcription was successful.

#         Returns:
#             (bool): True if transcription was successful. False otherwise.
#         """
#         raise Exception("Not implemented")
