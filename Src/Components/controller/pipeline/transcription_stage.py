# Standard imports
from typing import Dict, Tuple, List

from Src.components.engines.utterance import UtteranceAttributes
# Local imports
from ...utils.threads import ThreadPool
from ...organizer import Conversation, Settings
from ...engines import Engines, WatsonEngine, GoogleEngine, Utterance
from ...network import Network
from ...io import IO
from ...services import Source
from ..configurables.gb_settings import GailBotSettings, GBSettingAttrs
from .models import ExternalMethods, Payload, Utt, ProcessStatus
from ..configurables.blackboards import PipelineBlackBoard


class TranscriptionStage:
    SUPPORTED_ENGINES = ["watson", "google"]
    NUM_THREADS = 4

    def __init__(self, blackboard: PipelineBlackBoard,
                 external_methods: ExternalMethods) -> None:
        self.blackboard = blackboard
        self.external_methods = external_methods
        self.engines = Engines(IO(), Network())
        self.io = IO()
        self.thread_pool = ThreadPool(
            self.NUM_THREADS)
        self.thread_pool.spawn_threads()

    def generate_utterances(self, payload: Payload) -> None:
        try:
            # Determine if possible to transcribe
            if not self._can_transcribe(payload):
                payload.status = ProcessStatus.FAILED
                return
            # Extract the audio from the sources first and obtain a mapping
            # TODO: Assuming one audio per source, change later.
            source_audio_map = self._construct_source_to_audio_map(payload)
            payload.addons.source_to_audio_map = source_audio_map
            # Transcribe from the temp. dir
            payload.status = self._transcribe(payload)
        except Exception as e:
            print(e)

    def get_supported_engines(self) -> List[str]:
        return self.SUPPORTED_ENGINES

    ######################## PRIVATE METHODS ##################################

    def _can_transcribe(self, payload: Payload) -> bool:
        settings: Settings = payload.source.conversation.get_settings()
        if not settings.get_value(GBSettingAttrs.engine_type) \
            in self.SUPPORTED_ENGINES or \
                payload.status != ProcessStatus.READY:
            return False
        return True

    def _construct_source_to_audio_map(self, payload: Payload) -> Dict[str, str]:
        source_to_audio_map = dict()
        conversation: Conversation = payload.source.conversation
        source_paths_map = conversation.get_source_file_paths()
        source_types_map = conversation.get_source_file_types()
        for source_file_name, source_path in source_paths_map.items():
            # Extract audio from this path
            if self.io.is_supported_audio_file(source_path):
                # Move to the tmp dir.
                tmp_dir_path = conversation.get_temp_directory_path()
                self.io.copy(source_path, tmp_dir_path)
                path = "{}/{}.{}".format(
                    tmp_dir_path, self.io.get_name(
                        source_path), self.io.get_file_extension(source_path)[1])
            else:
                # Extract audio from video
                # NOTE: Assuming each video has single audio map.
                self.io.extract_audio_from_file(
                    source_path, conversation.get_temp_directory_path())
                path = "{}/{}.{}".format(
                    conversation.get_temp_directory_path(),
                    self.io.get_name(source_path), "wav")
            source_to_audio_map[source_file_name] = path
        return source_to_audio_map

    def _transcribe(self, payload: Payload) -> ProcessStatus:
        utterances_map = dict()
        source_status_map = dict()
        self._execute_transcription_threads(
            payload, utterances_map, source_status_map)
        # Convert Utterances to Utt
        utts_map = self._utterances_to_utt(utterances_map)
        # Check status
        if all(list(source_status_map.values())):
            payload.source.conversation.set_utterances(utts_map)
            return ProcessStatus.TRANSCRIBED
        else:
            return ProcessStatus.FAILED

    # --- Helpers

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
            source_status_map[source_file_name] = engine.was_transcription_successful(
            )
        except Exception as e:
            print(e)
