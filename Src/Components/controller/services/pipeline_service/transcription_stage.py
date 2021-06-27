## Standard imports
from Src.Components.network.network import Network
from typing import List, Dict, Tuple
from copy import deepcopy
from dataclasses import dataclass,field
# Local imports
from .....utils.manager import ObjectManager
from ....engines import Engines, WatsonEngine, GoogleEngine, Utterance
from ....io import IO
from ....organizer import Conversation
from .....utils.threads import ThreadPool
from ..organizer_service import GailBotSettings
from ..status import TranscriptionStatus
from .transcribable import Transcribable
# Third party imports

class TranscriptionStage:

    def __init__(self, num_threads : int) -> None:
        ## Vars.
        #  TODO: Determine if this should be  hard-coded or not.
        self.num_threads_transcription_thread_pool = 3
        ## Objects.
        self.engines = Engines(IO(),Network())
        self.io = IO()
        self.transcribables = ObjectManager()
        self.thread_pool = ThreadPool(num_threads)
        self.transcription_thread_pool = ThreadPool(
            self.num_threads_transcription_thread_pool)
        self.thread_pool.spawn_threads()
        self.transcription_thread_pool.spawn_threads()

    ################################## MODIFIERS ##########################

    def generate_utterances(self) -> Dict[str,TranscriptionStatus]:
        status_map = dict()
        transcribables = self.transcribables.get_all_objects()
        for _ , transcribable in transcribables.items():
            self.thread_pool.add_task(
                self._transcribe_thread,[transcribable,status_map],{})
        self.thread_pool.wait_completion()
        return status_map

    ################################## SETTERS #############################

    def add_transcribable(self, transcribable : Transcribable) -> bool:
        if not self._initialize_transcribable(transcribable):
            return False
        self.transcribables.add_object(transcribable.identifier,transcribable)

    def add_transcribables(self, transcribables : List[Transcribable]) -> bool:
        return all([self.add_transcribable(transcribable) \
            for transcribable in transcribables])

    ################################## GETTERS ################################

    def get_transcribables(self) -> Dict[str,Transcribable]:
        return self.transcribables.get_all_objects()

    def get_transcribable(self, identifier : str) -> Transcribable:
        if self.transcribables.is_object(identifier):
            return self.transcribables.get_object(identifier)

    ############################# PRIVATE METHODS ############################

    def _initialize_transcribable(self, transcribable : Transcribable) -> bool:
        conversation = transcribable.conversation
        source_paths_map = conversation.get_source_file_paths()
        source_types_map = conversation.get_source_file_types()
        for source_name, source_path in source_paths_map.items():
            # Setting status to False
            transcribable.source_status[source_name] = False
            # Getting transcribable sources.
            success, path = self._determine_transcribable_source_path(
                source_path, source_types_map[source_name],
                conversation.get_temp_directory_path())
            if not success:
                return False
            transcribable.source_to_transcribable_map[source_name] = path
        return True

    def _determine_transcribable_source_path(self,source_path : str,
            source_type : str, temp_dir_path : str) -> Tuple[bool,str]:
        if source_type == "audio":
            return (True, source_path)
        elif source_type == "video":
            if not self.io.extract_audio_from_file(source_path, temp_dir_path):
                return (False, None)
            ####### REMOVE ########
            # TODO: This path should eventually be obtained from IO directly
            # and should not be hard-coded.
            hard_coded_path = "{}/{}.{}".format(
                temp_dir_path, self.io.get_name(source_path),"wav")
            if not self.io.is_file(hard_coded_path):
                raise Exception("Extracted audio not found")
            ########################
            return (True, hard_coded_path)
        else:
            raise Exception("Source type not supported")

    #### Thread methods

    def _transcribe_thread(self, transcribable : Transcribable,
            status_map : Dict[str,bool]) -> None:
        transcribable_sources = transcribable.source_to_transcribable_map
        settings : GailBotSettings = transcribable.conversation.get_settings()
        utterances_map = dict()
        for source_name in transcribable_sources.keys():
            if settings.get_engine_type() == "watson":
                self.transcription_thread_pool.add_task(
                    self._transcribe_watson_thread,
                    [source_name, transcribable,utterances_map],{})
            elif settings.get_engine_type() == "google":
                self.transcription_thread_pool.add_task(
                    self._transcribe_google_thread,
                    [source_name,transcribable,utterances_map],{})
            else:
                raise Exception("Engine type not supported")
        self.transcription_thread_pool.wait_completion()
        # Set results.
        transcribable.conversation.set_utterances(deepcopy(utterances_map))
        # Setting conversation status
        is_successful = all(transcribable.status.values())
        if is_successful:
            transcribable.conversation.set_transcription_status(
                TranscriptionStatus.successful)
        else:
            transcribable.conversation.set_transcription_status(
                TranscriptionStatus.unsuccessful)

    def _transcribe_watson_thread(self, source_name : str,
            transcribable : Transcribable,
            utterances_map : Dict[str,Utterance]) -> None:
        engine = self.engines.engine("watson")
        settings : GailBotSettings = transcribable.conversation.get_settings()
        source_path = transcribable.source_to_transcribable_map[source_name]
        engine.configure(
            settings.get_watson_api_key(),settings.get_watson_region(),
            source_path,settings.get_watson_base_language_model(),
            settings.get_watson_language_customization_id())
        utterances = engine.transcribe()
        utterances_map[source_name] = utterances
        transcribable.source_status[source_name] = \
            engine.was_transcription_successful()

    def _transcribe_google_thread(self, source_name : str,
            transcribable : Transcribable,
            utterances_map : Dict[str,Utterance]) -> None:
        pass





