from google.cloud import speech_v1 as speech
PROJECT_ID = "gailbot-testing"
PROJECT_NUMBER = "359211140737"

def speech_to_text(config, audio):
    client = speech.SpeechClient(credentials=PROJECT_ID)
    response = client.recognize(config=config, audio=audio)
    print_sentences(response)


def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        print(f"Transcript: {transcript}")
        print(f"Confidence: {confidence:.0%}")


config = dict(language_code="en-US")
audio = dict(uri="gs://cloud-samples-data/speech/brooklyn_bridge.flac")
speech_to_text(config, audio)