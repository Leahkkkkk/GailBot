# Standard imports
# Local imports
from ....engines import Utterance, UtteranceAttributes

class Utt:
    """
    Wrapper for an utterance object that is intended to be used with
    PluginInput objects.
    """

    def __init__(self, utterance : Utterance) -> None:
        """
        Args:
            utterance (Utterance)
        """
        self.speaker_label = \
            utterance.get(UtteranceAttributes.speaker_label)[1]
        self.start_time_seconds =\
            utterance.get(UtteranceAttributes.start_time)[1]
        self.end_time_seconds = \
            utterance.get(UtteranceAttributes.end_time)[1]
        self.transcript = \
            utterance.get(UtteranceAttributes.transcript)[1]

    def get_speaker_label(self) -> str:
        """
        Obtain the speaker label associated with this utterance.
        """
        return self.speaker_label

    def get_transcript(self) -> str:
        """
        Obtain the transcript / text associated with this turn.
        """
        return self.transcript

    def get_start_time_seconds(self) -> float:
        """
        Obtain the start time, in seconds, for this turn.
        """
        return self.start_time_seconds

    def get_end_time_seconds(self) -> float:
        """
        Obtain the end time, in seconds for this turn.
        """
        return self.end_time_seconds

