import threading
from tests.services.test_data import PATH
from gailbot.core.utils.threads import ThreadPool
from google.cloud import speech_v1
import os
import io 
google_api_key = "/Users/yike/Desktop/input/googleApi/gailbot_key.json"

# Function to transcribe an audio file
def transcribe_file(file_name):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_api_key
    client = speech_v1.SpeechClient()

    # Set the audio configuration
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US'
    )
    with io.open(file_name, "rb") as audio:
                content = audio.read()
    # Set the audio file path
    audio = speech_v1.RecognitionAudio(content=content)

    # Perform the transcription
    response = client.recognize(config=config, audio=audio)

    # Print the transcription results
    for result in response.results:
        print(result.alternatives[0])
    return True


def test_multi_google():
    # List of audio file names to transcribe
    file_names = [PATH.HELLO_1, PATH.HELLO_2, PATH.HELLO_3, PATH.HELLO_4, PATH.HELLO_3]

    pool = ThreadPool(5)
    # Create a thread for each file and start the transcription process
    threads = []
    for file_name in file_names:
        thread = pool.add_task(transcribe_file, args=[file_name])
        threads.append(thread)


    # Wait for all threads to finish
    for thread in threads:
        assert pool.get_task_result(thread)
