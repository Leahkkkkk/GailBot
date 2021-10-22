from typing import Dict, Any, List
from abc import abstractmethod

from Src.components.organizer.conversation import Conversation
# Local imports
from ....io import IO
from ....plugin_manager import Plugin
from ..models import Payload, Utt, ProcessStatus
from ....plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ...helpers.gb_settings import GBSettingAttrs, GailBotSettings


class OutputStage:

    METADATA_EXTENSION = "json"
    METADATA_NAME = "metadata"
    RAW_EXTENSION = "gb"

    def __init__(self) -> None:
        self.io = IO()

    ############################# MODIFIERS ##################################

    def output(self, payload: Payload) -> None:
        # Write the metadata
        self._write_metadata(payload)
        # Write the raw utterance files.
        self._write_raw_utterances(payload)
        # Save the hook to the result directory.
        payload.source.hook.save()

    ########################## PRIVATE METHODS ###############################

    def _write_metadata(self, payload: Payload) -> None:
        conversation: Conversation = payload.source.conversation
        # Generate metadata.
        data = {
            "conversation_name": conversation.get_conversation_name(),
            "settings_profile_name": payload.source.settings_profile_name,
            "source_path": conversation.get_source_path(),
            "conversation_source_type": conversation.get_source_type(),
            "conversation_size": conversation.get_conversation_size(),
            "transcription_date": conversation.get_transcription_date(),
            # TODO: the status returned is not a string. Fix this.
            # "transcription_status" : conversation.get_transcription_status(),
            "transcription_time": conversation.get_transcription_time(),
            "transcriber_name": conversation.get_transcriber_name(),
            "number_of_speakers": conversation.number_of_speakers(),
            "number_of_source_files": conversation.number_of_source_files(),
            "source_file_names": conversation.get_source_file_names(),
            "source_file_types": conversation.get_source_file_types(),
            "result_directory_path": conversation.get_result_directory_path(), }
        # "outputs": payload.get_output_names(),
        # "process_status": payload.status,
        # "plugins_applied": list(payload.get_analysis_plugin_summaries().keys()),
        path = "{}/{}_metadata.{}".format(
            payload.source.hook.get_temp_directory_path(),
            payload.source.source_name, self.METADATA_EXTENSION)
        self.io.write(path, data, True)

    def _write_raw_utterances(self, payload: Payload) -> None:
        # Has to be transcribed or plugins applied
        if payload.status != ProcessStatus.PLUGINS_APPLIED and \
                payload.status != ProcessStatus.TRANSCRIBED:
            return
        conversation = payload.source.conversation
        for source_name, utterances in conversation.get_utterances().items():
            data = list()
            for utt in utterances:
                utt: Utt
                msg = "{}, {}, {}, {}".format(
                    utt.speaker_label,
                    utt.text,
                    utt.start_time_seconds,
                    utt.end_time_seconds)
                data.append(msg)
            data = "\n".join(data)
            # Save to file
            path = "{}/{}.{}".format(
                payload.source.hook.get_temp_directory_path(),
                source_name, self.RAW_EXTENSION)
            self.io.write(path, data, True)
