# -*- coding: utf-8 -*-
# @Author: Vivian Li, Siara Small
# @Date:   2023-01-30 16:00
# @Last Modified by:  Vivian Li
# @Last Modified time: 2023-01-31 12:01:31

import os 
import io
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import cloud_speech
from typing import Dict, List 
from gailbot.core.utils.general import (
    get_extension, 
    write_json, 
    is_directory, 
    make_dir)
from tests.logger import makelogger
from ...engines import exception as Err
test_logger = makelogger("google")

""" TODO: 
    1. Documentation 
    2. the original data from google is not json serializable, need 
       to convert to json serializable form 
    3. test for file with mp3 and wav format passes the tests, need to test for 
        opus 
    4. google API key  

"""
class GoogleCore: 
    """
    Implement core functionalities to transcribe an audio file through 
    google STT engine
    """
    
    ENCODING_TABLE = {
        "wav": speech.RecognitionConfig.AudioEncoding.LINEAR16, 
        "mp3": speech.RecognitionConfig.AudioEncoding.MP3,
        "opus": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        "flac": speech.RecognitionConfig.AudioEncoding.FLAC,
        "amr": speech.RecognitionConfig.AudioEncoding.AMR
    }
    
    def __init__(self, google_key: Dict[str, str] = None ) -> None:
        
        self._init_status()
        try:
            if not google_key:
                """ TODO: replace with user credential """
                os.environ['GOOGLE_APPLICATION_CREDENTIALS']= os.path.join(os.getcwd(),'google_key.json')
            else:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_key
            self.client = speech.SpeechClient()   
        except:
            raise Err.ConnectionError
        else:
            self.connected = True
            test_logger.info("Connected")
    
    @property
    def supported_formats(self) -> List[str]:
        """
        Access the supported audio formats 

        Returns:
            List[str] : list of supported formats
        """
        return list[self.ENCODING_TABLE]

    def is_file_supported(self, file: str) -> bool:
        """
        Determines if a given file is supported

        Args:
            file (str) : file name to check if supported

        Returns: True if the file is supported, false if not.
        """
        return get_extension(file) in self.supported_formats
    
    def transcribe(self, audio_path: str, output_directory:str) -> List[Dict[str, str]]:
        """
        Transcribes the provided audio stream using a websocket connections.
        And output the result to given output directory 

        Args:
            audio_path (str) : 
                path to audio file that will be transcribed
            output_directory (str) : 
                path to directory where the transcribed data will be stored
        """
        
        try:
            response = self.run_engine(audio_path)
        except:
            raise Err.TranscriptionError
        
        try:
            return self.prepare_utterance(output_directory, response)
        except Exception as e :
            test_logger.error(e)
            raise Err.OutPutError
       
            
    def run_engine(self, audio_path: str) -> cloud_speech.RecognizeResponse:
        """ 
        run the google STT engine to transcribe the file 
        
        Args: 
            audio_path (str):
                path to audio file that will be transcribed
        
        Return (cloud_speech.RecognizeResponse):
            return the response data from google STT 
        """
        try:
            with io.open(audio_path, "rb") as audio:
                content = audio.read()
                audio = speech.RecognitionAudio(content = content)
                self.read_audio = True
            encoding = self.ENCODING_TABLE[get_extension(audio_path)]
            config = speech.RecognitionConfig(
                encoding=encoding,
                enable_automatic_punctuation=True,
                enable_speaker_diarization=True,
                enable_word_time_offsets=True,
                language_code="en-US",
            )
            self.transcribing = True
            response = self.client.recognize(
                request={"config": config, "audio": audio})
        
        except Exception as e:
            test_logger.error(e)
            self.transcribe_error = True
            raise Err.TranscriptionError
        else:
            self.transcribing = False
            self.transcribe_success = True
            test_logger.info(response.request_id)
            test_logger.info(response.speech_adaptation_info)
            test_logger.info(response.results)
            test_logger.info(response.total_billed_time)
        return response
    
    
    def prepare_utterance(self, output_directory: str, 
                          response: cloud_speech.RecognizeResponse) -> List[Dict[str, str]]:
        """
        output the response data from google STT, convert the raw data to 
        utterance data which is a list of dictionary in the format 
        {speaker: , start_time: , end_time: , text: }
        
        Args: 
            output_directory(str) : output path 
            response (cloud_speech.RecognizeResponse): raw response from google 
        
        Return:
            a list of dictionary that contains the output data
        """
        if not is_directory(output_directory):
            test_logger.debug("make  the directory ")
            print(output_directory)
            make_dir(output_directory, overwrite=True)
            test_logger.debug("finished making  the directory ")

        results = response.results
        """ TODO: the original data from google is not json serializable, need 
                  to convert to json serializable form 
        """
        # write_json(os.path.join(output_directory, "data.json"), {"results": results})
        status_result = {
            "connected": self.connected,
            "read_audio": self.read_audio, 
            "transcribing": self.transcribing, 
            "transcribe_success": self.transcribe_success,
            "transcribe_error": self.transcribe_error,
            "output_success": True,
            "request_id": response.request_id,
        }
        
        write_json(os.path.join(output_directory, "results.json"), status_result)

        """ Prepare Utterance """
        utterances = list()
        for result in results:
            for word in result.alternatives[0].words:
                utt = {
                    "speaker": word.speaker_tag,
                    "start_time": word.start_time.seconds,
                    "end_time":word.end_time.seconds,
                    "text":word.word
                }
                utterances.append(utt)
        test_logger.info(utterances)
        return utterances
    
    def _init_status(self):
        """ initialize the status  """
        self.connected = False
        self.read_audio = False
        self.transcribing = False
        self.transcribe_success = False
        self.transcribe_error = False
        self.output_success = False