# Standard library imports
from Src.Components.organizer import settings
from typing import List, Dict
from copy import deepcopy
# Local imports
from ....io import IO
from ....organizer import Organizer,Conversation, Settings, Conversation
from ..status import TranscriptionStatus
from ..fs_service import FileSystemService
from .source import Source
from .source_details import SourceDetails
from .setting_details import SettingDetails
from .settings import GailBotSettings, GBSettingAttrs
from .manager import ObjectManager
from .decorators import OrganizerDecorators

# Third party imports

class OrganizerService:

    def __init__(self, fs_service : FileSystemService) -> None:
        ## Variables
        self.default_num_speakers = 1
        self.default_settings_type = "GailBotSettings"
        self.default_settings_creator = lambda data : GailBotSettings(data)
        ## Objects
        self.fs_service = fs_service
        self.io = IO()
        self.organizer = Organizer(IO())
        self.organizer.register_settings_type(
            self.default_settings_type, self.default_settings_creator)
        self.sources = ObjectManager()
        self.settings_profiles = ObjectManager()
        ## Initialize settings profiles
        profiles = self.fs_service.load_all_settings_profiles_data_from_disk()
        for name,profile in profiles.items():
            self.settings_profiles.add_object(name,profile)


    ############################## MODIFIERS #################################

    ### Source

    @OrganizerDecorators.check_configured
    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str,
            settings_profile_name : str = "default") -> bool:
        if not self._can_add_source(
                source_name, source_path,result_dir_path,settings_profile_name):
            return False

        settings = self.settings_profiles.get_object(settings_profile_name,True)
        ws_location = self.fs_service.get_source_workspace_location_on_disk(
            source_name)
        is_created, conversation = self.organizer.create_conversation(
            source_path,source_name,self.default_num_speakers,
            transcriber_name,result_dir_path,ws_location,settings)
        conversation.set_transcription_status(TranscriptionStatus.ready)

        source = self._create_source(source_name, conversation,
                        settings_profile_name)
        if not is_created:
            self._cleanup_source(source_name)
            return False
        return True


    @OrganizerDecorators.check_configured
    def remove_source(self, source_name : str) -> bool:
        return self.sources.remove_object(source_name)


    @OrganizerDecorators.check_configured
    def clear_sources(self) -> bool:
        return self.sources.clear_objects()


    ### Settings profiles.

    @OrganizerDecorators.check_configured
    def apply_settings_profile_to_source(self, source_name : str,
            settings_profile_name : str) -> bool:
        if not self.sources.is_object(source_name) or \
                not self.settings_profiles.is_object(settings_profile_name):
            return False

        settings = self.settings_profiles.get(settings_profile_name,True)
        source = self.settings_profiles.get(source_name)
        source.settings_profile_name = settings_profile_name
        source.conversation = self.organizer.apply_settings_to_conversation(
            source.conversation,settings)
        return True

    @OrganizerDecorators.check_configured
    def save_custom_settings_profile(self, settings_profile_name : str) -> bool:
        if not self.settings_profiles.is_object(settings_profile_name):
            return False
        settings = self.settings_profiles.get(settings_profile_name,True)
        return self.fs_service.save_settings_profile_to_disk(
                settings_profile_name,settings)

    @OrganizerDecorators.check_configured
    def delete_custom_settings_profile(self, settings_profile_name : str) -> bool:
        if not self.settings_profiles.is_object(settings_profile_name):
            return False
        return self.settings_profiles.remove_object(settings_profile_name) and \
            self.fs_service.remove_settings_profile_from_disk(
                settings_profile_name)

    @OrganizerDecorators.check_configured
    def save_source_settings_profile(self, source_name : str,
           new_settings_profile_name : str) -> bool:
        if not self.sources.is_object(source_name) or \
                self.settings_profiles.is_object(new_settings_profile_name) or \
                self.fs_service.is_saved_settings_profile(
                    new_settings_profile_name):
            return False
        source = self.sources.get_object(source_name)
        conversation = source.conversation
        settings : GailBotSettings = conversation.get_settings()
        return self.settings_profiles.add_object(
                new_settings_profile_name,settings) and \
            self.save_custom_settings_profile(new_settings_profile_name) and \
            self.apply_settings_profile_to_source(
                source_name, new_settings_profile_name)

    ############################## GETTERS ###################################

    def is_configured(self) -> bool:
        return self.fs_service.is_configured()

    ## Source

    @OrganizerDecorators.check_configured
    def is_source(self, source_name : str) -> bool:
        return self.sources.is_object(source_name)

    @OrganizerDecorators.check_configured
    def get_source_names(self) -> List[str]:
        return self.sources.get_object_names()

    @OrganizerDecorators.check_configured
    def get_source_paths(self) -> Dict[str,str]:
        paths = dict()
        source_names = self.get_source_names()
        for source_name in source_names:
            paths[source_name] = self.sources.get_object(
                source_name).conversation.get_source_type()
        return paths

    @OrganizerDecorators.check_configured
    def get_source_conversation(self, source_name : str) -> Conversation:
        if not self.sources.is_object(source_name):
            return
        return self.sources.get_object(source_name).conversation

    @OrganizerDecorators.check_configured
    def get_filtered_source_conversations(self, source_names : List[str]) \
            -> Dict[str,Conversation]:
        return self.sources.get_filtered_objects(
            lambda name, obj : name in source_names)

    @OrganizerDecorators.check_configured
    def get_all_source_conversations(self) -> Dict[str,Conversation]:
        return self.sources.get_all_objects()

    @OrganizerDecorators.check_configured
    def get_source_details(self, source_name : str) -> SourceDetails:
        return self._initialize_source_details(source_name)

    @OrganizerDecorators.check_configured
    def get_filtered_source_details(self, source_names : List[str])\
            -> Dict[str,SourceDetails]:
        details = dict()
        for name in source_names:
            details[name] = self.get_source_details(name)
        return details

    @OrganizerDecorators.check_configured
    def get_all_source_details(self) -> Dict[str,SourceDetails]:
        return self.get_filtered_source_details(self.sources.get_object_names())

    ### Settings profiles

    @OrganizerDecorators.check_configured
    def is_settings_profile(self, settings_profile_name : str) -> bool:
        return self.settings_profiles.is_object(settings_profile_name)

    @OrganizerDecorators.check_configured
    def get_source_settings_profile(self, source_name : str) -> Settings:
        if not self.sources.is_object(source_name):
             return
        return self.sources.get_object(source_name).conversation.get_settings()

    @OrganizerDecorators.check_configured
    def get_source_settings_profile_name(self, source_name : str) -> str:
        if not self.sources.is_object(source_name):
             return
        return self.sources.get_object(source_name).settings_profile_name

    @OrganizerDecorators.check_configured
    def get_settings_profile_names(self) -> List[str]:
        return self.settings_profiles.get_object_names()

    @OrganizerDecorators.check_configured
    def get_source_settings_profile_details(self, source_name : str) \
            -> SettingDetails:
        if not self.sources.is_object(source_name):
             return
        settings_profile_name = self.get_source_settings_profile_name(
            source_name)
        return self.get_source_settings_profile_details(settings_profile_name)

    @OrganizerDecorators.check_configured
    def get_settings_profile_details(self, settings_profile_name : str) \
            -> SettingDetails:
        if not self.settings_profiles.is_object(settings_profile_name):
            return
        if not self.is_configured() or \
                not self.is_settings_profile(settings_profile_name):
            return
        return self._initialize_settings_details(
            settings_profile_name,
            self.fs_service.is_saved_settings_profile(settings_profile_name),
            self.fs_service.get_saved_settings_profile_location_on_disk(
                settings_profile_name),
             self.get_source_names_using_settings_profile(
            settings_profile_name))

    @OrganizerDecorators.check_configured
    def get_source_names_using_settings_profile(self,
            settings_profile_name : str) -> List[str]:
        return list(self.sources.get_filtered_objects(
            lambda name , obj : obj.settings_profile_name \
                == settings_profile_name).keys())

    @OrganizerDecorators.check_configured
    def get_all_settings_profiles_details(self) -> Dict[str,SettingDetails]:
        details = dict()
        names = self.settings_profiles.get_object_names()
        for name in names:
            details[name] = self.get_settings_profile_details(name)
        return details

    ########################### PRIVATE METHODS ##############################

    def _can_add_source(self, source_name : str, source_path : str,
            result_dir_path : str, settings_profile_name : str) -> bool:
        return not self.is_source(source_name) and \
            (self.io.is_directory(source_path) or\
                 self.io.is_file(source_path)) and \
            (self.io.is_directory(result_dir_path) or \
                self.io.create_directory(result_dir_path)) and \
            self.is_settings_profile(settings_profile_name)

    ### Source

    def _create_source(self,source_name : str, conversation : Conversation,
            settings_profile_name : str) -> Source:
        source = Source(conversation,source_name,settings_profile_name)
        self.sources.add_object(source_name,source,False)
        self.fs_service.create_source_workspace_on_disk(source_name)

    def _cleanup_source(self, source_name : str) -> None:
        self.sources.remove_object(source_name)
        self.fs_service.cleanup_source_workspace_from_disk(source_name)

    ### SettingsDetails

    def _initialize_settings_details(self, settings_profile_name : str,
            is_saved : bool, save_location : str, used_by_sources : List[str])\
                 -> SettingDetails:
        attrs = [e.value for e in GBSettingAttrs]
        settings : GailBotSettings = self.settings_profiles.get_object(
            settings_profile_name,True)
        return SettingDetails(
            settings_profile_name,is_saved,save_location,used_by_sources,
            self.default_settings_type,attrs,settings.get_all_values())

    ### SourceDetails

    def _initialize_source_details(self, source_name : str ) -> SourceDetails:
        source = self.sources.get_object(source_name)
        conversation : Conversation = source.conversation
        return SourceDetails(
            source_name,source.settings_profile_name,
            conversation.get_conversation_size(), conversation.get_source_type(),
            conversation.get_transcription_date(),
            conversation.get_transcription_status(),
            conversation.get_transcription_time(),
            conversation.get_transcriber_name(),
            conversation.number_of_source_files(),
            conversation.number_of_speakers(),
            conversation.get_source_file_names(),
            conversation.get_source_file_types(),
            conversation.get_result_directory_path(),
            conversation.get_source_path())

