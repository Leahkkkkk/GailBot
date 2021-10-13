# Standard library imports

from typing import List, Dict, Any, Tuple
# Local imports
from ....io import IO
from ....organizer import Organizer, Conversation
from .....utils.manager import ObjectManager
from ..status import TranscriptionStatus
from ..fs_service import FileSystemService, SettingsHook, SourceHook
from .settings_details import SettingsDetails
from .source_details import SourceDetails
from .source import Source, RequestType
from .settings_profile import GBSettingAttrs, GailBotSettings, SettingProfile
from .source_loader import SourceLoader
from .source_loaders import FileSourceLoader, DirectorySourceLoader, \
    TranscribedSourceLoader

# Third party imports


class OrganizerService:
    """
    Service to Organize sources.
    """

    def __init__(self, fs_service: FileSystemService) -> None:
        """
        Args:
            fs_service (FileSystemService): Must be configured.s
        """
        # Variables
        self.default_num_speakers = 1
        self.default_settings_type = "GailBotSettings"
        self.default_settings_creator = lambda data: GailBotSettings(data)
        # Objects
        self.fs_service = fs_service
        self.io = IO()
        self.organizer = Organizer(IO())
        self.organizer.register_settings_type(
            self.default_settings_type, self.default_settings_creator)
        # Sources + profiles
        self.source_loaders: List[SourceLoader] = \
            [TranscribedSourceLoader(self.fs_service, self.organizer),  # This has to run first
             FileSourceLoader(self.fs_service, self.organizer),
             DirectorySourceLoader(self.fs_service, self.organizer)]
        self.sources = ObjectManager()
        self.settings_profiles = ObjectManager()
        # Initializing
        self.configure_from_disk()

    ############################## MODIFIERS #################################

    def configure_from_disk(self) -> bool:
        """
        Configure the service from disk of the fs service is configured.

        Returns:
            (bool): True if configured successfully, False otherwise.
        """
        if not self.fs_service.is_workspace_configured():
            return False
        # Get a mapping of all the settings profiles loaded.
        settings_hooks = self.fs_service.get_all_settings_hooks()
        for name, hook in settings_hooks.items():
            self._initialize_settings_profile(name, hook.load(), hook)
        return True

    def add_source(self, source_name: str, source_path: str,
                   result_dir_path: str, transcriber_name: str = "GailBot") -> bool:
        # Cannot re-add source.
        if self.is_source(source_name):
            return False
        # Cycle through all the available SourceLoaders and use the appropriate
        # one.
        for source_loader in self.source_loaders:
            source = source_loader.load_source(
                source_name, source_path, result_dir_path, transcriber_name)
            if source != None:
                # Add to sources objects
                if self.sources.add_object(source_name, source):
                    # Log that the source is created
                    msg = "[{}] Source created".format(source_name)
                    source.log(msg)
                    return True
                else:
                    return False
        return False

    def remove_source(self, source_name: str) -> bool:
        """
        Remove the given source if it exists.

        Args:
            source_name (str)

        Returns:
            (bool)" True if removed successfully, False otherwise.
        """
        if not self.is_source(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        source.get_hook().cleanup()
        msg = "[{}] Source removed".format(source_name)
        source.log(msg)
        return self.sources.remove_object(source_name) and \
            self.fs_service.remove_source_hook(source_name)

    def remove_sources(self, source_names: List[str]) -> bool:
        """
        Remove all sources with the specified names.

        Args:
            source_names (List[str])

        Returns:
            (bool): True if all sources removed, False otherwise.
        """
        return all([self.remove_source(name) for name in source_names])

    def clear_sources(self) -> bool:
        """
        Remove all sources.

        Returns:
            (bool): True if all sources removed, False otherwise,
        """
        return all([self.remove_source(name) for
                    name in self.sources.get_object_names()])

    def reset_source(self, source_name: str) -> bool:
        """
        Reload the given source if it exists.

        Args:
            source_name (str)

        Returns:
            (bool): True if successfully reloaded, False otherwise.
        """
        # Must be a source.
        if not self.is_source(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        # Remove source
        if not self.remove_source(source_name):
            return False
        # Re-add source
        if not self.add_source(
                source_name, source.get_source_path(),
                source.get_result_directory_path(),
                source.get_transcriber_name()):
            return False
        # TODO: Determine if the settings profie should be re-applied.
        # if self.is_settings_profile(source.get_settings_profile_name()):
        #     return self.apply_settings_profile_to_source(
        #         source_name, source.get_settings_profile_name())
        return True

    def reset_sources(self, source_names: List[str]) -> bool:
        """
        Reload the given sources.

        Args:
            source_names (List[str])

        Returns:
            (bool): True if specified sources reloaded, False otherwise.
        """
        return all([self.reset_source(source_name)
                    for source_name in source_names])

    def reset_all_sources(self) -> bool:
        """
        Reload all sources.

        Returns:
            (bool): True if all sources reloaded.
        """
        return self.reset_sources(self.sources.get_object_names())

    # Settings profiles

    def create_new_settings_profile(
            self, new_settings_profile_name: str, data: Dict[GBSettingAttrs, Any]) \
            -> bool:
        """
        Create a new profile with the given data.

        Args:
            new_settings_profile_name (str): Name of the new profile.
            data (Dict[GBSettingAttrs,Any]):
                Must have all key-value pairs for settings.

        Returns:
            (bool): True if new profile created, False otherwise.
        """
        # Only work if configured and the profile does not exist.
        if self.is_settings_profile(new_settings_profile_name):
            return False
        # Attempt to create and save settings object.
        parsed_data = self._parse_settings_profile_data(data)
        return self._initialize_settings_profile(
            new_settings_profile_name, parsed_data)

    def save_settings_profile(self, settings_profile_name: str) -> bool:
        """
        Save the given settings profile to disk.

        Args:
            settings_profile_name (str): Name of the profile.

        Returns:
            (bool): True if saved, False otherwise.
        """
        # Profile has to exist
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile: SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return settings_profile.save()

    def remove_settings_profile(self, settings_profile_name: str) -> bool:
        """
        Remove the given settings profile and any source using that profile.
        Deletes the profile from disk if it is saved.

        Args:
            settings_profile_name (str)

        Returns:
            (bool): True if deleted, False otherwise.
        """
        # Profile has to exist
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile: SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings_profile.get_hook().cleanup()
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.remove_sources(source_names) and \
            self.settings_profiles.remove_object(settings_profile_name)

    def remove_all_settings_profiles(self) -> bool:
        """
        Remove all settings profiles.

        Returns:
            (bool): True if all removed, False otherwise.
        """
        return all([self.remove_settings_profile(name)
                    for name in self.settings_profiles.get_object_names()])

    def change_settings_profile_name(self, settings_profile_name: str,
                                     new_name: str) -> bool:
        """
        Change the name of an existing settings profile, including in the
        sources using that settings profile.

        Args:
            settings_profile_name (str): Name of existing settings profiles.
            new_name (str): New name for the settings profile.

        Returns:
            (bool): True if changed, False otherwise.
        """
        if settings_profile_name == new_name:
            return True
        if not self.is_settings_profile(settings_profile_name):
            return False
        # Cannot change the name to an existing profile name.
        if self.is_settings_profile(new_name):
            return False
        # Obtaining current settings.
        settings_profile: SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings: GailBotSettings = settings_profile.get_settings()
        data = settings.get_all_values()
        # Create a new settings with this data
        if not self._initialize_settings_profile(new_name, data):
            return False
        # Get all sources associated with old profile and change their profile.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        self.apply_settings_profile_to_sources(source_names, new_name)
        return self.remove_settings_profile(settings_profile_name)

    def apply_settings_profile_to_source(self, source_name: str,
                                         settings_profile_name: str) -> bool:
        """
        Apply the specified settings profile to the specified source if they
        exist.

        Args:
            source_name (str)
            settings_profile_name (str)

        Returns:
            (bool): True if profile applied to source, False otherwise.
        """
        # Source has to exist
        if not self.is_source(source_name) or \
                not self.is_settings_profile(settings_profile_name):
            return False
        # Change source data.
        source: Source = self.sources.get_object(source_name)
        source.set_settings_profile_name(settings_profile_name)
        settings_profile: SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        # Simply apply new profile to conversation if configured.
        if source.is_configured():
            self.organizer.apply_settings_to_conversation(
                source.get_conversation(), settings_profile.get_settings())
        # Otherwise, create new conversation.
        else:
            if not self._is_source_configurable(source_name):
                return False
            created, conversation = self.organizer.create_conversation(
                source.get_source_path(), source.get_source_name(), self.default_num_speakers,
                source.get_transcriber_name(), source.get_result_directory_path(),
                source.get_hook().get_workspace_path(),
                settings_profile.get_settings())
            if not created:
                return False
            conversation.set_transcription_status(TranscriptionStatus.ready)
            source.set_conversation(conversation)
            source.set_configured()
        # Logging
        msg = "[{}] Settings profile applied: {}".format(
            settings_profile_name, source_name)
        source.log(msg)
        return True

    def apply_settings_profile_to_sources(self, source_names: List[str],
                                          settings_profile_name: str) -> bool:
        """
        Apply the specified settings profile to the specified sources if they
        exist.

        Args:
            source_names (List[str])
            settings_profile_name (str)

        Returns:
            (bool): True if profile applied to source, False otherwise.
        """
        return all([self.apply_settings_profile_to_source(
            source_name, settings_profile_name)
            for source_name in source_names])

    # Sources and settings profiles.

    def save_source_settings_profile(self, source_name: str,
                                     new_settings_profile_name: str) -> bool:
        """
        Save the settings profile associated with the source with the given name.

        Args:
            source_name (str)
            new_settings_profile_name (str)

        Returns:
            (bool): True if the profile is saved, False otherwise.
        """
        if not self.is_source(source_name) or \
                self.is_settings_profile(new_settings_profile_name) or \
                not self.sources.get_object(source_name).is_configured():
            return False
        # Save to disk and load profile
        source: Source = self.sources.get_object(source_name)
        settings: GailBotSettings = source.get_conversation().get_settings()
        data = settings.get_all_values()
        # Create this as new settings and save
        self._initialize_settings_profile(new_settings_profile_name, data)
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

        Returns:
            (List[str])
        """
        return self.io.get_supported_audio_formats()

    def get_supported_video_formats(self) -> List[str]:
        """
        Get the supported video formats

        Returns:
            (List[str])
        """
        return self.io.get_supported_video_formats()

    # Sources

    def is_source(self, source_name: str) -> bool:
        """
        Determine whether the given source exists.

        Args:
            source_name (str)

        Returns:
            (bool): True if source exists, False otherwise.
        """
        return self.sources.is_object(source_name)

    def is_source_configured(self, source_name: str) -> bool:
        """
        Determine if the source is configured.

        Args:
            source_name (str)

        Returns:
            (bool): True if source configured, False otherwise.
        """
        return self.is_source(source_name) and \
            self.sources.get_object(source_name).is_configured()

    def get_source_names(self) -> List[str]:
        """
        Obtain the names of all sources.

        Returns:
            (List[str])
        """
        return self.sources.get_object_names()

    def get_configured_source_names(self) -> List[str]:
        """
        Get the names of all sources that have been configured.

        Returns:
            (List[str])
        """
        return list(self.sources.get_filtered_objects(
            lambda name, obj: obj.is_configured()).keys())

    def get_source_details(self, source_name: str) -> SourceDetails:
        """
        Get the details of the specified source.

        Args:
            source_name (str)

        Returns:
            (SourceDetails)
        """
        if not self.is_source(source_name):
            return
        source: Source = self.sources.get_object(source_name)
        if self.is_source_configured(source_name):
            conversation: Conversation = source.get_conversation()
            return SourceDetails(
                source_name,
                source.get_settings_profile_name(),
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
                source_name, source.get_settings_profile_name(), None, None, None,
                None, None, source.get_transcriber_name(), None, None, None, None,
                source.get_result_directory_path(), source.get_source_path())

    def get_sources_details(self, source_names: List[str]) \
            -> Dict[str, SourceDetails]:
        """
        Get details for all the specified sources if they exist.

        Args:
            source_names (List[str])

        Returns:
            (Dict[str,SourceDetails]):
                Map from source name to its details.
        """
        details = dict()
        for name in source_names:
            if self.is_source(name):
                details[name] = self.get_source_details(name)
        return details

    def get_all_source_details(self) -> Dict[str, SourceDetails]:
        """
        Get the source details of all sources.

        Returns:
            (Dict[str,SourceDetails]):
                Map from source name to its details.
        """
        return self.get_sources_details(self.sources.get_object_names())

    def get_configured_sources(self) -> Dict[str, Source]:
        """
        Obtain all sources that have been configured.

        Returns:
            (Dict[str,Source]):
                Mapping from source name to Source.
        """
        configured = dict()
        sources = self.sources.get_all_objects()
        for source_name, source in sources.items():
            source: Source
            if source.is_configured():
                configured[source_name] = source
        return configured

    # Settings profiles

    def is_settings_profile(self, settings_profile_name: str) -> bool:
        """
        Determine if the settings profile exists.

        Args:
            settings_profile_name (str)

        Returns:
            (bool)" True if the profile exists, False otherwise.
        """
        return self.settings_profiles.is_object(settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name: str) -> bool:
        """
        Determine if the specified settings profile is saved on disk.

        Args:
            settings_profile_name (str)

        Returns:
            (bool): True if the profile is saved on disk, False otherwise.
        """
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile: SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return settings_profile.get_hook().is_saved()

    def get_settings_profile_details(self, settings_profile_name: str) \
            -> SettingsDetails:
        """
        Get the details for the settings profile.

        Args:
            settings_profile_name (str)

        Returns:
            (SettingsDetails)
        """
        if not self.is_settings_profile(settings_profile_name):
            return
        settings_profile: SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings: GailBotSettings = settings_profile.get_settings()
        return SettingsDetails(
            settings_profile.get_profile_name(), settings_profile.get_hook().is_saved(),
            self.get_source_names_using_settings_profile(
                settings_profile.get_profile_name()), settings.get_all_values())

    def get_settings_profiles_details(self,
                                      settings_profile_names: List[str]) -> Dict[str, SettingsDetails]:
        """
        Get the details for the specified settings profiles.

        Args:
            settings_profile_names (List[str])

        Returns:
            (Dict[str,SettingsDetails]):
                Map from profile name to its details.
        """
        details = dict()
        for name in settings_profile_names:
            if self.is_settings_profile(name):
                details[name] = self.get_settings_profile_details(name)
        return details

    def get_all_settings_profiles_details(self) -> Dict[str, SettingsDetails]:
        """
        Get the details for all settings profiles.

        Returns:
            (Dict[str,SettingsDetails]):
                Map from profile name to its details.
        """
        return self.get_settings_profiles_details(
            self.settings_profiles.get_object_names())

    def get_source_settings_profile_name(self, source_name: str) -> str:
        """
        Obtain the name of the settings profile associated with the source.

        Args:
            source_name (str)

        Returns:
            (str): Name of the settings profile associated with the source.
        """
        if not self.is_source_configured(source_name):
            return
        source: Source = self.sources.get_object(source_name)
        return source.get_settings_profile_name()

    def get_source_names_using_settings_profile(self,
                                                settings_profile_name: str) -> List[str]:
        """
        Obtain the name of all source using the given settings profile.

        Args:
            settings_profile_name (str)

        Returns:
            (List[str]): Names of sources.
        """
        return list(self.sources.get_filtered_objects(
            lambda name, obj: obj.settings_profile_name
            == settings_profile_name).keys())

    def get_sources_details_using_settings_profile(self,
                                                   settings_profile_name: str) -> Dict[str, SourceDetails]:
        """
        Obtain the details of sources using the specified settings profile.

        Args:
            settings_profile_name (str)

        Returns:
            (Dict[str,SourceDetails]): Map from source name  to SourceDetails.
        """
        names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.get_sources_details(names)

    def get_source_settings_profile_details(self, source_name: str) \
            -> SettingsDetails:
        """
        Obtain the SettingsDetails of the source.

        Args:
            source_name (str)

        Returns:
            (SettingsDetails)
        """
        if not self.is_source_configured(source_name):
            return
        source: Source = self.sources.get_object(source_name)
        return self.get_settings_profile_details(
            source.get_settings_profile_name())

    def get_sources_settings_profile_details(self, source_names: List[str]) \
            -> Dict[str, SettingsDetails]:
        """
        Obtain the SettingsDetails of the sources

        Args:
            source_names (List[str])

        Returns:
            (Dict[str,SettingsDetails]):
                Map from source name to SettingsDetails.
        """
        details = dict()
        for name in source_names:
            if self.is_source_configured(name):
                details[name] = self.get_settings_profile_details(
                    self.get_source_settings_profile_name(name))
        return details

    def get_all_sources_settings_profile_details(self) \
            -> Dict[str, SettingsDetails]:
        """
        Obtain the SettingsDetails of all sources

        Returns:
            (Dict[str,SettingsDetails]):
                Map from source name to SettingsDetails.
        """
        return self.get_sources_settings_profile_details(
            self.sources.get_object_names())

    ############################## SETTERS ###################################

    def set_settings_profile_attribute(self, settings_profile_name: str,
                                       attr: GBSettingAttrs, value: Any) -> bool:
        """
        Set the attribute of a given settings profile and for all the sources
        that are using this profile.

        Args:
            settings_profile_name (str)
            attr (GBSettingAttrs)
            value (Any)

        Returns:
            (bool): True if successful, False otherwise.
        """
        if not self.is_settings_profile(settings_profile_name):
            return False
        # Change the actual settings object first.
        settings_profile: SettingProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings: GailBotSettings = settings_profile.get_settings()
        if not settings.set_using_attribute(attr, value):
            return False
        # Change the same attribute for all sources that are using this
        # setting profile.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return all([self.set_source_settings_profile_attribute(
            source_name, attr, value) for source_name in source_names])

    def set_source_settings_profile_attribute(self, source_name: str,
                                              attr: GBSettingAttrs, value: Any) -> bool:
        """
        Set the attribute of a settings profile attached to a specific source.

        Args:
            source_name (str)
            attr (GBSettingAttrs)
            value (Any)

        Returns:
            (bool): True if successful, False otherwise.
        """
        if not self.is_source_configured(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        settings: GailBotSettings = source.get_conversation().get_settings()
        if not settings.set_using_attribute(attr, value):
            return False
        source.set_conversation(
            self.organizer.apply_settings_to_conversation(
                source.get_conversation(), settings))
        return True

    ######################### PRIVATE METHODS ###############################

    def _parse_settings_profile_data(self, data: Dict[GBSettingAttrs, Any]) \
            -> Dict[str, Any]:
        """
        Convert from GBSettingAttrs dictionary to string dictionary.
        """
        parsed = dict()
        for k, v in data.items():
            parsed[k.value] = v
        return parsed

    def _is_source_configurable(self, source_name: str) -> bool:
        source: Source = self.sources.get_object(source_name)
        return (source_name != None and self.is_source(source_name)) and \
            (self.io.is_file(source.get_source_path()) or
             self.io.is_directory(source.get_source_path())) and \
            (source.get_settings_profile_name() != None and
             self.is_settings_profile(source.get_settings_profile_name())) and \
            (source.get_hook() != None) and \
            (source.get_transcriber_name() != None) and \
            (source.get_result_directory_path() != None and
                self.io.is_directory(source.get_result_directory_path()))

    def _initialize_settings_profile(self, settings_profile_name: str,
                                     data: Dict[str, Any], hook: SettingsHook = None) -> bool:
        try:
            # Create hook if not given
            if hook == None:
                hook = self.fs_service.generate_settings_hook(
                    settings_profile_name)
            # Create settings profile
            created, settings = self.organizer.create_settings(
                self.default_settings_type, data)
            if not created:
                return False
            profile = SettingProfile(
                settings_profile_name, settings, hook)
            self.settings_profiles.add_object(settings_profile_name, profile)
            return True
        except:
            return False
