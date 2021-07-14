# Standard imports
# Local imports
from .....engines import Utterance, UtteranceAttributes
from ...organizer_service import GailBotSettings, RequestType
from ..pipeline_payload import SourcePayload

class OutputStage:

    def __init__(self) -> None:
        pass

    def output(self, payload : SourcePayload) -> None:
        # Write all files.
        self._write_utterances(payload)
        # Generate metadata at the end.
        self._write_metadata(payload)
        payload.save_to_directory()

    ########################## PRIVATE METHODS ###############################

    def _write_metadata(self, payload : SourcePayload) -> None:
        conversation = payload.get_conversation()
        # Generate metadata.
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
            "source_path" : conversation.get_source_path(),
            "outputs" : payload.get_output_names()}
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

