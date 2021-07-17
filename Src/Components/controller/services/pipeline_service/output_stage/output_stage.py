# Standard imports
# Local imports
from .....engines import Utterance, UtteranceAttributes
from ...organizer_service import GailBotSettings, RequestType
from ..pipeline_payload import SourcePayload

class OutputStage:
    """
    Generate output files for all payloads.
    """

    def __init__(self) -> None:
        pass

    def output(self, payload : SourcePayload) -> None:
        """
        Geerate the outputs for the specified payload.

        Args:
            payload (SourcePayload)
        """
        # Write all files.
        self._write_utterances(payload)
        # Generate metadata at the end.
        self._write_metadata(payload)
        payload.save_to_directory()

    ########################## PRIVATE METHODS ###############################

    def _write_metadata(self, payload : SourcePayload) -> None:
        """
        Write a metadata file for this specific payload.

        Args:
            payload (SourcePayload)
        """
        conversation = payload.get_conversation()
        # Generate metadata.
        metadata = {
            "conversation_name" : conversation.get_conversation_name(),
            "settings_profile_name" : payload.get_source().get_settings_profile_name(),
            "source_path" : conversation.get_source_path(),
            "conversation_source_type" : conversation.get_source_type(),
            "conversation_size" :conversation.get_conversation_size(),
            "transcription_date" : conversation.get_transcription_date(),
            # TODO: the status returned is not a string. Fix this.
            #"transcription_status" : conversation.get_transcription_status(),
            "transcription_time" : conversation.get_transcription_time(),
            "transcriber_name" : conversation.get_transcriber_name(),
            "number_of_speakers" : conversation.number_of_speakers(),
            "number_of_source_files" : conversation.number_of_source_files(),
            "source_file_names" : conversation.get_source_file_names(),
            "source_file_types" : conversation.get_source_file_types(),
            "result_directory_path" : conversation.get_result_directory_path(),
            "outputs" : payload.get_output_names(),
            "is_transcribed" : payload.is_transcribed(),
            "is_analyzed" : payload.is_analyzed(),
            "is_formatted"  : payload.is_formatted(),
            "analysis_plugins_applied" : list(payload.get_analysis_plugin_summaries().keys()),
            "format_plugins_applied" : list(payload.get_format_plugin_summaries().keys())}

        # Write to permanent files.
        extension = "json"
        identifier = "metadata"
        file_name = "{}.{}".format(identifier,extension)
        if payload.write_to_file(
                identifier,"permanent",identifier,extension,metadata):
            msg = "[{}] [Output stage] Metadata created as: {}".format(
                payload.get_source_name(),file_name)
        else:
            msg = "[{}] [Output stage] Unable to generate metadata".format(
                payload.get_source_name())
        payload.log(RequestType.FILE,msg)

    def _write_utterances(self, payload : SourcePayload) -> None:
        """
        Write utterances for all the source files in this payload.

        Args:
            payload (SourcePayload)
        """
        # Utterances are only written if the transcription was successful
        if not payload.is_transcribed():
            return
        conversation = payload.get_conversation()
        for source_name, utterances in conversation.get_utterances().items():
            data = list()
            for utt in utterances:
                msg = "{}: {} {}_{}".format(
                    utt.get(UtteranceAttributes.speaker_label)[1],
                    utt.get(UtteranceAttributes.transcript)[1],
                    utt.get(UtteranceAttributes.start_time)[1],
                    utt.get(UtteranceAttributes.end_time)[1])
                data.append(msg)
            data = "\n".join(data)
            # Save data to file
            extension = "txt"
            identifier = "{}_utterances".format(source_name)
            file_name = "{}.{}".format(identifier,extension)
            if  payload.write_to_file(
                    identifier, "permanent",identifier,extension,data):
                msg = "[{}] [Output stage] Source: {} --> output: {}".format(
                    payload.get_source_name(),source_name, file_name)
            else:
                msg = "[{}] [Output stage] Source: {} --> output failed".format(
                    payload.get_source_name(),source_name)
            payload.log(RequestType.FILE,msg)

