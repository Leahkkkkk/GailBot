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
        
        # get the info of audio source and preprocess the audio if needed 
        mediaHandler = MediaHandler()
        stream = mediaHandler.read_file(audio_path)
        info = mediaHandler.info(stream)
        logger.info(f"the audio file information is {info}")
        
        audio_duration = info["duration_seconds"]
        audio_channels = info["channels"] 
        audio_format = info["format"]
       
        #  convert stereo to mono 
        if audio_channels > 1:
            l_stream, _ = mediaHandler.stereo_to_mono(stream)
            audio_path = mediaHandler.write_stream(l_stream, out_dir=payload_workspace, name=get_name(audio_path), format=info["format"])
            
        # convert the wav file to all bit 16 bit
        if audio_format.lower() == "wav":
            wav_copy_ws = os.path.join(payload_workspace, f"{get_name(audio_path)}_wav_16bit")
            if not is_directory(wav_copy_ws):
                make_dir(wav_copy_ws)
            output_for16 = os.path.join(wav_copy_ws, f"{get_name(audio_path)}_16bit.wav")
            audio_path = MediaHandler.convert_to_16bit_wav(audio_path, output_for16)
        
        # chunk the audio lager than 60 seconds
        if audio_duration >= GOOGLE_CONFIG.maximum_duration:
            logger.info(f"audio length exceeds maximum limit")
            # get the duration each chunk 
            chunk_duration = GoogleCore._get_chunk_duration(audio_path, audio_duration)
            # chunk the file 
            audio_list = MediaHandler.chunk_audio_to_outpath(audio_path, payload_workspace, chunk_duration)
        else:
            audio_list = [audio_path]
            
        try:
            return  self._transcribe_list_file(audio_list, payload_workspace)
        except Exception as e:
            logger.error(e, exc_info=e)
            raise Err.TranscriptionError("ERROR: Google STT transcription failed")
        
    def _run_engine(self, audio_path: str, workspace) -> cloud_speech.RecognizeResponse:
        """ 
        run the google STT engine to transcribe the file 
        
        Args: 
            audio_path (str):
                path to audio file that will be transcribed
        
        Return (cloud_speech.RecognizeResponse):
            return the response data from google STT 
        """
        try:
            # initialize client
            client = speech.SpeechClient() 
            
            # preprocessing the file 
            format = get_extension(audio_path).lower()
            encoding = self.ENCODING_TABLE[format]
            kwargs = deepcopy(GOOGLE_CONFIG.defaults)
            
            # add additional key word arguments for file that is no in wav or flac format
            if not (format == "wav" or format == "flac"):
                kwargs.update({"encoding": encoding, "sample_rate_hertz": 16000})

            # read audio file 
            with io.open(audio_path, "rb") as audio:
                content = audio.read()
                audio = speech.RecognitionAudio(content = content)
                self.read_audio = True
           
            # transcribe audio file 
            config = speech.RecognitionConfig(**kwargs)
            self.transcribing = True
            response = client.recognize(config=config, audio=audio)
        
        except Exception as e:
            logger.error(e, exc_info=e)
            self.transcribe_error = True
            raise Err.TranscriptionError("Google STT Transcription failed")
        else:
            self.transcribing = False
            self.transcribe_success = True
            logger.info(response.results)
        return response
      
    def _prepare_utterance(self, response: cloud_speech.RecognizeResponse, start_time = 0) -> List[Dict[str, str]]:
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
                    "start": word.start_time.seconds + start_time,
                    "end":   word.end_time.seconds + start_time,
                    "text":word.word,
                    "speaker": word.speaker_tag
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
    
    def _transcribe_list_file(self, audios: List[str], workspace) -> List[Dict[str, str]]:
        """transcribe a list of audios and return the utterance result

        Args:
            audios (List[str]): a list of path to audio source
            workspace (str): the path to workspace

        Returns:
            List[Dict[str, str]]: a list that represent the utterance result
        """
        utterances = []
        start_time = 0 
        for audio in audios:
            logger.info(f"transcribe {audio} in progress")
            response = self._run_engine(audio, workspace)
            assert response
            logger.info("geting the response in chunk")
            logger.info(response)
            new_utt = self._prepare_utterance(response, start_time)
            if len(new_utt):
                start_time = new_utt[-1]["end_time"]
                logger.info(new_utt)
                utterances.extend(new_utt)
        return utterances
    
    @staticmethod
    def _get_chunk_duration(file_path: str, file_duration: int):

        duration = GOOGLE_CONFIG.maximum_duration
        filesize = os.path.getsize(file_path)
        num_chunks = file_duration // GOOGLE_CONFIG.maximum_duration
        size_60 = filesize / num_chunks
        if size_60 >= GOOGLE_CONFIG.maximum_size:
            duration = duration * (GOOGLE_CONFIG.maximum_size / size_60) 
        logger.info(f"chunk audio to {duration}")
        return duration
    