from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.types import SpeakerDiarizationConfig
from google.protobuf.wrappers_pb2 import BoolValue
import os
import io
from tests.logger import makelogger

test_logger  = makelogger("test_google")

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= os.path.join(os.getcwd(),'google_key.json')
client = speech.SpeechClient()
audio = os.path.join(os.getcwd(), "data/test_file/audio_file_input/test.wav")

with io.open(audio, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_separate_recognition_per_channel= False, 
    enable_automatic_punctuation=True,
    # diarization_speaker_count=2,
    enable_speaker_diarization=True,
    language_code="en-US",
    enable_word_time_offsets=True,
)

# Sends the request to google to transcribe the audio
response = client.recognize(request={"config": config, "audio": audio})
# Reads the response
test_logger.info(response.request_id)
test_logger.info(response.speech_adaptation_info)
test_logger.info(response.results)
test_logger.info(response.total_billed_time)
for result in response.results:
    result.alternatives[0].words[0].speaker_tags
    test_logger.info("Transcript: {}".format(result.alternatives[0].transcript))
    test_logger.info(f"raw: {result}")
    # print(result)
    

"""  """

type_match = {
 "wav": speech.RecognitionConfig.AudioEncoding.LINEAR16, 
 "mp3": speech.RecognitionConfig.AudioEncoding.MP3,
 "opus": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
 
}

