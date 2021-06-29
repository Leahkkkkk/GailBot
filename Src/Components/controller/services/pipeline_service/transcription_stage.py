# Standard library imports
from typing import Any, List, Dict, Tuple
from copy import deepcopy
# Local imports
from .....utils.threads import ThreadPool
from ....organizer import Conversation
from ....engines import Engines, WatsonEngine, GoogleEngine, Utterance
from ....network import Network
from ....io import IO
from ..organizer_service import GailBotSettings
from ..status import TranscriptionStatus

class TranscriptionStage:

    def __init__(self) -> None:
        ## Vars.
        self.num_threads_transcription_thread_pool = 3
        self.num_threads = 3
        ## Objects
        self.engines = Engines(IO(),Network())
        self.io = IO()
        self.thread_pool = ThreadPool(self.num_threads)
        self.transcription_thread_pool = ThreadPool(
            self.num_threads_transcription_thread_pool)
        self.thread_pool.spawn_threads()
        self.transcription_thread_pool.spawn_threads()

    def generate_utterances(self, conversations : Dict[str,Conversation]) \
            -> Any:
        # Extract sources for all conversations.
        conversations_audio_sources = dict()
        conversations_status_maps = dict()
        for name, conversation in conversations.items():
            # Extract conversation audio sources.
            source_to_audio_map = self._extract_conversation_audios(conversation)
            conversations_audio_sources[name] = source_to_audio_map
            # Transcribe all sources in conversation.
            self.thread_pool.add_task(
                self._transcribe_thread,
                [conversation,source_to_audio_map,conversations_status_maps],
                 {})
        self.thread_pool.wait_completion()
        # Return the results for all conversations.
        return {
            "conversations_audio_sources" : conversations_audio_sources,
            "conversations_status_maps" : conversations_status_maps}

    ############################# PRIVATE METHODS ############################

    def _extract_conversation_audios(self, conversation : Conversation) \
            -> Dict[str,str]:
        source_to_audio_map = dict()
        source_paths_map = conversation.get_source_file_paths()
        source_types_map = conversation.get_source_file_types()
        for source_name, source_path in source_paths_map.items():
            success, path = self._extract_audio_from_path(
                source_path, source_types_map[source_name],
                conversation.get_temp_directory_path())
            if not success:
                source_to_audio_map[source_name] = None
            else:
                source_to_audio_map[source_name] = path
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

    def _transcribe_thread(self, conversation : Conversation,
            source_to_audio_map : Dict[str,str],
            conversation_status_map : Dict[str,bool]) -> None:

        utterances_map = dict()
        source_status_map = dict()
        settings : GailBotSettings = conversation.get_settings()
        for source_name, source_path in source_to_audio_map.items():
            if settings.get_engine_type() == "watson":
                self.transcription_thread_pool.add_task(
                    self._transcribe_watson_thread,
                    [source_name, source_path, settings,utterances_map,
                    source_status_map], {})
            elif settings.get_engine_type() == "google":
                self.transcription_thread_pool.add_task(
                    self._transcribe_google_thread,
                    [source_name, source_path, settings, utterances_map,
                    source_status_map], {})
            else:
                raise Exception("Engine type not supported")
        self.transcription_thread_pool.wait_completion()
        # Set results
        conversation_status_map[conversation.get_conversation_name()] \
            = source_status_map
        conversation.set_utterances(deepcopy(utterances_map))
        # Set the status
        if all([conversation_status_map.values()]):
            conversation.set_transcription_status(
                TranscriptionStatus.successful)
        else:
            conversation.set_transcription_status(
                TranscriptionStatus.unsuccessful)

    def _transcribe_watson_thread(self, source_name, source_path,
            settings : GailBotSettings,
            utterances_map : Dict[str,Utterance],
            conversation_status_map : Dict[str,bool]) -> None:
        engine = self.engines.engine("watson")
        engine.configure(
            settings.get_watson_api_key(),settings.get_watson_region(),
            source_path,settings.get_watson_base_language_model(),
            settings.get_watson_language_customization_id())
        utterances_map[source_name] = engine.transcribe()
        conversation_status_map[source_name] = \
            engine.was_transcription_successful()

    def _transcribe_google_thread(self, conversation : Conversation) -> None:
        pass




