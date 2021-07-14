# Standard imports
from typing import Dict, Tuple, List
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....organizer import Conversation
from .....engines import Engines, WatsonEngine, GoogleEngine, Utterance
from .....network import Network
from .....io import IO
from ...organizer_service import GailBotSettings, RequestType
from ...status import TranscriptionStatus
from ..pipeline_payload import SourcePayload

class TranscriptionStage:

    SUPPORTED_ENGINES = ["watson","google"]
    NUM_THREADS = 4

    def __init__(self) -> None:
        ## Objects
        self.engines = Engines(IO(),Network())
        self.io = IO()
        self.thread_pool = ThreadPool(
            self.NUM_THREADS)
        self.thread_pool.spawn_threads()

    ############################# MODIFIERS ##################################

    def generate_utterances(self, payload : SourcePayload) -> None:
        msg = "[{}] [Transcription stage] Extracting audio from sources".format(
            payload.get_source_name())
        payload.log(RequestType.FILE,msg)
        payload.set_source_to_audio_map(self._extract_source_audios(payload))
        status = self._transcribe(payload)
        msg = "[{}] [Transcription stage] Was transcription successful: {}".format(
            payload.get_source_name(),status)
        payload.log(RequestType.FILE,msg)
        payload.set_transcription_status(status)

    ########################## GETTERS #######################################

    def get_supported_engines(self) -> List[str]:
        return self.SUPPORTED_ENGINES

    ######################## PRIVATE METHODS ##################################

    def _extract_source_audios(self, payload : SourcePayload) -> Dict[str,str]:
        source_to_audio_map = dict()
        conversation = payload.get_conversation()
        source_paths_map = conversation.get_source_file_paths()
        source_types_map = conversation.get_source_file_types()
        for source_file_name, source_path in source_paths_map.items():
            success, path = self._extract_audio_from_path(
                source_path, source_types_map[source_file_name],
                conversation.get_temp_directory_path())
            if not success:
                source_to_audio_map[source_file_name] = None
            else:
                source_to_audio_map[source_file_name] = path
        return source_to_audio_map

    def _extract_audio_from_path(self, source_path : str, source_type : str,
            extract_dir_path : str) -> Tuple[bool,str]:
        if source_type == "audio":
            return (True, source_path)
        elif source_type == "video":
            if not self.io.extract_audio_from_file(source_path, extract_dir_path):
                return (False, None)
            ####### REMOVE ########
            # TODO: This path should eventually be obtained from IO directly
            # and should not be hard-coded.
            hard_coded_path = "{}/{}.{}".format(
                extract_dir_path, self.io.get_name(source_path),"wav")
            if not self.io.is_file(hard_coded_path):
                return (False, None)
            ########################
            return (True, hard_coded_path)
        else:
            return (False, None)


    def _transcribe(self, payload : SourcePayload) -> bool:

        # Verify if transcription possible
        if not self._can_transcribe_source(payload):
            payload.get_conversation().set_transcription_status(
                TranscriptionStatus.unsuccessful)
            return
        # Transcribe using the appropriate engine.
        utterances_map = dict()
        source_status_map = dict()
        settings : GailBotSettings = payload.get_conversation().get_settings()
        for source_file_name, _ in payload.get_source_to_audio_map().items():
            if settings.get_engine_type() == "watson":
                self.thread_pool.add_task(
                    self._transcribe_watson_thread, [source_file_name, payload,
                    utterances_map, source_status_map],{})
            elif settings.get_engine_type() == "google":
                self.thread_pool.add_task(
                    self._transcribe_google_thread, [source_file_name, payload,
                    utterances_map, source_status_map],{})
        self.thread_pool.wait_completion()
        # Determine the status
        if all(list(source_status_map.values())):
            payload.get_conversation().set_transcription_status(
                TranscriptionStatus.successful)
            # Set the conversation utterances
            payload.get_conversation().set_utterances(utterances_map)
            return True
        else:
            payload.get_conversation().set_transcription_status(
                TranscriptionStatus.unsuccessful)
            return False

    def _transcribe_watson_thread(self, source_file_name : str,
            payload : SourcePayload, utterances_map : Dict[str,List[Utterance]],
            source_status_map : Dict[str,bool]) -> None:
        engine : WatsonEngine = self.engines.engine("watson")
        source_path = payload.get_source_to_audio_map()[source_file_name]
        settings : GailBotSettings = payload.get_conversation().get_settings()
        engine.configure(
            settings.get_watson_api_key(),settings.get_watson_region(),
            source_path,settings.get_watson_base_language_model(),
            settings.get_watson_language_customization_id())
        utterances = engine.transcribe()
        utterances_map[source_file_name] = utterances
        source_status_map[source_file_name] = \
            engine.was_transcription_successful()

    def _transcribe_google_thread(self) -> None:
        raise Exception("Not implemented")

    def _can_transcribe_source(self, payload : SourcePayload) -> bool:
        # Engine must be supported
        settings : GailBotSettings = payload.get_conversation().get_settings()
        if not settings.get_engine_type() in self.SUPPORTED_ENGINES:
            return False
        # Audio files should be valid.
        for _, audio_path in payload.get_source_to_audio_map().items():
            if audio_path == None:
                return False
        return True
