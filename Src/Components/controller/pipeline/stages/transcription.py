# Standard imports
from typing import Dict, Tuple, List

from Src.components.engines.utterance import UtteranceAttributes
# Local imports
from ....utils.threads import ThreadPool
from ....organizer import Conversation, Settings
from ....engines import Engines, WatsonEngine, GoogleEngine, Utterance
from ....network import Network
from ....io import IO
from ....services import Source
from ...helpers.gb_settings import GailBotSettings, GBSettingAttrs
from ..models import Payload, Utt, ProcessStatus
from ...blackboards import PipelineBlackBoard


class TranscriptionStage:

    SUPPORTED_ENGINES = ["watson", "google"]
    NUM_THREADS = 4

    def __init__(self, blackboard: PipelineBlackBoard) -> None:
        self.blackboard = blackboard
        self.engines = Engines(IO(), Network())
        self.io = IO()
        self.thread_pool = ThreadPool(
            self.NUM_THREADS)
        self.thread_pool.spawn_threads()

    def generate_utterances(self, payload: Payload) -> None:
        """
        Transcribe all the files in a single payload
        """

        # NOTE: Need to do this in a better way. Maybe attach something to
        # previously transcribed conversations
        utterance_map = payload.source.conversation.get_utterances()
        if all([len(v) > 0 for v in utterance_map.values()]):
            payload.status = ProcessStatus.TRANSCRIBED
            return
        # -----
        self._construct_source_to_audio_map(payload)
        if self._can_transcribe(payload):
            self._transcribe(payload)
        else:
            payload.status = ProcessStatus.FAILED

    ########################## GETTERS #######################################

    def get_supported_engines(self) -> List[str]:
        return self.SUPPORTED_ENGINES

    ######################## PRIVATE METHODS ##################################

    def _construct_source_to_audio_map(self, payload: Payload) -> None:
        source_to_audio_map = dict()
        conversation: Conversation = payload.source.conversation
        source_paths_map = conversation.get_source_file_paths()
        source_types_map = conversation.get_source_file_types()
        for source_file_name, source_path in source_paths_map.items():
            _, path = self._extract_audio_from_path(
                source_path, source_types_map[source_file_name],
                conversation.get_temp_directory_path())
            source_to_audio_map[source_file_name] = path
        payload.addons.source_to_audio_map = source_to_audio_map

    def _extract_audio_from_path(self, source_path: str, source_type: str,
                                 extract_dir_path: str) -> Tuple[bool, str]:

        if self.io.is_supported_audio_file(source_path):
            return (True, source_path)
        if not self.io.extract_audio_from_file(source_path, extract_dir_path):
            return (False, None)
        ####### REMOVE ########
        # TODO: This path should eventually be obtained from IO directly
        # and should not be hard-coded.
        hard_coded_path = "{}/{}.{}".format(
            extract_dir_path, self.io.get_name(source_path), "wav")
        if not self.io.is_file(hard_coded_path):
            return (False, None)
        return (True, hard_coded_path)
        ########################

    def _utterances_to_utt(self, utterances_map: Dict[str, Utterance]) \
            -> Dict[str, Utt]:
        utt_map = dict()
        for name, utterances in utterances_map.items():
            utt_map[name] = [Utt(
                utterance.get(UtteranceAttributes.speaker_label)[1],
                utterance.get(UtteranceAttributes.start_time)[1],
                utterance.get(UtteranceAttributes.end_time)[1],
                utterance.get(UtteranceAttributes.transcript)[1]
            ) for utterance in utterances]
        return utt_map

    def _can_transcribe(self, payload: Payload) -> bool:
        settings: Settings = payload.source.conversation.get_settings()
        if not settings.get_value(GBSettingAttrs.engine_type) in self.SUPPORTED_ENGINES or \
                payload.status != ProcessStatus.READY:
            return False
        for audio_path in payload.addons.source_to_audio_map.values():
            if audio_path == None:
                return False
        return True

    def _transcribe(self, payload: Payload) -> None:
        utterances_map = dict()
        source_status_map = dict()
        self._execute_transcription_threads(
            payload, utterances_map, source_status_map)
        # Convert Utterances to Utt
        utts_map = self._utterances_to_utt(utterances_map)
        # Check status
        if all(list(source_status_map.values())):
            payload.status = ProcessStatus.TRANSCRIBED
            payload.source.conversation.set_utterances(utts_map)
        else:
            payload.status = ProcessStatus.FAILED

    def _execute_transcription_threads(
            self, payload: Payload, utterances_map: Dict,
            source_status_map: Dict) -> None:
        settings: GailBotSettings = payload.source.conversation.get_settings()
        for source_file_name in payload.addons.source_to_audio_map.keys():
            if settings.get_value(GBSettingAttrs.engine_type) == "watson":
                self.thread_pool.add_task(
                    self._transcribe_watson_thread,
                    [source_file_name, payload,
                     utterances_map, source_status_map], {})
            elif settings.get_value(GBSettingAttrs.engine_type) == "google":
                self.thread_pool.add_task(
                    self._transcribe_google_thread,
                    [source_file_name, payload,
                     utterances_map, source_status_map], {})
        self.thread_pool.wait_completion()

    def _transcribe_watson_thread(
            self, source_file_name: str,
            payload: Payload, utterances_map: Dict[str, List[Utterance]],
            source_status_map: Dict[str, bool]) -> None:
        try:
            engine: WatsonEngine = self.engines.engine("watson")
            source_path = payload.addons.source_to_audio_map[source_file_name]
            settings: GailBotSettings = payload.source.conversation.get_settings()
            engine.configure(
                settings.get_value(GBSettingAttrs.watson_api_key),
                settings.get_value(GBSettingAttrs.watson_region),
                source_path,
                settings.get_value(GBSettingAttrs.watson_base_language_model),
                payload.source.hook.get_temp_directory_path(),
                settings.get_value(GBSettingAttrs.watson_language_customization_id))
            utterances = engine.transcribe()
            utterances_map[source_file_name] = utterances
            source_status_map[source_file_name] =\
                engine.was_transcription_successful()
        except Exception as e:
            print(e)

    def _transcribe_google_thread(self) -> None:
        raise Exception("Not implemented")
