# Standard imports

# Local imports
from .services import ConfigService, OrganizerService,FileSystemService,\
    PipelineService, GBSettingAttrs, SystemBlackBoard
# Third party imports


class ControllerInitializer:
    """
    Separates various initialization logic from the controller.
    """

    def __init__(self) -> None:
        pass


    def initialize(self ,workspace_dir_path : str) -> None:
        ## Vars.
        self.pipeline_service_num_threads = 3
        ## Objects
        self.fs_service = FileSystemService()
        self.fs_service.configure_from_workspace_path(workspace_dir_path)
        if not self.fs_service.is_workspace_configured():
            raise Exception("Unable to configure workspace")
        self.config_service = ConfigService(self.fs_service)
        if not self.config_service.is_configured():
            raise Exception("unable to configure ConfigService")
        self.organizer_service = OrganizerService(self.fs_service)
        self.pipeline_service = PipelineService(
            self.pipeline_service_num_threads)
        # Running initialization methods
        self._add_default_settings_profile()

    ############################## GETTERS ##################################

    def get_fs_service(self) -> FileSystemService:
        return self.fs_service

    def get_organizer_service(self) -> OrganizerService:
        return self.organizer_service

    def get_pipeline_service(self) -> PipelineService:
        return self.pipeline_service

    ########################## PRIVATE METHODS ##############################

    def _add_default_settings_profile(self) -> None:
        """
        Add a default settings profile using the system blackboard.
        """
        system_bb = self.config_service.get_system_blackboard()
        # Add a default settings profile.
        try:
            data = {
                GBSettingAttrs.engine_type : system_bb.engine_type,
                GBSettingAttrs.watson_api_key : system_bb.watson_api_key,
                GBSettingAttrs.watson_language_customization_id : \
                    system_bb.watson_language_customization_id,
                GBSettingAttrs.watson_base_language_model : \
                    system_bb.watson_base_language_model,
                GBSettingAttrs.watson_region : system_bb.watson_region,
                GBSettingAttrs.analysis_plugins_to_apply : \
                    system_bb.analysis_plugins_to_apply,
                GBSettingAttrs.output_format : system_bb.output_format}
            self.organizer_service.create_new_settings_profile(
                "default",data)
        except:
            pass