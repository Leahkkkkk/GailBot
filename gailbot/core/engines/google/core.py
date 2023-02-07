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
    write_json, 
    is_directory, 
    make_dir,
    paths_in_dir,
    delete,
    get_name)

from gailbot.core.utils.logger import makelogger
from ...engines import exception as Err
from gailbot.configs import google_config_loader, top_level_config_loader
from gailbot.core.utils.general import get_size
from gailbot.core.utils.media import MediaHandler

logger = makelogger("google")
GOOGLE_CONFIG = google_config_loader()
TOP_CONFIG = top_level_config_loader()
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
    
    def __init__(self, google_key: Dict[str, str] = None ) -> None:
        self._init_status()
        self.workspace_directory = os.path.join(
            TOP_CONFIG.root, TOP_CONFIG.workspace.google_workspace)
        try:
            if not google_key:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS']= os.path.join(os.getcwd(),'google_key.json')
            else:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_key
            self.client = speech.SpeechClient()   
        except:
            raise Err.ConnectionError("ERROR: Failed to connect to google cloud")
        else:
            self.connected = True
            logger.info("Connected")
    
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
        
        Return:
            A list of dictionary that contains the utterance data of the 
            audio file, each part of the audio file is stored in the format 
            {speaker: , start_time: , end_time: , text: }
        """
        self._init_workspace(output_directory)
        mediaHandler = MediaHandler()
        stream = mediaHandler.read_file(audio_path)
        length = mediaHandler.info(stream)["duration_seconds"]
        if length >= GOOGLE_CONFIG.maximum_duration:
            try:
                res = self._transcribe_large_file(
                    audio_path, self.workspace_directory, output_directory)
                logger.info(res)
                return res
            except Exception as e:
                logger.error(e)
                raise Err.TranscriptionError(
                    "ERROR: Failed to transcribe large file")
        try:
            response = self.run_engine(audio_path)
        except:
            raise Err.TranscriptionError("ERROR: Google STT transcription failed")
        
        try:
            return self.prepare_utterance(output_directory, response)
        except Exception as e :
            logger.error(e)
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
            logger.error(e)
            self.transcribe_error = True
            raise Err.TranscriptionError("Google STT Transcription failed")
        else:
            self.transcribing = False
            self.transcribe_success = True
            logger.info(response.results)
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
            A list of dictionary that contains the utterance data of the 
            audio file, each part of the audio file is stored in the format 
            {speaker: , start_time: , end_time: , text: }
        """
        if not is_directory(output_directory):
            logger.debug("make  the directory ")
            print(output_directory)
            make_dir(output_directory, overwrite=True)
            logger.debug("finished making  the directory ")

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
            logger.error(e)
        else:
            return dir
    
    def _transcribe_large_file(self, audiopath: str, workspace: str, output: str):
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
            new_utt = self.prepare_utterance(output, response)
            logger.info(new_utt)
            utterances.append(new_utt)
        delete(workspace)
        return utterances
    
    def _init_workspace(self, output_directory) -> None :    
        """ 
        initialize the work space
        
        Args: 
            output_directory[str]: the output path where the transcription result 
                                    will be stored
        """ 
        try:
            if not is_directory(output_directory):
                make_dir(output_directory, overwrite=True)
            make_dir(self.workspace_directory, overwrite=True)
            assert is_directory(self.workspace_directory)
        except Exception as e:
            logger.error(e)
            raise FileExistsError("ERROR: failed to create directory")