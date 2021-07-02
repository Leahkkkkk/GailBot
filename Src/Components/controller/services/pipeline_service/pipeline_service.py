# Standard library imports
from typing import List, Dict, Tuple
# Local imports
from ....pipeline import Pipeline
from ....organizer import Conversation
from ....plugin_manager import PluginManagerSummary
from .summary import PipelineServiceSummary
from .conversation_summary import ConversationSummary
from .transcription_stage import TranscriptionStage
from .analysis_stage import AnalysisStage
from .format_stage import FormatStage
from .payload import PipelineServicePayload
from .logic import PipelineServiceLogic
from .loader import PipelineServiceLoader

class PipelineService:

    def __init__(self) -> None:
        ## Vars.
        self.pipeline_name = "transcription_pipeline_service"
        self.pipeline_num_threads = 4
        ## Stage Objects
        self.transcription_stage = TranscriptionStage()
        self.analysis_stage = AnalysisStage()
        self.format_stage = FormatStage()
        ## Others
        self.payload = PipelineServicePayload()
        self.logic = PipelineServiceLogic()
        self.loader = PipelineServiceLoader()
        ## Initializing the pipeline
        self.pipeline = Pipeline(self.pipeline_name,self.pipeline_num_threads)
        self.pipeline.set_logic(self.logic)
        self.pipeline.add_component(
            "transcription_stage", self.transcription_stage)
        self.pipeline.add_component(
            "analysis_stage",self.analysis_stage,["transcription_stage"])
        self.pipeline.add_component(
            "format_stage",self.format_stage,["analysis_stage"])

    ################################# MODIFIERS #############################

    def register_analysis_plugins(self, config_path : str) -> List[str]:
        """
        Register analysis plugins using the configuration file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            (List[str]):
                Names of plugins that were loaded from the configuration file.
        """
        names = self.analysis_stage.get_plugin_names()
        parsed_data = self.loader.parse_analysis_plugin_configuration_file(
            config_path)
        for data in parsed_data:
            self.analysis_stage.register_plugin_from_data(data)
        return [name for name in self.analysis_stage.get_plugin_names() \
                if name not in names]

    def register_format(self, config_path : str) -> Tuple[str,List[str]]:
        """
        Register a format from the configuration file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            (Tuple[str,List[str]]):
                Name of the format + list of all plugins loaded.
        """
        format_name, parsed_data = self.loader.parse_format_configuration_file(
            config_path)
        return (format_name,
            self.format_stage.register_format(format_name, parsed_data))

    def start_service(self) -> PipelineServiceSummary:
        """
        Start the pipeline service.

        Returns:
            (PipelineServiceSummary)
        """
        # TODO: Do not hard-code format name
        self.payload.set_format("normal")
        self.pipeline.set_base_input(self.payload)
        self.pipeline.execute()
        return self._generate_pipeline_summary(
            self.payload,self.pipeline.get_execution_summary())

    ################################# GETTERS ###############################

    def get_analysis_plugin_names(self) -> List[str]:
        """
        Obtain a list of all analysis plugins.

        Returns:
            (List[str]): List of plugins to be used in the analysis.
        """
        return self.analysis_stage.get_plugin_names()

    def get_format_names(self) -> List[str]:
        """
        Obtain a list of all formats that are available.

        Returns:
            (List[str]): List of format names.
        """
        return self.format_stage.get_formats()

    def get_format_plugin_names(self, format_name : str) -> List[str]:
        """
        Obtain a list of all plugins that are available with the specified
        format.

        Args:
            format_name (str): Name of the format.

        Returns:
            (List[str]): List of plugins associated with format.
        """
        return self.format_stage.get_format_plugins(format_name)

    def add_conversations(self, conversations : Dict[str,Conversation]) -> bool:
        """
        Add conversations to the service.

        Args:
            conversations

        Returns:
            (bool): True if all conversations added. False otherwise.
        """
        # TODO: Change payload method to accept dictionary instead of list.
        return self.payload.add_conversations(list(conversations.values()))

    def is_conversation(self, conversation_name : str) -> bool:
        """
        Determine if the conversation has been added.

        Args:
            conversation_name (str)

        Returns:
            (bool): True if conversation exists, False otherwise.
        """
        return self.payload.is_conversation(conversation_name)

    def get_conversations(self) -> Dict[str,Conversation]:
        """
        Obtain all the conversations.

        Returns:
            (Dict[str,Conversation]):
                Mapping from conversation name to conversation.
        """
        return self.payload.get_conversations()

    ########################## PRIVATE METHODS ###############################

    # TODO: Standardize naming convention across stages.
    def _generate_pipeline_summary(self, payload : PipelineServicePayload,
            pipeline_summary : Dict) -> PipelineServiceSummary:
        # Generating the conversation summary for all conversations.
        # summaries = dict()
        # conversations = payload.get_conversations()
        # transcription_results = payload.get_transcription_stage_output()
        # analysis_results = payload.get_analysis_stage_output()
        # format_results = payload.get_format_stage_output()
        # for conversation_name, conversation in conversations.items():
        #     analysis_summary = analysis_results.analysis_summaries[conversation_name]
        #     format_summary = format_results.format_summaries[conversation_name]
        #     summaries[conversation_name] = ConversationSummary(
        #         conversation_name,
        #         analysis_summary.successful_plugins,
        #         format_summary.successful_plugins,
        #         payload.get_format(),
        #         conversation.get_transcription_status())
        # return PipelineServiceSummary(summaries)
        return PipelineServiceSummary({})





