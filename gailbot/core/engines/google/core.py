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

class GoogleCore: 
    
    ENCODING_TABLE = {
        "wav": speech.RecognitionConfig.AudioEncoding.LINEAR16, 
        "mp3": speech.RecognitionConfig.AudioEncoding.MP3,
        "opus": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
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
        return ["mp3", "wav", "opus"]

    def is_file_supported(self, file: str) -> bool:
        return get_extension(file) in self.supported_formats
    
    def transcribe(self, audio_path: str, output_directory:str) -> List[Dict[str:str]]:
        try:
            response = self.run_engine(audio_path)
        except:
            raise Err.TranscriptionError
        
        try:
            return self.prepare_utterance(response, output_directory)
        except:
            raise Err.OutPutError
       
            
    def run_engine(self, audio_path: str) -> cloud_speech.RecognizeResponse:
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
    
    
    def prepare_utterance(self, output_directory: str, response: cloud_speech.RecognizeResponse) -> List[Dict[str:str]]:
        if not is_directory(output_directory):
            make_dir(output_directory, overwrite=True)
        
        results = response.results
        write_json(os.path.join(output_directory, "data.json"), {"results": results})
        
        """ TODO: check this result format """
        
        
        write_json(os.path.join(output_directory, "results.json"), results)
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
        return utterances
    
    def _init_status(self):
        self.connected = False
        self.read_audio = False
        self.transcribing = False
        self.transcribe_success = False
        self.transcribe_error = False
        self.output_success = False