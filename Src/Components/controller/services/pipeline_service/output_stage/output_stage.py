# Standard imports
from typing import List, Dict, Any
# Local imports
from ......utils.threads import ThreadPool
from ......utils.manager import ObjectManager
from .....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from .....io import IO
from .....engines import Utterance, UtteranceAttributes
from ...fs_service import SourceHook
from ...gb_settings import GailBotSettings
from ..pipeline_payload import SourcePayload

class OutputStage:

    def __init__(self) -> None:
        ## Vars.
        self.metadata_extension = "json"
        self.utterances_extension = "txt"
        ## Objects
        self.io = IO()

    ################################# MODIFIERS #############################

    def output_payload(self, payload : SourcePayload) -> bool:
        if not self._create_metadata(payload) or \
                not self._write_utterances(payload):
            return False
        # Save the hook.
        result_dir = payload.conversation.get_result_directory_path()
        if not payload.hook.copy_permanent_items(result_dir):
            # Remove result directory if hook not saved.
            self.io.delete(result_dir)

    def output_payloads(self, payloads : Dict[str,SourcePayload]) -> bool:
        return all([self.output_payload(payload) \
            for payload in payloads.values()])

    ########################## PRIVATE METHODS ###############################

    def _create_metadata(self, payload : SourcePayload) -> bool:
        conversation = payload.conversation
        temp_dir = conversation.get_temp_directory_path()
        path = "{}/{}.{}".format(
            temp_dir,payload.source_name,self.metadata_extension)
        hook : SourceHook = payload.hook
        metadata = {
                "conversation_size" :conversation.get_conversation_size(),
                "conversation_source_type" : conversation.get_source_type(),
                "transcription_date" : conversation.get_transcription_date(),
                #"transcription_status" : conversation.get_transcription_status(),
                "transcription_time" : conversation.get_transcription_time(),
                "transcriber_name" : conversation.get_transcriber_name(),
                "number_of_source_files" : conversation.number_of_source_files(),
                "number_of_speakers" : conversation.number_of_speakers(),
                "source_file_names" : conversation.get_source_file_names(),
                "source_file_types" : conversation.get_source_file_types(),
                "result_directory_path" : conversation.get_result_directory_path(),
                "source_path" : conversation.get_source_path()}
        # Write new file to the temp directory, add to hook and delete.
        if not self.io.write(path,metadata, True) or \
                not hook.add_to_source("metadata",path,True) or \
                not self.io.delete(path):
            return False
        return True

    def _write_utterances(self, payload : SourcePayload) -> bool:
        conversation = payload.conversation
        temp_dir = conversation.get_temp_directory_path()
        hook : SourceHook = payload.hook
        utterances_map = conversation.get_utterances()
        for source_name, utterances in utterances_map.items():
            data = list()
            for utt in utterances:
                msg = "{}: {} {}_{}".format(
                    utt.get(UtteranceAttributes.speaker_label)[1],
                    utt.get(UtteranceAttributes.transcript)[1],
                    utt.get(UtteranceAttributes.start_time)[1],
                    utt.get(UtteranceAttributes.end_time)[1])
                data.append(msg)
            data = "\n".join(data)
            file_path = "{}/{}.{}".format(
                temp_dir,source_name, self.utterances_extension)
            if not self.io.write(file_path,data,True) or \
                    not hook.add_to_source(source_name, file_path, True) or \
                    not self.io.delete(file_path):
                return False
        return True

