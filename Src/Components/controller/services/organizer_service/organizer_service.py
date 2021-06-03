# Standard library imports
from typing import List, Dict, Any
# Local imports
from ....io import IO
from ....organizer import Organizer,Conversation
from .....utils.manager import ObjectManager
from ..status import TranscriptionStatus
from ..fs_service import FileSystemService
from .source import Source
from .source_details import SourceDetails
from .setting_details import SettingDetails
from .settings import GailBotSettings, GBSettingAttrs
# Third party imports

class OrganizerService:


    def __init__(self, fs_service : FileSystemService) -> None:
        ## Variables
        self.default_num_speakers = 1
        self.default_settings_type = "GailBotSettings"
        self.default_settings_creator = lambda data : GailBotSettings(data)
        ## Objects
        self.fs_service = fs_service
        if not fs_service.is_configured():
            raise Exception("fs service not configured")
        self.io = IO()
        self.organizer = Organizer(IO())
        self.organizer.register_settings_type(
            self.default_settings_type, self.default_settings_creator)
        self.sources = ObjectManager()
        self.settings_profiles = ObjectManager()
        self.configure_from_disk()

    ############################## MODIFIERS #################################

    def configure_from_disk(self) -> bool:
        """
        Configure the service from disk of the fs service is configured.
        """
        if not self.fs_service.is_configured():
            return False
        self._initialize_profiles_from_disk()
        return True

    ### Sources

    # TODO: Add checks on adding invalid sources.
    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str = "GailBot") -> bool:
        """
        Add a new source.
        """
        # Ensure that the source can be added.
        if self.is_source(source_name) and \
            (self.io.is_directory(source_path) or\
                 self.io.is_file(source_path)) and \
            (self.io.is_directory(result_dir_path) or \
                self.io.create_directory(result_dir_path)):
            return False
        # Create workspace for the source
        self.fs_service.create_source_workspace_on_disk(source_name)
        ws_path = self.fs_service.get_source_workspace_location_on_disk(
            source_name)
        # Create the source object and add to list.
        source = Source(
            source_name, None,source_path,None,ws_path,transcriber_name,
            result_dir_path,False)
        return self.sources.add_object(source_name,source,False)

    def remove_source(self, source_name : str) -> bool:
        """
        Remove the given source if it exists.
        """
        # Only work if the service is configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Remove source from sources
        self.fs_service.cleanup_source_workspace_from_disk(source_name)
        return self.sources.remove_object(source_name)

    def remove_sources(self, source_names : List[str]) -> bool:
        return all([self.remove_source(name) for name in source_names])

    def clear_sources(self) -> bool:
        """
        Remove all sources.
        """
        return all([self.remove_source(name) for\
             name in self.sources.get_object_names()])


    ### Settings profiles

    def create_new_settings_profile(
        self, new_settings_profile_name : str, data : Dict[GBSettingAttrs,Any]) \
                -> bool:
        """
        Create a new profile with the given data.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Only work if configured and the profile does not exist.
        if self.is_settings_profile(new_settings_profile_name):
            return False
        # Attempt to create and save settings object.
        created, settings = self.organizer.create_settings(
            self.default_settings_type,self._parse_settings_profile_data(data))
        return False if not created else self.settings_profiles.add_object(
            new_settings_profile_name,settings)

    def save_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Save the given settings profile.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Profile has to exist
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings = self.settings_profiles.get_object(settings_profile_name,True)
        return self.fs_service.save_settings_profile_to_disk(
            settings_profile_name,settings)

    def remove_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Remove the given settings profile and any source using that profile.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Profile has to exist
        if not self.is_settings_profile(settings_profile_name):
            return False
        # Remove both from manager and disk, and all sources using profile.
        self.fs_service.remove_settings_profile_from_disk(
                settings_profile_name)
        names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.remove_sources(names) and \
            self.settings_profiles.remove_object(settings_profile_name)

    def remove_all_settings_profiles(self) -> bool:
        """
        Remove all settings profiles.
        """
        return all([self.remove_settings_profile(name) \
                for name in self.settings_profiles.get_object_names()])

    def change_settings_profile_name(self, settings_profile_name : str,
            new_name : str) -> bool:
        """
        Change the name of an existing settings profile, including in the
        sources using that settings profile.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings = self.settings_profiles.get_object(settings_profile_name,True)
        # Create the new settings object.
        self.settings_profiles.add_object(new_name,settings)
        # Save the new settings object to file if the previous one was saved.
        if self.fs_service.is_saved_settings_profile(settings_profile_name):
            self.fs_service.save_settings_profile_to_disk(new_name,settings)
        # Change settings of all objects using previous settings.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        for name in source_names:
            self.apply_settings_profile_to_source(name, new_name)
            source : Source = self.sources.get_object(name)
        return self.remove_settings_profile(settings_profile_name)

    ### Sources and settings profiles.

    def apply_settings_profile_to_source(self, source_name : str,
            settings_profile_name : str) -> bool:
        """
        Apply the specified settings profile to the specified source.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Source has to exist
        if not self.is_source(source_name) or \
                not self.is_settings_profile(settings_profile_name):
            return False
        source : Source = self.sources.get_object(source_name)
        source.settings_profile_name = settings_profile_name
        settings = self.settings_profiles.get_object(settings_profile_name)
        if source.is_configured:
            self.organizer.apply_settings_to_conversation(
                source.conversation,settings)
        else:
            # Create a conversation and apply settings if possible.
            source.settings_profile_name = settings_profile_name
            if not self._is_source_configurable(source_name):
                return False
            created, conversation = self.organizer.create_conversation(
                source.source_path,source.source_name,self.default_num_speakers,
                source.transcriber_name,source.result_dir_path,
                source.source_ws_path,settings)
            conversation.set_transcription_status(TranscriptionStatus.ready)
            if not created:
                return False
            source.conversation = conversation
            source.is_configured = True
        return True

    def save_source_settings_profile(self, source_name : str,
            new_settings_profile_name : str)  -> bool:
        """
        Save the settings profile associated with the source with the given name.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Source has to exist and be configured.
        if not self.is_source(source_name) or \
                self.is_settings_profile(new_settings_profile_name) or \
                not self.sources.get_object(source_name).is_configured:
            return False
        # Save to disk and load profile
        source : Source = self.sources.get_object(source_name)
        settings = source.conversation.get_settings()
        self.settings_profiles.add_object(
            new_settings_profile_name,settings)
        if not self.save_settings_profile(new_settings_profile_name):
            self.settings_profiles.remove_object(new_settings_profile_name)
            return False
        # Change source settings profile to this one
        return self.apply_settings_profile_to_source(
            source_name,new_settings_profile_name)

    ############################## GETTERS ###################################

    def is_configured(self) -> bool:
        """
        Determine if the service is configured.
        """
        return self.fs_service.is_configured()

    ### Sources

    def is_source(self, source_name : str) -> bool:
        """
        Determine whether the given source exists.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        return self.sources.is_object(source_name)

    def is_source_configured(self, source_name : str) -> bool:
        """
        Determine if the source is configured.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Source has to exist
        if not self.is_source(source_name):
            return False
        return self.sources.get_object(source_name).is_configured

    def get_source_names(self) -> List[str]:
        """
        Obtain the names of all sources.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        return self.sources.get_object_names()

    def get_configured_source_names(self) -> List[str]:
        """
        Get the names of all sources that have been configured.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        return list(self.sources.get_filtered_objects(
            lambda name, obj: obj.is_configured).keys())

    def get_source_details(self, source_name : str) -> SourceDetails:
        """
        Get the details of the specified source.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_source(source_name):
            return
        return self._create_source_details(source_name)

    def get_sources_details(self, source_names : List[str]) \
            -> Dict[str,SourceDetails]:
        """
        Get the source details of all the specified sources if they exist.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        mapping = dict()
        for source_name in source_names:
            if self.is_source(source_name):
                mapping[source_name] = self.get_source_details(source_name)
        return mapping

    def get_all_source_details(self) -> Dict[str,SourceDetails]:
        """
        Get the source details of all sources.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        return self.get_sources_details(self.sources.get_object_names())

    def get_configured_source_conversation(self, source_name : str) \
            -> Conversation:
        """
        Get the conversation associated with a source that is configured.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        # Source needs to exist and be configured
        if not self.is_source_configured(source_name):
            return
        return self.sources.get_object(source_name).conversation

    def get_configured_sources_conversations(self, source_names : List[str]) \
            -> Dict[str,Conversation]:
        """
        Get the conversations associated with the given sources if they are
        configured.
        """
        mapping = dict()
        for source_name in source_names:
            if self.is_source_configured(source_name):
                mapping[source_name] =\
                     self.get_configured_source_conversation(source_name)
        return mapping

    def get_all_configured_source_conversations(self) -> Dict[str,Conversation]:
        """
        Get the conversations associated with all configured sources.
        """
        return self.get_configured_sources_conversations(
            self.get_source_names())

    ### Settings profiles

    def is_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Determine if the given profile exists.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        return self.settings_profiles.is_object(settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name : str) -> bool:
        """
        Determine if the specified settings profile is saved on disk.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_settings_profile(settings_profile_name):
            return False
        return self.fs_service.is_saved_settings_profile(settings_profile_name)

    def get_settings_profile_details(self, settings_profile_name : str) \
            -> SettingDetails:
        """
        Get the details for the settings profile.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_settings_profile(settings_profile_name):
            return
        return self._create_settings_details(settings_profile_name)

    def get_settings_profiles_details(self,
            settings_profile_names : List[str]) -> Dict[str,SettingDetails]:
        """
        Get the details for the specified settings profiles.
        """
        mapping = dict()
        for profile_name in settings_profile_names:
            if self.is_settings_profile(profile_name):
                mapping[profile_name] = self.get_settings_profile_details(
                    profile_name)
        return mapping

    def get_all_settings_profiles_details(self) -> Dict[str,SettingDetails]:
        """
        Get the details for all settings profiles.
        """
        return self.get_settings_profiles_details(
            self.settings_profiles.get_object_names())

    ### Sources and settings profiles.

    def get_source_settings_profile_name(self, source_name) -> str:
        """
        Get the name of the settings profile associated with the given source.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_source_configured(source_name):
            return
        source : Source = self.sources.get_object(source_name)
        return source.settings_profile_name

    def get_source_names_using_settings_profile(self,
            settings_profile_name : str) -> List[str]:
        """
        Obtain the name of all source using the given settings profile.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        return list(self.sources.get_filtered_objects(
            lambda name, obj : obj.settings_profile_name \
                == settings_profile_name).keys())

    def get_sources_details_using_settings_profile(self,
            settings_profile_name : str) -> Dict[str,SourceDetails]:
        """
        Get details of the sources using the specified settings profile.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_settings_profile(settings_profile_name):
            return {}
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.get_sources_details(source_names)

    def get_source_settings_profile_details(self, source_name : str) \
            -> SettingDetails:
        """
        Get the Settings details of the settings associated with the given
        source.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_source_configured(source_name):
            return
        profile_name = self.get_source_settings_profile_name(source_name)
        return self.get_settings_profile_details(profile_name)

    def get_sources_settings_profile_details(self, source_names : List[str]) \
            -> Dict[str,SettingDetails]:
        """
        Get the settings details of the setting profiles associated with
        the given sources.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        mapping = dict()
        for source_name in source_names:
            if self.is_source_configured(source_name):
                mapping[source_name] = self.get_settings_profile_details(
                    self.get_source_settings_profile_name(source_name))
        return mapping

    def get_all_sources_settings_profile_details(self) \
            -> Dict[str,SettingDetails]:
        """
        Get the settings profile details associated with all sources.
        """
        return self.get_sources_settings_profile_details(
            self.sources.get_object_names())

    ############################## SETTERS ###################################

    ### Sources

    ### Settings profiles

    ### Sources and settings profiles.

    def set_settings_profile_attribute(self,settings_profile_name : str,
            attr : GBSettingAttrs, value : Any) -> bool:
        """
        Set the attribute of a given settings profile and for all the sources
        that are using this profile.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_settings_profile(settings_profile_name):
            return False
        # Change the actual settings object first.
        settings : GailBotSettings = \
            self.settings_profiles.get_object(settings_profile_name)
        if not settings.set(attr.value,value):
            return False
        # Change the same attribute for all sources that are using this
        # setting profile.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return all([self.set_source_settings_profile_attribute(
            source_name, attr,value) for source_name in source_names])

    def set_source_settings_profile_attribute(self, source_name : str,
            attr : GBSettingAttrs, value : Any) -> bool:
        """
        Set the attribute of a settings profile attached to a specific source.
        """
        # Has to be configured
        if not self.is_configured():
            raise Exception("Service not configured")
        if not self.is_source_configured(source_name):
            return False
        source : Source = self.sources.get_object(source_name)
        settings : GailBotSettings = source.conversation.get_settings()
        if not settings.set_using_attribute(attr,value):
            return False
        source.conversation = self.organizer.apply_settings_to_conversation(
            source.conversation,settings)
        return True

    ########################## PRIVATE METHODS ###############################

    ### Sources

    def _is_source_configurable(self, source_name : str) -> bool:
        source : Source = self.sources.get_object(source_name)

        return (source_name != None and self.is_source(source_name)) and \
            (self.io.is_file(source.source_path) or self.io.is_directory(source.source_path)) and \
            (source.settings_profile_name != None and\
                 self.is_settings_profile(source.settings_profile_name )) and \
            (source.source_ws_path != None \
                and self.io.is_directory(source.source_ws_path)) and \
            (source.transcriber_name != None) and \
            (source.result_dir_path != None and \
                self.io.is_directory(source.result_dir_path))

    ### Settings profiles

    def _initialize_profiles_from_disk(self) -> None:
        """
        Load all settings profiles from disk.
        """
        mapping = self.fs_service.load_all_settings_profiles_data_from_disk()
        for name, settings_profile in mapping.items():
            self.settings_profiles.add_object(name,settings_profile,True)

    def _parse_settings_profile_data(self, data : Dict[GBSettingAttrs,Any]) \
            -> Dict[str,Any]:
        """
        Convert from GBSettingAttrs dictionary to string dictionary.
        """
        parsed = dict()
        for k,v in data.items():
            parsed[k.value] = v
        return parsed

    ### Sources and settings profiles.

    ### SettingsDetails

    def _create_settings_details(self, settings_profile_name : str) \
            -> SettingDetails:
        attrs = [e.value for e in GBSettingAttrs]
        settings : GailBotSettings = self.settings_profiles.get_object(
            settings_profile_name,True)
        return SettingDetails(
            settings_profile_name,
            self.fs_service.is_saved_settings_profile(settings_profile_name),
            self.fs_service.get_saved_settings_profile_location_on_disk(
                settings_profile_name),
            self.get_source_names_using_settings_profile(settings_profile_name),
            self.default_settings_type,
            attrs,
            settings.get_all_values())

    ### SourceDetails

    def _create_source_details(self, source_name : str) -> SourceDetails:
        source : Source = self.sources.get_object(source_name)
        if source.is_configured:
            conversation : Conversation = source.conversation
            return SourceDetails(
                source_name,
                source.settings_profile_name,
                conversation.get_conversation_size(),
                conversation.get_source_type(),
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
        else:
            return SourceDetails(
                source_name, source.settings_profile_name, None,None,None,
                None,None, source.transcriber_name, None, None, None, None,
                source.result_dir_path, source.source_path)

