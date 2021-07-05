# Standard imports
from typing import Dict, Tuple, List
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....organizer import Conversation
from .....engines import Engines, WatsonEngine, GoogleEngine, Utterance
from .....network import Network
from .....io import IO
from ...organizer_service import GailBotSettings
from ...status import TranscriptionStatus
from ..source import Source

class TranscriptionStage:

    def __init__(self, num_threads : int) -> None:

        ## Vars.
        self.supported_engines = ["watson", "google"]
        self.num_threads_transcription_thread_pool = 3
        self.max_threads = 4
        # Thread checking
        if num_threads <= 0 or num_threads > self.max_threads:
            raise Exception("Invalid number of threads")
        ## Objects
        self.sources = ObjectManager()
        self.engines = Engines(IO(),Network())
        self.io = IO()
        self.thread_pool = ThreadPool(num_threads)
        self.transcription_thread_pool = ThreadPool(
            self.num_threads_transcription_thread_pool)
        self.thread_pool.spawn_threads()
        self.transcription_thread_pool.spawn_threads()

    ############################# MODIFIERS ##################################

    def add_source(self, source_name : str, source : Source) -> bool:
        return self.sources.add_object(source_name, source)

    def add_sources(self, sources : Dict[str,Source]) -> bool:
        return all([self.add_source(source_name, source) \
            for source_name, source in sources.items()])

    def remove_source(self, source_name : str) -> bool:
        return self.sources.remove_object(source_name)

    def clear_sources(self) -> None:
        self.sources.clear_objects()

    def generate_utterances(self) -> None:
        sources = self.sources.get_all_objects()
        # Extract all the audios for all sources first.
        for _ , source in sources.items():
            self.thread_pool.add_task(
                self._extract_source_audios, [source], {})
        self.thread_pool.wait_completion()
        # Transcribe all sources next.
        for _ , source in sources.items():
            self.thread_pool.add_task(
                self._transcribe_thread,[source],{})
        self.thread_pool.wait_completion()

    ############################ GETTERS ####################################

    def get_sources(self) -> Dict[str,Source]:
        return self.sources.get_all_objects()

    def get_source(self, source_name : str) -> Source:
        return self.sources.get_object(source_name)

    def get_supported_engines(self) -> List[str]:
        return self.supported_engines

    ############################# PRIVATE METHODS ############################

    def _extract_source_audios(self, source : Source) -> None:
        source_to_audio_map = dict()
        conversation = source.conversation
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
        # Add the dictionary to the source
        source.source_to_audio_map = source_to_audio_map

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

    def _transcribe_thread(self, source : Source) -> None:
        settings : GailBotSettings = source.conversation.get_settings()
        # All audio paths must be present and engine must be supported.
        if not self._can_transcribe_source(source) or \
                not settings.get_engine_type() in self.supported_engines:
            source.conversation.set_transcription_status(
                TranscriptionStatus.unsuccessful)
        # Transcribe using the appropriate engine.
        utterances_map = dict()
        source_status_map = dict()
        for source_file_name, _ in source.source_to_audio_map.items():
            if settings.get_engine_type() == "watson":
                self.transcription_thread_pool.add_task(
                    self._transcribe_watson_thread, [source_file_name, source,
                    utterances_map, source_status_map],{})
            elif settings.get_engine_type() == "google":
                self.transcription_thread_pool.add_task(
                    self._transcribe_google_thread, [source_file_name, source,
                    utterances_map, source_status_map],{})
        self.transcription_thread_pool.wait_completion()
        # Determine the status
        if all(list(source_status_map.values())):
            source.conversation.set_transcription_status(
                TranscriptionStatus.successful)
            # Set the conversation utterances
            source.conversation.set_utterances(utterances_map)
            # The stage has been successful for this source.
            source.transcription_successful = True
        else:
            source.conversation.set_transcription_status(
                TranscriptionStatus.unsuccessful)


    def _transcribe_watson_thread(self, source_file_name : str,
            source : Source, utterances_map : Dict[str,List[Utterance]],
            source_status_map : Dict[str,bool]) -> None:

        engine : WatsonEngine = self.engines.engine("watson")
        source_path = source.source_to_audio_map[source_file_name]
        settings : GailBotSettings = source.conversation.get_settings()
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

    def _can_transcribe_source(self, source : Source) -> bool:
        for _, audio_path in source.source_to_audio_map.items():
            if audio_path == None:
                return False
        return True
