# -*- coding: utf-8 -*-
# @Author: Vivian Li, Siara Small
# @Date:   2023-01-30 16:00
# @Last Modified by:  Vivian Li
# @Last Modified time: 2023-01-31 12:01:31

# stdlib import
import os 
import io
from copy import deepcopy
from typing import Union
from urllib import request
from typing import Dict, List 

# internal import
from gailbot.core.utils.general import (
    get_extension, 
    get_extension,
    is_directory, 
    make_dir,
    get_name)
from gailbot.core.utils.download import is_internet_connected
from gailbot.core.utils.logger import makelogger
from ...engines import exception as EXCEPTION
from gailbot.configs import google_config_loader, workspace_config_loader
from gailbot.core.utils.media import MediaHandler

#external import
from google.cloud.speech_v1p1beta1.types import cloud_speech
from google.cloud import speech_v1p1beta1 as speech

logger = makelogger("google")
GOOGLE_CONFIG = google_config_loader()

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
    
    def __init__(self, google_api_key_config) -> None:  
        """initialize an instance of google engine

        Args:
            google_api_key_config (str): path to a json file that stores
            google cloud speech to text api key
        """     
        self._init_status()
        client = GoogleCore.is_valid_google_api(google_api_key_config)
        self.workspace = workspace_config_loader().engine_ws.google
        assert client 
        self.connected = True
        self.current_chunk_duration = GOOGLE_CONFIG.maximum_duration
        
    
    @staticmethod
    def is_valid_google_api(google_api_key_config: str):
        """ Given a path to a json file that stores the google api key
            return the google client if the api is valid, else return false     

        Args:
            google_api_key_config (str): a path to a file that stores the google api 
                                 key 

        Returns:
            Union(SpeechCient, bool): if the api key is valid, return the google 
                                      speech client, else return false 
        """
        try:
            assert get_extension(google_api_key_config) == "json", "The google api key file is in wrong format"
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_api_key_config
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
            {speaker: , start_time: , end: , text: }
        """
        logger.info("start transcribing audio using google cloud STT")
        if not is_internet_connected():
            raise EXCEPTION.TranscriptionError(EXCEPTION.ERROR.CONNECTION_ERROR)
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
            logger.info("detect stereo audio file, converting to mono file")
            l_stream, _ = mediaHandler.stereo_to_mono(stream)
            audio_path = mediaHandler.write_stream(l_stream, out_dir=payload_workspace, name=get_name(audio_path), format=info["format"])
            
        # convert the wav file to all bit 16 bit
        if audio_format.lower() == "wav":
            logger.info("detect wav file, converting to wav 16 bit header file")
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
            self.current_chunk_duration = chunk_duration
            # chunk the file 
            audio_list = MediaHandler.chunk_audio_to_outpath(audio_path, payload_workspace, chunk_duration)
        else:
            audio_list = [audio_path]
            
        try:
            return  self._transcribe_list_file(audio_list, payload_workspace)
        except Exception as e:
            logger.error(e, exc_info=e)
            raise EXCEPTION.TranscriptionError(EXCEPTION.ERROR.GOOGLE_TRANSCRIPTION_FAILED)
        
    def _run_engine(self, audio_path: str, workspace) -> cloud_speech.RecognizeResponse:
        """ 
        run the google STT engine to transcribe the file 
        
        Args: 
            audio_path (str):
                path to audio file that will be transcribed
        
        Return (cloud_speech.RecognizeResponse):
            return the response data from google STT 
        """
        logger.info(f"rung google engine on file {audio_path}")
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
            raise EXCEPTION.TranscriptionError(EXCEPTION.ERROR.GOOGLE_TRANSCRIPTION_FAILED)
        else:
            logger.info("get google response ")
            self.transcribing = False
            self.transcribe_success = True
        return response
      
    def _prepare_utterance(self, response: cloud_speech.RecognizeResponse, offset = 0) -> List[Dict[str, str]]:
        """
        output the response data from google STT, convert the raw data to 
        utterance data which is a list of dictionary in the format 
        {speaker: , start_time: , end: , text: }
        
        Args: 
            output_directory(str) : output path 
            response (cloud_speech.RecognizeResponse): raw response from google 
        
        Return:
            A list of dictionary that contains the utterance data of the 
            audio file, each part of the audio file is stored in the format 
            {speaker: , start_time: , end: , text: }
        """

        results = response.results
        logger.info("get the google response")
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
            alternative = result.alternatives[0]
            if alternative.transcript:
                for word in alternative.words:
                    utt = {
                        "start":word.start_time.total_seconds() + float(offset), 
                        "end":word.end_time.total_seconds() + float(offset),
                        "text": word.word,
                        "speaker": str(word.speaker_tag)
                    }
                    utterances.append(utt)
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
        offset = 0.0
        logger.info(audios)
        for audio in audios:
            logger.info(f"transcribe {audio} in progress")
            response = self._run_engine(audio, workspace)
            assert response
            logger.info("geting the response in chunk")
            new_utt = self._prepare_utterance(response, offset)
            utterances.extend(new_utt)
            offset += self.current_chunk_duration 
        return utterances
    
    @staticmethod
    def _get_chunk_duration(file_path: str, file_duration: int) -> int:
        """given the file path and file duration calculate the expected 
           chunk duration that is able to send the chunked file to googl cloud 

        Args:
            file_path (str): a str to the file path
            file_duration (int): the lenth of the file 

        Returns:
            int: the expected duration of each audio chunk 
        """
        duration = GOOGLE_CONFIG.maximum_duration
        filesize = os.path.getsize(file_path)
        num_chunks = file_duration // GOOGLE_CONFIG.maximum_duration
        size_60 = filesize / num_chunks
        if size_60 >= GOOGLE_CONFIG.maximum_size:
            duration = duration * (GOOGLE_CONFIG.maximum_size / size_60) 
        logger.info(f"chunk audio to {duration}")
        return duration
    