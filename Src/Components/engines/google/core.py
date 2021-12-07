# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-07 12:47:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 12:47:33
# # Standard library imports
# # Local imports
# # Third party imports
# from typing import List, Any, Dict, Tuple
# from google.cloud import speech_v1p1beta1 as speech
# from ...io import IO
# from ..utterance import Utterance
# import io as io

# class GoogleCore:

#     format_to_content_types = {
#         "flac" : "audio/flac",
#         "mp3" : "audio/mp3",
#         "wav" : "audio/wav"}

#     # TODO: add more language_codes if want to add functionality for other languages.
#     language_codes = {
#         "english" : "en-us"
#     }

#     def __init__(self, io = IO) -> None:
#         self.google_defaults = {
#             "enable_automatic_punctuation": True,
#             "language_code" : self.language_codes["english"],
#             "enable_speaker_diarization" : True,
#         }
#         self.inputs = {
#             "audio_path" : None,
#             "sample_rate_hertz" : None,
#             "diarization_speaker_count" : None
#         }
#         self.io = io

#     ## Setters

#     def set_audio_path(self, audio_source_path : str) -> bool:
#         """
#         Set the audio_path of audio file to transcribe. Validate that file
#         is a valid and supported audio.

#         Args:
#             audio_source_path (str):
#                 Path to audio file.

#         Returns:
#             (bool): True if audio_path successfully set, false otherwise.
#         """
#         if not self.io.is_file(audio_source_path) or \
#                 not self._is_supported_audio_file(audio_source_path):
#             return False
#         self.inputs["audio_path"] = audio_source_path
#         return True

#     # # TODO: define invalid rates -- some ranges are not suggested, or don't make sense inbetween a certain range
#     def set_sample_rate_hertz(self, sample_rate_hertz : int) -> bool:
#         """
#         Set the sample_rate_herts of audio file. Validate that sample_rate_hertz
#         is in proper range.

#         Args:
#             sample_rate_hertz (int):
#                 Sample rate of audio.

#         Returns:
#             (bool): True if sample_rate_hertz successfully set, false otherwise.
#         """
#         if sample_rate_hertz <= 0:
#             return False
#         self.inputs["sample_rate_hertz"] = sample_rate_hertz
#         return True

#     def set_diarization_speaker_count(self, speaker_count : int) -> bool:
#         """
#         Set the speaker_count of audio conversation. Validate that speaker_count
#         is more than 0.

#         Args:
#             speaker_count (int):
#                 Number of speakers in audio.
#         Returns:
#             (bool): True if diarization_speaker_count sucecssfully set, false
#                     otherwise.
#         """
#         if speaker_count <= 0:
#             return False
#         self.inputs["diarization_speaker_count"] = speaker_count
#         return True

#     ## Getters

#     def get_audio_path(self) -> str:
#         """
#         Retrieve audio_path from inputs.

#         Returns:
#             (str): audio path to file to transcribe.
#         """
#         return self.inputs["audio_path"]

#     def get_sample_rate_hertz(self) -> int:
#         """
#         Retrieve sample_rate_hertz from inputs.

#         Returns:
#             (int): sample rate of audio.
#         """
#         return self.inputs["sample_rate_hertz"]

#     def get_diarization_speaker_count(self) -> int:
#         """
#         Retrieve diarization speaker count from inputs.

#         Returns:
#             (int): number of speakers in conversation.
#         """
#         return self.inputs["diarization_speaker_count"]

#     def get_supported_audio_formats(self) -> List[str]:
#         """
#         Get the audio formats that are supported by the transcription service.

#         Returns:
#             List[str]: Supported audio formats.
#         """
#         return list(self.format_to_content_types.keys())

#     def get_supported_language_codes(self) -> List[str]:
#         """
#         Get the languages that are supported by the transcription service.

#         Returns:
#             List[str]: Supported languages.
#         """
#         return list(self.language_codes.keys())

#     def reset_configurations(self) -> bool:
#         """
#         Reset all the configurations/inputs.

#         Returns:
#             (bool): True if set successfully. False otherwise.
#         """
#         for k in self.inputs.keys():
#             self.inputs[k] = None
#         return True

#     def transcribe_audio(self) -> List[Utterance]:
#         """
#         Sends transcription request to Google client and parses utterances
#         from response.

#         Returns:
#             List[Utterance]: list of utterances of transcription on the word
#                              level.
#         """
#         # Get Google speech client, configure and send request
#         client = speech.SpeechClient()
#         audio, config = self._configure_api_request()
#         response = client.recognize(config=config, audio=audio)

#         utterances = self._parse_utterances_from_response(response)

#         return utterances

#     # private
#     def _is_supported_audio_file(self, file_path : str) -> bool:
#         """
#         Determine if the audio file at the given path is supported.

#         Args:
#             file_path (str): Path to the audio file.

#         Returns:
#             (bool): True if the file is supported. False otherwise.
#         """
#         _, extension = self.io.get_file_extension(file_path)
#         return extension in self.format_to_content_types.keys()

#     # TODO: it is not suggested to set encoding by extension. Need to find alternative methods for defining encoding
#     def _determine_encoding(self, audio_source_path : str) -> Any:
#         """
#         Determines encoding of audio file.

#         Args:
#             audio_source_path (str): path to audio source.

#         Return:
#             (Any): Encoding of audio file provided, None if no encoding
#                    determined
#         """
#         if not self._is_supported_audio_file(audio_source_path):
#             return None

#         _, extension = self.io.get_file_extension(audio_source_path)
#         if extension == "mp3":
#             return speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
#         elif extension == "wav":
#             return speech.RecognitionConfig.AudioEncoding.LINEAR16
#         elif extension == "flac":
#             return speech.RecognitionConfig.AudioEncoding.FLAC
#         return None

#     def _configure_api_request(self) -> Tuple[speech.RecognitionAudio, speech.RecognitionConfig]:
#         """
#         Configures audio and config to send request to speech client.

#         Return:
#            Tuple[speech.RecognitionAudio, speech.RecognitionConfig]:
#                 Audio and speech objects used for request
#         """
#         #TODO: does our io support this?
#         file_path = self.inputs["audio_path"]
#         with io.open(file_path, "rb") as audio:
#             content = audio.read()

#         audio = speech.RecognitionAudio(content=content)
#         config = speech.RecognitionConfig(
#             encoding=self._determine_encoding(file_path),
#             sample_rate_hertz=self.inputs["sample_rate_hertz"],
#             language_code=self.google_defaults["language_code"],
#             enable_speaker_diarization=self.google_defaults["enable_speaker_diarization"],
#             diarization_speaker_count=self.inputs["diarization_speaker_count"],
#             enable_automatic_punctuation=self.google_defaults["enable_automatic_punctuation"]
#         )

#         return (audio, config)

#     def _parse_utterances_from_response(self, response) -> List[Utterance]:
#         """
#         Parses utterances from Google response.

#         Args:
#             response: response from Google speech client after request sent.

#         Returns:
#             List[Utterance]: list of utterances on the word level from response.
#         """
#         result = response.results[-1]   # word list at end of response
#         words_info = result.alternatives[0].words

#         utterances = []
#         for word_info in words_info:
#             utterances.append(Utterance({
#                 "speaker_label" : word_info.speaker_tag,
#                 "start_time" : str(word_info.start_time),
#                 "end_time" : str(word_info.end_time),
#                 "transcript" : word_info.word
#             }))

#         return utterances
