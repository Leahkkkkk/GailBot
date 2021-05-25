## Standard imports
from typing import List, Dict
from copy import deepcopy
# Local imports
from ....engines import Engines, WatsonEngine, GoogleEngine, Utterance
from ....io import IO
from ....organizer import Conversation
from .....utils.threads import ThreadPool
from ..organizer_service import GailBotSettings
from ..status import TranscriptionStatus
# Third party imports

class TranscriptionStage:

    def __init__(self, engines : Engines, io : IO, num_threads : int) -> None:
        self.engines = engines
        self.io = io
        if num_threads <= 0:
            raise Exception("Invalid number of threads")
        # Thread pools.
        self.thread_pool = ThreadPool(num_threads)
        self.transcription_thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()
        self.transcription_thread_pool.spawn_threads()
        self.conversations = list()

    def set_conversations(self, conversations : List[Conversation]) -> None:
        self.conversations = conversations

    def transcribe(self) -> None:
        for conversation in self.conversations:
            self.thread_pool.add_task(
                self._transcribe_conversation_thread,[conversation],{})
        self.thread_pool.wait_completion()


    ############################# PRIVATE METHODS #############################

    def _transcribe_conversation_thread(self, conversation : Conversation) \
                -> None:
        # Initializing objects for current conversation.
        status = list()
        results = dict()
        settings : GailBotSettings = conversation.get_settings()
        engine_type = settings.get_engine_type()
        engine = self.engines.engine(engine_type)
        # Transcribe each data file in the conversation
        source_paths = conversation.get_source_file_paths()
        for name, path in source_paths.items():
            if engine_type == "watson":
                self.transcription_thread_pool.add_task(
                    self._transcribe_using_watson_thread,
                    [engine,name,path,results,status,settings],{})
            elif engine_type == "google":
                self.transcription_thread_pool.add_task(
                    self._transcribe_using_google_thread,[],{})
            else:
                raise Exception("Invalid engine type")
        # Wait for all files in this conversation to complete.
        self.transcription_thread_pool.wait_completion()
        if all(status):
            conversation.set_transcription_status(
                TranscriptionStatus.successful)
        else:
            conversation.set_transcription_status(
                TranscriptionStatus.unsuccessful)
        conversation.set_utterances(deepcopy(results))

    def _transcribe_using_watson_thread(self, engine : WatsonEngine,
            source_name : str, source_path : str, results : Dict[str,Utterance],
            status : List[bool], settings : GailBotSettings) -> None:
        engine.configure(
            settings.get_watson_api_key(),settings.get_watson_region(),
            source_path,settings.get_watson_base_language_model(),
            settings.get_watson_language_customization_id())
        utterances = engine.transcribe()
        results[source_name] = utterances
        status.append(engine.was_transcription_successful())

    def _transcribe_using_google_thread(self) -> None:
        raise Exception("Not implemented")
