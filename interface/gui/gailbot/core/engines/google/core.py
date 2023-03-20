# -*- coding: utf-8 -*-
# @Author: Vivian Li, Siara Small
# @Date:   2023-01-30 16:00
# @Last Modified by:  Vivian Li
# @Last Modified time: 2023-01-31 12:01:31
import os 
import io
from copy import deepcopy
from typing import Union
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import cloud_speech
from typing import Dict, List 
from gailbot.core.utils.general import (
    get_extension, 
    get_extension,
    is_directory, 
    make_dir,
    paths_in_dir,
    delete,
    get_name,
    copy)

from gailbot.core.utils.logger import makelogger
from ...engines import exception as Err
from gailbot.configs import google_config_loader, workspace_config_loader
from gailbot.core.utils.media import MediaHandler

logger = makelogger("google")
GOOGLE_CONFIG = google_config_loader()
""" TODO: 
1. google API key  
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
    
    def __init__(self, google_api_key) -> None:  
        self._init_status()
        client = GoogleCore.is_valid_google_api(google_api_key)
        self.workspace = workspace_config_loader().engine_ws.google
        assert client 
        self.client = client
        self.connected = True
        
    
    @staticmethod
    def is_valid_google_api(google_api_key: str):
        """ Given a path to a json file that stores the google api key
            return the google client if the api is valid, else return false     

        Args:
            google_api_key (str): a path to a file that stores the google api 
                                 key 

        Returns:
            Union(SpeechCient, bool): if the api key is valid, return the google 
                                      speech client, else return false 
        """
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_api_key
            client = speech.SpeechClient() 
            return client  
        except Exception as e:
            logger.error("f failed to connect to google", exc_info=e)
            return False 
        
    
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
    
    def transcribe(self, audio_path: str, payload_workspace: str) -> List[Dict[str, str]]:
        """
        Transcribes the provided audio stream using a websocket connections.
        And output the result to given output directory 

        Args:
            audio_path (str) : 
                path to audio file that will be transcribed
            output_directory (str) : 
                path to directory where the transcribed data will be stored
        
        Return:
            A list of dictionary that contains the utterance data of the 
            audio file, each part of the audio file is stored in the format 
            {speaker: , start_time: , end_time: , text: }
        """
        mediaHandler = MediaHandler()
        stream = mediaHandler.read_file(audio_path)
        length = mediaHandler.info(stream)["duration_seconds"]
        if length >= GOOGLE_CONFIG.maximum_duration:
            try:
                res = self._transcribe_large_file(
                    audio_path, payload_workspace)
                logger.info(res)
                return res
            except Exception as e:
                logger.error(e, exc_info=e)
                raise Err.TranscriptionError(
                    "ERROR: Failed to transcribe large file")
        try:
            response = self.run_engine(audio_path)
        except:
            raise Err.TranscriptionError("ERROR: Google STT transcription failed")
        
        try:
            return self.prepare_utterance(response)
        except Exception as e :
            logger.error(e, exc_info=e)
            raise Err.OutPutError(f"ERROR: Output Google STT failed, error message: {e}")
       
            
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
            format = get_extension(audio_path).lower()
            encoding = self.ENCODING_TABLE[format]
            kwargs = deepcopy(GOOGLE_CONFIG.defaults)
            
            if format == "wav" or format == "flac":
                kwargs.update({"encoding": encoding})
            else:
                kwargs.update({"encoding": encoding, "sample_rate_hertz": 16000})
            
            config = speech.RecognitionConfig(**kwargs)
            
            self.transcribing = True
            response = self.client.recognize(
                request={"config": config, "audio": audio})
        
        except Exception as e:
            logger.error(e, exc_info=e)
            self.transcribe_error = True
            raise Err.TranscriptionError("Google STT Transcription failed")
        else:
            self.transcribing = False
            self.transcribe_success = True
            logger.info(response.results)
        return response
      
    def prepare_utterance(self, response: cloud_speech.RecognizeResponse) -> List[Dict[str, str]]:
        """
        output the response data from google STT, convert the raw data to 
        utterance data which is a list of dictionary in the format 
        {speaker: , start_time: , end_time: , text: }
        
        Args: 
            output_directory(str) : output path 
            response (cloud_speech.RecognizeResponse): raw response from google 
        
        Return:
            A list of dictionary that contains the utterance data of the 
            audio file, each part of the audio file is stored in the format 
            {speaker: , start_time: , end_time: , text: }
        """
        results = response.results
        
        status_result = {
            "connected": self.connected,
            "read_audio": self.read_audio, 
            "transcribing": self.transcribing, 
            "transcribe_success": self.transcribe_success,
            "transcribe_error": self.transcribe_error,
            "output_success": True,
            "request_id": response.request_id,
        }
        
        logger.info(status_result)
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
        
        logger.info(utterances)
        return utterances
    
    def _init_status(self):
        """ 
        Initializes the status
        """
        self.connected = False
        self.read_audio = False
        self.transcribing = False
        self.transcribe_success = False
        self.transcribe_error = False
        self.output_success = False
    
    def _chunk_audio(self, audiopath: str, output: str) -> Union[str, bool]:
        """ given the audio path, chunking the audio into a series of audio
            segment
        
        Args:
            audiopath[str]: the file path to the audio file 
            outout[str]: the output of the chunked file 
            
        Return:
            Union[str, bool]: return the output directory if the chunking is 
            successful else return False
        """
        if not is_directory(output):
            make_dir(output)
        dir = os.path.join(output, "audio")
        make_dir(dir)
        basename = get_name(audiopath)
        idx = 0
        try:
            mediaHandler = MediaHandler()
            stream = mediaHandler.read_file(audiopath)
            chunks = mediaHandler.chunk(stream, GOOGLE_CONFIG.maximum_duration)
            
            for chunk in chunks:
                mediaHandler.write_stream(
                    chunk, dir, name=f"{basename}-{idx}", 
                    format=get_extension(audiopath))
                idx += 1
                
        except Exception as e:
            logger.error(e, exc_info=e)
        else:
            return dir
    
    def _transcribe_large_file(self, audiopath: str, workspace: str):
        """ 
        transcribing large audio file that exceeds the google cloud's limit for
        transcribing local file size
        
        Arg: 
            audiopath[str]: file path to the source audio file
            workspace[str]: workspace for storing temporary file required in the 
                            in the transcription process
            output[str]: the output file path of the transcription result
            
        Return: 
            A list of dictionary that contains the utterance data of the 
            audio file, each part of the audio file is stored in the format 
            {speaker: , start_time: , end_time: , text: }
        """
        audio_chunks_dir = self._chunk_audio(audiopath, workspace)
        audio_chunks = paths_in_dir(audio_chunks_dir)
        audio_chunks = sorted(audio_chunks, key = lambda file: (len(file), file))
        utterances = []
        for chunk in audio_chunks:
            logger.info(f"transcribe {chunk} in progress")
            response = self.run_engine(chunk)
            assert response
            logger.info("geting the response in chunk")
            logger.info(response)
            new_utt = self.prepare_utterance(response)
            logger.info(new_utt)
            utterances.append(new_utt)
        delete(workspace)
        return utterances
    
