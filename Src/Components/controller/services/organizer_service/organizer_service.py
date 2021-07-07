# Standard library imports

from typing import List, Dict, Any, Tuple
# Local imports
from ....io import IO
from ....organizer import Organizer,Conversation
from .....utils.manager import ObjectManager
from ..status import TranscriptionStatus
from ..fs_service import FileSystemService, SettingsHook, SourceHook
from ..source import Source
from ..gb_settings import GailBotSettings, GBSettingAttrs
from .settings import SettingProfile
from .settings_details import SettingsDetails
from .source_details import SourceDetails
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
        ## Sources + profiles
        self.sources = ObjectManager()
        self.settings_profiles  = ObjectManager()
        ## Initializing
        self.configure_from_disk()

    ############################## MODIFIERS #################################

    def configure_from_disk(self) -> bool:
        """
        Configure the service from disk of the fs service is configured.
        """
        if not self.fs_service.is_workspace_configured():
            return False
        # Get a mapping of all the settings profiles loaded.
        settings_hooks = self.fs_service.get_all_settings_hooks()
        for name, hook in settings_hooks.items():
            self._initialize_settings_profile(name,hook.load(),hook)
        return True

    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str = "GailBot") -> bool:
        """
        Add a new source that can be either an audio or video file.
        """
        # Ensure that the source can be added.
        if self.is_source(source_name) and \
            (self.io.is_directory(source_path) or\
                 self.io.is_file(source_path)) and \
            (self.io.is_directory(result_dir_path) or \
                self.io.create_directory(result_dir_path)):
            return False
        # Create workspace for the source
        source_hook = self.fs_service.generate_source_hook(source_name)
        if source_hook == None:
            return False
        source_result_dir_path = self.fs_service.generate_source_result_directory(
            source_name, result_dir_path)
        # Create and save the source object
        source = Source(source_name, source_path, source_result_dir_path,
            source_hook, transcriber_name)
        return self.sources.add_object(source_name,source)

    def remove_source(self, source_name : str) -> bool:
        """
        Remove the given source if it exists.
        """
        if not self.is_source(source_name):
            return False
        source : Source = self.sources.get_object(source_name)
        source.hook.cleanup()
        return self.sources.remove_object(source_name)

    def remove_sources(self, source_names : List[str]) -> bool:
        return all([self.remove_source(name) for name in source_names])

    def clear_sources(self) -> bool:
        return all([self.remove_source(name) for\
             name in self.sources.get_object_names()])

    def reset_source(self, source_name : str) -> bool:
        """
        Reload the given source.
        """
        # Must be a source.
        if not self.is_source(source_name):
            return False
        source : Source = self.sources.get_object(source_name)
        # Remove source
        if not self.remove_source(source_name):
            return False
        # Re-add source
        if not self.add_source(
                source_name, source.source_path,source.result_dir_path,
                source.transcriber_name):
            return False
        if self.is_settings_profile(source.settings_profile_name):
            return self.apply_settings_profile_to_source(
                source_name, source.settings_profile_name)
        return True

    def reset_sources(self, source_names : List[str]) -> bool:
        """
        Reload the given sources.
        """
        return all([self.reset_source(source_name) \
            for source_name in source_names])

    def reset_all_sources(self) -> bool:
        """
        Reload all sources.
        """
        return self.reset_sources(self.sources.get_object_names())

    ### Settings profiles

    def create_new_settings_profile(
        self, new_settings_profile_name : str, data : Dict[GBSettingAttrs,Any]) \
                -> bool:
        """
        Create a new profile with the given data.
        """
        # Only work if configured and the profile does not exist.
        if self.is_settings_profile(new_settings_profile_name):
            return False
        # Attempt to create and save settings object.
        parsed_data = self._parse_settings_profile_data(data)
        return self._initialize_settings_profile(
                new_settings_profile_name,parsed_data)

    def save_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Save the given settings profile.
        """
        # Profile has to exist
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile : SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return settings_profile.hook.save(settings_profile.settings)

    def remove_settings_profile(self, settings_profile_name : str) -> bool:
        """
        Remove the given settings profile and any source using that profile.
        """
        # Profile has to exist
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile : SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings_profile.hook.cleanup()
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.remove_sources(source_names) and \
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
        if not self.is_settings_profile(settings_profile_name):
            return False
        # Obtaining current settings.
        settings_profile : SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings : GailBotSettings = settings_profile.settings
        data = settings.get_all_values()
        # Create a new settings with this data
        if not self._initialize_settings_profile(new_name,data):
            return False
        # Get all sources associated with old profile and change their profile.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        self.apply_settings_profile_to_sources(source_names,new_name)
        return self.remove_settings_profile(settings_profile_name)

    def apply_settings_profile_to_source(self, source_name : str,
            settings_profile_name : str) -> bool:
        """
        Apply the specified settings profile to the specified source.
        """
        # Source has to exist
        if not self.is_source(source_name) or \
                not self.is_settings_profile(settings_profile_name):
            return False
        # Change source data.
        source : Source = self.sources.get_object(source_name)
        source.settings_profile_name = settings_profile_name
        settings_profile : SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        # Simply apply new profile to conversation if configured.
        if source.is_configured:
            self.organizer.apply_settings_to_conversation(
                source.conversation,settings_profile.settings)
        # Otherwise, create new conversation.
        else:
            if not self._is_source_configurable(source_name):
                return False
            created, conversation = self.organizer.create_conversation(
                source.source_path,source.source_name,self.default_num_speakers,
                source.transcriber_name,source.result_dir_path,
                self.fs_service.get_temporary_workspace_path(),
                settings_profile.settings)
            if not created:
                return False
            conversation.set_transcription_status(TranscriptionStatus.ready)
            source.conversation = conversation
            source.is_configured = True
        return True

    def apply_settings_profile_to_sources(self, source_names : List[str],
            settings_profile_name : str) -> bool:
        return all([self.apply_settings_profile_to_source(
                source_name,settings_profile_name)] \
                    for source_name in source_names )

    ### Sources and settings profiles.

    def save_source_settings_profile(self, source_name : str,
            new_settings_profile_name : str)  -> bool:
        """
        Save the settings profile associated with the source with the given name.
        """
        if not self.is_source(source_name) or \
                self.is_settings_profile(new_settings_profile_name) or \
                not self.sources.get_object(source_name).is_configured:
            return False
        # Save to disk and load profile
        source : Source = self.sources.get_object(source_name)
        settings : GailBotSettings = source.conversation.get_settings()
        data = settings.get_all_values()
        # Create this as new settings and save
        self._initialize_settings_profile(new_settings_profile_name,data)
        if not self.save_settings_profile(new_settings_profile_name):
            self.settings_profiles.remove_object(new_settings_profile_name)
            return False
        # Apply this new settings to source.
        return self.apply_settings_profile_to_source(
            source_name, new_settings_profile_name)

    ############################## GETTERS ###################################

    def get_supported_audio_formats(self) -> List[str]:
        """
        Get the supported audio formats
        """
        return self.io.get_supported_audio_formats()

    def get_supported_video_formats(self) -> List[str]:
        """
        Get the supported video formats
        """
        return self.io.get_supported_video_formats()

    ### Sources

    def is_source(self, source_name : str) -> bool:
        """
        Determine whether the given source exists.
        """
        return self.sources.is_object(source_name)

    def is_source_configured(self, source_name : str) -> bool:
        """
        Determine if the source is configured.
        """
        return self.is_source(source_name) and \
            self.sources.get_object(source_name).is_configured

    def get_source_names(self) -> List[str]:
        """
        Obtain the names of all sources.
        """
        return self.sources.get_object_names()

    def get_configured_source_names(self) -> List[str]:
        """
        Get the names of all sources that have been configured.
        """
        return list(self.sources.get_filtered_objects(
            lambda name, obj: obj.is_configured).keys())

    def get_source_details(self, source_name : str) -> SourceDetails:
        """
        Get the details of the specified source.
        """
        if not self.is_source(source_name):
            return
        source : Source = self.sources.get_object(source_name)
        if self.is_source_configured(source_name):
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

    def get_sources_details(self, source_names : List[str]) \
            -> Dict[str,SourceDetails]:
        details = dict()
        for name in source_names:
            details[name] = self.get_source_details(name)
        return details

    def get_all_source_details(self) -> Dict[str,SourceDetails]:
        """
        Get the source details of all sources.
        """
        return self.get_sources_details(self.sources.get_object_names())

    def get_configured_sources(self) -> Dict[str,Source]:
        configured = dict()
        sources = self.sources.get_all_objects()
        for source_name, source in sources.items():
            source : Source
            if source.is_configured:
                configured[source_name] = source
        return configured

    ### Settings profiles

    def is_settings_profile(self, settings_profile_name : str) -> bool:
        return self.settings_profiles.is_object(settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name : str) -> bool:
        """
        Determine if the specified settings profile is saved on disk.
        """
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile : SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return settings_profile.hook.is_saved()

    def get_settings_profile_details(self, settings_profile_name : str) \
            -> SettingsDetails:
        """
        Get the details for the settings profile.
        """
        if not self.is_settings_profile(settings_profile_name):
            return
        settings_profile  : SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings : GailBotSettings = settings_profile.settings
        return SettingsDetails(
            settings_profile.profile_name,settings_profile.hook.is_saved(),
            self.get_source_names_using_settings_profile(
                settings_profile.profile_name),settings.get_all_values())

    def get_settings_profiles_details(self,
            settings_profile_names : List[str]) -> Dict[str,SettingsDetails]:
        """
        Get the details for the specified settings profiles.
        """
        details = dict()
        for name in settings_profile_names:
            details[name] = self.get_settings_profile_details(name)
        return details

    def get_all_settings_profiles_details(self) -> Dict[str,SettingsDetails]:
        """
        Get the details for all settings profiles.
        """
        return self.get_settings_profiles_details(
            self.settings_profiles.get_object_names())

    def get_source_settings_profile_name(self, source_name) -> str:
        if not self.is_source_configured(source_name):
            return
        source : Source = self.sources.get_object(source_name)
        return source.settings_profile_name

    def get_source_names_using_settings_profile(self,
            settings_profile_name : str) -> List[str]:
        """
        Obtain the name of all source using the given settings profile.
        """
        return list(self.sources.get_filtered_objects(
            lambda name, obj : obj.settings_profile_name \
                == settings_profile_name).keys())

    def get_sources_details_using_settings_profile(self,
            settings_profile_name : str) -> Dict[str,SourceDetails]:
        names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.get_sources_details(names)

    def get_source_settings_profile_details(self, source_name : str) \
            -> SettingsDetails:
        if not self.is_source_configured(source_name):
            return
        source : Source = self.sources.get_object(source_name)
        return self.get_settings_profile_details(source.settings_profile_name)

    def get_sources_settings_profile_details(self, source_names : List[str]) \
            -> Dict[str,SettingsDetails]:
        details = dict()
        for name in source_names:
            if self.is_source_configured(name):
                details[name] = self.get_settings_profile_details(
                    self.get_source_settings_profile_name(name))
        return details

    def get_all_sources_settings_profile_details(self) \
            -> Dict[str,SettingsDetails]:
        return self.get_sources_settings_profile_details(
            self.sources.get_object_names())

    ############################## SETTERS ###################################

    def set_settings_profile_attribute(self,settings_profile_name : str,
            attr : GBSettingAttrs, value : Any) -> bool:
        """
        Set the attribute of a given settings profile and for all the sources
        that are using this profile.
        """
        if not self.is_settings_profile(settings_profile_name):
            return False
        # Change the actual settings object first.
        settings_profile : SettingProfile = \
            self.settings_profiles.get_object(settings_profile_name)
        settings : GailBotSettings = settings_profile.settings
        if not settings.set_using_attribute(attr,value):
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
        if not self.is_source_configured(source_name):
            return False
        source : Source = self.sources.get_object(source_name)
        settings : GailBotSettings = source.conversation.get_settings()
        if not settings.set_using_attribute(attr,value):
            return False
        source.conversation = self.organizer.apply_settings_to_conversation(
            source.conversation,settings)
        return True

    ######################### PRIVATE METHODS ###############################

    def _parse_settings_profile_data(self, data : Dict[GBSettingAttrs,Any]) \
            -> Dict[str,Any]:
        """
        Convert from GBSettingAttrs dictionary to string dictionary.
        """
        parsed = dict()
        for k,v in data.items():
            parsed[k.value] = v
        return parsed

    def _is_source_configurable(self, source_name : str) -> bool:
        source : Source = self.sources.get_object(source_name)
        return (source_name != None and self.is_source(source_name)) and \
            (self.io.is_file(source.source_path) or\
                 self.io.is_directory(source.source_path)) and \
            (source.settings_profile_name != None and\
                 self.is_settings_profile(source.settings_profile_name )) and \
            (source.hook != None) and \
            (source.transcriber_name != None) and \
            (source.result_dir_path != None and \
                self.io.is_directory(source.result_dir_path))

    def _initialize_settings_profile(self, settings_profile_name : str,
            data : Dict[str,Any], hook : SettingsHook = None) -> bool:
        try:
            # Create hook if not given
            if hook == None:
                hook = self.fs_service.generate_settings_hook(
                    settings_profile_name)
            # Create settings profile
            created, settings = self.organizer.create_settings(
                    self.default_settings_type,data)
            if not created:
                return False
            profile = SettingProfile(
                settings_profile_name, settings,hook)
            self.settings_profiles.add_object(settings_profile_name,profile)
            return True
        except:
            return False




