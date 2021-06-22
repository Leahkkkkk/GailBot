## Standard imports
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
# Third party imports

@dataclass
class Transcribable:
    conversation : Conversation
    status : Dict[str,bool] = field(default_factory=dict)
    utterances : Dict[str,Utterance] = field(default_factory=dict)
    transcribable_sources : Dict[str,str] = field(default_factory=dict) # Source name to its transcribable path

class TranscriptionStage:

    def __init__(self, engines : Engines, io : IO, num_threads : int) -> None:
        pass
        if num_threads <= 0:
            raise Exception("Invalid number of threads")
        # Objects
        self.engines = engines
        self.io = io
        self.transcribables_manager = ObjectManager()
        # Vars.
        self.num_threads_transcription_thread_pool = 3 # TODO: Determine if this should be  hard-coded or not.
        # ThreadPools
        self.thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()
        self.transcription_thread_pool = ThreadPool(
            self.num_threads_transcription_thread_pool)
        self.transcription_thread_pool.spawn_threads()

    ################################## MODIFIERS ##########################

    def transcribe(self) -> Dict[str,TranscriptionStatus]:
        """
        Transcribe all the conversations that have been set.
        """
        status = dict()
        transcribables = self.transcribables_manager.get_all_objects()
        # Transcribe all items
        for transcribable in transcribables.values():
            self.thread_pool.add_task(
                self._transcribe_thread, [transcribable],{})
        self.thread_pool.wait_completion()
        # Generate a status mapping
        for name, transcribable in transcribables.items():
            transcribable : Transcribable
            status[name] = transcribable.conversation.get_transcription_status()
        return status

    ################################## SETTERS #############################

    def set_conversation(self, conversation : Conversation) -> bool:
        return self.set_conversations([conversation])

    def set_conversations(self, conversations : List[Conversation]) -> bool:
        """
        Set the conversation objects to transcribe.
        """
        self.transcribables_manager.clear_objects()
        for conversation in conversations:
            success, transcribable = self._create_transcribable(conversation)
            if not success:
                self.transcribables_manager.clear_objects()
                return False
            self.transcribables_manager.add_object(
                conversation.get_conversation_name(),transcribable)
        return True

    ################################## GETTERS ################################

    def get_conversations(self) -> Dict[str,Conversation]:
        conversations = dict()
        transcribables =  self.transcribables_manager.get_all_objects()
        for name, transcribable in transcribables.items():
            transcribable : Transcribable
            conversations[name] = transcribable.conversation
        return conversations

    def get_number_of_conversations(self) -> int:
        return len(self.transcribables_manager.get_object_names())

    ############################# PRIVATE METHODS #############################

    def _create_transcribable(self, conversation : Conversation) \
            -> Tuple[bool,Transcribable]:
        # create transcribable.
        transcribable = Transcribable(conversation)
        source_paths_map = conversation.get_source_file_paths()
        source_types_map = conversation.get_source_file_types()
        for source_name, source_path in source_paths_map.items():
            # Initialize statuses
            transcribable.status[source_name] = False
            # Initialize utterances
            transcribable.utterances[source_name] = None
            # Initialize transcribable_sources
            success, path = self._determine_transcribable_source_path(
                    source_path, source_types_map[source_name],
                    conversation.get_temp_directory_path())
            if not success:
                return (False, None)
            transcribable.transcribable_sources[source_name] = path
        return (True, transcribable)

    def _determine_transcribable_source_path(self,source_path : str,
            source_type : str, temp_dir_path : str) -> Tuple[bool,str]:
        if source_type == "audio":
            return (True, source_path)
        elif source_type == "video":
            if not self.io.extract_audio_from_file(source_path, temp_dir_path):
                return (False, None)
            return (True, "")
        else:
            raise Exception("Source type not supported")

    ## Transcription threads

    def _transcribe_thread(self, transcribable : Transcribable) -> None:
        transcribable_sources = transcribable.transcribable_sources
        print("Transcribable sources", transcribable_sources)
        settings : GailBotSettings = transcribable.conversation.get_settings()
        for source_name in transcribable_sources.keys():
            print("Source name ", source_name)
            if settings.get_engine_type() == "watson":
                self.transcription_thread_pool.add_task(
                    self._transcribe_watson_thread,[source_name, transcribable],{})
            elif settings.get_engine_type() == "google":
                self.transcription_thread_pool.add_task(
                    self._transcribe_google_thread, [source_name,transcribable],{})
            else:
                raise Exception("Engine type not supported")
        self.transcription_thread_pool.wait_completion()
        # Set the results
        transcribable.conversation.set_utterances(
            deepcopy(transcribable.utterances))
        # Set the data for the conversation object
        is_successful = all(transcribable.status.values())
        if is_successful:
            transcribable.conversation.set_transcription_status(
                TranscriptionStatus.successful)
        else:
            transcribable.conversation.set_transcription_status(
                TranscriptionStatus.unsuccessful)


    def _transcribe_watson_thread(self,transcribable_source : str,
            transcribable  : Transcribable) -> None:
        engine = self.engines.engine("watson")
        settings : GailBotSettings = transcribable.conversation.get_settings()
        source_path = transcribable.transcribable_sources[transcribable_source]
        print("Source path", source_path)
        engine.configure(
            settings.get_watson_api_key(),settings.get_watson_region(),
            source_path,settings.get_watson_base_language_model(),
            settings.get_watson_language_customization_id())
        utterances = engine.transcribe()
        # Setting utterances
        transcribable.utterances[transcribable_source] = utterances
        # Set the status
        transcribable.status[transcribable_source] = \
            engine.was_transcription_successful()

    def _transcribe_google_thread(self, transcribable_source : str,
            transcribable : Transcribable) -> None:
        engine = self.engines.engine("google")
        raise Exception("Google engine not currently supported")




