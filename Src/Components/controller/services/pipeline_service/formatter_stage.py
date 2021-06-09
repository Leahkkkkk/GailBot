# Standard library imports
from typing import List
# Local imports
from ....organizer import Conversation
from ....engines import Utterance, UtteranceAttributes
from ....io import IO
from .....utils.threads import ThreadPool
from ..organizer_service import GailBotSettings
# Third party imports

class FormatterStage:

    def __init__(self, io : IO, num_threads : int) -> None:
        self.meta_extension = "json"
        self.meta_file_name = "meta"
        self.io = io
        if num_threads <= 0:
            raise Exception("Invalid number of threads")
        self.thread_pool = ThreadPool(num_threads)
        self.thread_pool.spawn_threads()
        self.conversations = list()

    ################################## SETTERS ################################

    def set_conversations(self, conversations : List[Conversation]) -> None:
        self.conversations = conversations

    # TODO: Add a setting to define the output format.
    def format_and_save_conversations(self) -> None:
        for conversation in self.conversations:
            self.thread_pool.add_task(
                self._save_conversation_thread, [conversation], {})
        self.thread_pool.wait_completion()

    ############################# PRIVATE METHODS #############################

    def _save_conversation_thread(self, conversation : Conversation) -> None:
        result_dir_path = conversation.get_result_directory_path()
        self._create_conversation_metadata_file(conversation)
        self._create_utterance_files(conversation)

    def _create_conversation_metadata_file(self, conversation : Conversation) -> None:
        # TODO: Change this to make a hidden file of specified type.
        # TODO: Need to change IO to make the above possible.

        # MetaDatafile includes
        file_path = "{}/{}.{}".format(conversation.get_result_directory_path(),
            self.meta_file_name, self.meta_extension)
        meta_data = {
            "conversation_name" : conversation.get_conversation_name(),
            "conversation_size" : conversation.get_conversation_size(),
            "source_type" : conversation.get_source_type(),
            "source_path" : conversation.get_source_path(),
            "transcription_date" : conversation.get_transcription_date(),
            "transcription_status" : conversation.get_transcription_status(),
            "transcription_start_time" : conversation.get_transcription_time(),
            "transcriber_name" : conversation.get_transcriber_name(),
            "number_of_source_files" : conversation.number_of_source_files(),
            "number_of_speakers" : conversation.number_of_speakers(),
            "source_file_details" : conversation.get_source_file_paths(),
            "source_file_types" : conversation.get_source_file_types()}
        self.io.write(file_path,meta_data,True)

    def _create_utterance_files(self, conversation : Conversation) -> None:
        for name, utterances in conversation.get_utterances():
            # TODO: Change the file format later
            self._create_utterances_file(
                conversation.get_result_directory_path(), name, utterances,"txt")

    def _create_utterances_file(self, result_dir_path : str, filename : str,
            utterances : List[Utterance], extension : str) -> None:
        file_path = "{}/{}.{}".format(result_dir_path, filename, extension)
        self.io.write(file_path,utterances,True)



