# Standard imports
# Local imports
from ....engines import Utterance, UtteranceAttributes

class Utt:

    def __init__(self, utterance : Utterance) -> None:
        self.speaker_label = \
            utterance.get(UtteranceAttributes.speaker_label)[1]
        self.start_time_seconds =\
            utterance.get(UtteranceAttributes.start_time)[1]
        self.end_time_seconds = \
            utterance.get(UtteranceAttributes.end_time)[1]
        self.transcript = \
            utterance.get(UtteranceAttributes.transcript)[1]

    def get_speaker_label(self) -> str:
        return self.speaker_label

    def get_transcript(self) -> str:
        return self.transcript

    def get_start_time_seconds(self) -> float:
        return self.start_time_seconds

    def get_end_time_seconds(self) -> float:
        return self.end_time_seconds

