
# Standard imports
from typing import List, Dict, Any, Callable, Set
# Local imports
# from .source_loaders import SourceLoader, FileSourceLoader, \
#     DirectorySourceLoader, TranscribedSourceLoader
from .source_loaders import SourceLoader
from .details import SourceDetails, SettingsDetails
from .objects import Source, SettingsProfile
from .conversation_creator import CustomConversationCreator
from ...utils.manager import ObjectManager
from ...io import IO
from ...organizer import Organizer, Conversation, Settings, ConversationCreator
from ..fs_service import FileSystemService, SettingsHook, SourceHook


class OrganizerService:

    def __init__(self, fs_service: FileSystemService) -> None:
        # Vars
        # Objects
        self.fs_service = fs_service
        self.io = IO()
        self.organizer = Organizer(IO)
        self.organizer.register_creator("custom", CustomConversationCreator)
        self.source_loader = SourceLoader(fs_service)
        self.sources: ObjectManager = ObjectManager()
        self.settings_profiles: ObjectManager = ObjectManager()
        self.conversation_creator_method = None

    ############################## MODIFIERS #################################

    # --- Configuration methods

    def add_source_can_load_method(self, method: Callable) -> None:
        self.source_loader.add_source_checker(method)

    def set_conversation_creator_method(self, method: Callable[[str], Dict]) \
            -> None:
        self.conversation_creator_method = method

    def add_settings_profile_type(self, settings_type: str,
                                  setting_creator: Callable[[], Settings]) -> bool:
        return self.organizer.register_settings_type(
            settings_type, setting_creator)

    # ---- Others

    def add_source(self, source_name: str, source_path: str,
                   result_dir_path: str, transcriber_name: str) -> bool:
        if self.is_source(source_name):
            return False
        # Load using the source loader
        source = self.source_loader.load_source(
            source_name, source_path, result_dir_path, transcriber_name
        )
        return self.sources.add_object(source_name, source) \
            if source != None else False

    def remove_source(self, source_name: str) -> bool:
        if not self.is_source(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        source.hook.cleanup()
        return self.sources.remove_object(source_name)

    def remove_sources(self, source_names: List[str]) -> bool:
        return all([self.remove_source(name) for name in source_names])

    def clear_sources(self) -> bool:
        return all([self.remove_source(name) for
                    name in self.sources.get_object_names()])

    def reset_source(self, source_name: str) -> bool:
        if not self.is_source(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        # Remove source
        if not self.remove_source(source_name):
            return False
        # Re-add source
        return self.add_source(
            source_name, source.source_path,
            source.hook.get_result_directory_path(),
            source.transcriber_name)

    def reset_sources(self, source_names: List[str]) -> bool:
        return all([self.reset_source(source_name)
                    for source_name in source_names])

    def reset_all_sources(self) -> bool:
        return self.reset_sources(self.sources.get_object_names())

    # Settings profiles

    def create_new_settings_profile(
        self, settings_type: str,
            new_settings_profile_name: str, data: Dict[Settings, Any]) \
            -> bool:
        if self.is_settings_profile(new_settings_profile_name) or \
                not self.organizer.is_registered_settings_type(settings_type):
            return False
        # Instantiate settings with the data
        return self._initialize_settings_profile(
            settings_type, new_settings_profile_name, data)

    def save_settings_profile(self, settings_profile_name: str) -> bool:
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return settings_profile.hook.save(settings_profile.settings)

    def remove_settings_profile(self, settings_profile_name: str) -> bool:
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings_profile.hook.cleanup()
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.remove_sources(source_names) and \
            self.settings_profiles.remove_object(settings_profile_name)

    def remove_all_settings_profiles(self) -> bool:
        return all([self.remove_settings_profile(name)
                   for name in self.settings_profiles.get_object_names()])

    def change_settings_profile_name(self, settings_profile_name: str,
                                     new_name: str) -> bool:
        if settings_profile_name == new_name:
            return True
        if not self.is_settings_profile(settings_profile_name) or \
                self.is_settings_profile(new_name):
            return False
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        data = settings_profile.settings.get_all_values()
        # Create a new settings with this data
        if not self._initialize_settings_profile(
                settings_profile.settings_type,
                new_name, data):
            return False
        # Get all sources associated with old profile and change their profile.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        self.apply_settings_profile_to_sources(source_names, new_name)
        return self.remove_settings_profile(settings_profile_name)

    def apply_settings_profile_to_source(self, source_name: str,
                                         settings_profile_name: str) -> bool:
        if not self.is_source(source_name) or \
                not self.is_settings_profile(settings_profile_name):
            return False
        # Change source data.
        source: Source = self.sources.get_object(source_name)
        source.settings_profile_name = settings_profile_name
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        if source.configured:
            self.organizer.apply_settings_to_conversation(
                source.conversation, settings_profile.settings)
        else:
            if not self._is_source_configurable(source_name):
                return False
            created, conversation = self.organizer.create_conversation(
                "custom", [], {
                    "source_path": source.source_path,
                    "conversation_name": source.source_name,
                    "transcriber_name": source.transcriber_name,
                    "num_speakers": 1,  # TODO: Change this
                    "result_dir_path": source.hook.get_result_directory_path(),
                    "temp_dir_path": source.hook.get_temp_directory_path(),
                    "data_file_configs": self.conversation_creator_method(source.source_path)},
                settings_profile.settings)
            if not created:
                return False
            source.conversation = conversation
            source.configured = True
        return True

    def apply_settings_profile_to_sources(self, source_names: List[str],
                                          settings_profile_name: str) -> bool:
        return all([self.apply_settings_profile_to_source(
            source_name, settings_profile_name)
            for source_name in source_names])

    # Sources and settings profiles.

    def save_source_settings_profile(self, source_name: str,
                                     new_settings_profile_name: str) -> bool:
        if not self.is_source(source_name) or \
                self.is_settings_profile(new_settings_profile_name) or \
                not self.is_source_configured(source_name):
            return False
        # Save to disk and load profile
        source: Source = self.sources.get_object(source_name)
        settings: Settings = source.conversation.get_settings()
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            source.settings_profile_name)
        data = settings.get_all_values()
        if not self._initialize_settings_profile(
                settings_profile.settings_type,
                new_settings_profile_name, data):
            return False
        if not self.save_settings_profile(new_settings_profile_name):
            self.remove_settings_profile(new_settings_profile_name)
            return False
        return self.apply_settings_profile_to_source(
            source_name, new_settings_profile_name)

    ############################## GETTERS ###################################

    def get_supported_audio_formats(self) -> List[str]:
        pass

    def get_supported_video_formats(self) -> List[str]:
        pass

    # Sources

    def is_source(self, source_name: str) -> bool:
        return self.sources.is_object(source_name)

    def is_source_configured(self, source_name: str) -> bool:
        return self.is_source(source_name) and \
            self.sources.get_object(source_name).configured

    def get_source_names(self) -> List[str]:
        return self.sources.get_object_names()

    def get_configured_source_names(self) -> List[str]:
        return list(self.sources.get_filtered_objects(
            lambda name, obj: obj.configured).keys())

    def get_source_details(self, source_name: str) -> SourceDetails:
        pass

    def get_sources_details(self, source_names: List[str]) \
            -> Dict[str, SourceDetails]:
        pass

    def get_all_source_details(self) -> Dict[str, SourceDetails]:
        pass

    def get_configured_sources(self) -> Dict[str, Source]:
        configured = dict()
        sources = self.sources.get_all_objects()
        for source_name, source in sources.items():
            source: Source
            if source.configured:
                configured[source_name] = source
        return configured

    # Settings profiles

    def is_settings_profile(self, settings_profile_name: str) -> bool:
        return self.settings_profiles.is_object(settings_profile_name)

    def is_settings_profile_saved(self, settings_profile_name: str) -> bool:
        if not self.is_settings_profile(settings_profile_name):
            return False
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        return settings_profile.hook.is_saved()

    def get_settings_profile_details(self, settings_profile_name: str) \
            -> SettingsDetails:
        pass

    def get_settings_profiles_details(
            self, settings_profile_names: List[str]) -> Dict[str, SettingsDetails]:
        pass

    def get_all_settings_profiles_details(self) -> Dict[str, SettingsDetails]:
        pass

    def get_source_settings_profile_name(self, source_name: str) -> str:
        if not self.is_source_configured(source_name):
            return
        source: Source = self.sources.get_object(source_name)
        return source.settings_profile_name

    def get_source_names_using_settings_profile(
            self, settings_profile_name: str) -> List[str]:
        return list(self.sources.get_filtered_objects(
            lambda name, obj: obj.settings_profile_name
            == settings_profile_name).keys())

    def get_sources_details_using_settings_profile(
            self, settings_profile_name: str) -> Dict[str, SourceDetails]:
        names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return self.get_sources_details(names)

    def get_source_settings_profile_details(self, source_name: str) \
            -> SettingsDetails:
        if not self.is_source_configured(source_name):
            return
        source: Source = self.sources.get_object(source_name)
        return self.get_settings_profile_details(
            source.settings_profile_name)

    def get_sources_settings_profile_details(self, source_names: List[str]) \
            -> Dict[str, SettingsDetails]:
        details = dict()
        for name in source_names:
            if self.is_source_configured(name):
                details[name] = self.get_settings_profile_details(
                    self.get_source_settings_profile_name(name))
        return details

    def get_all_sources_settings_profile_details(self) \
            -> Dict[str, SettingsDetails]:
        return self.get_sources_settings_profile_details(
            self.sources.get_object_names())

    ############################## SETTERS ###################################

    def set_settings_profile_attribute(self, settings_profile_name: str,
                                       attr: Any, value: Any) -> bool:
        if not self.is_settings_profile(settings_profile_name):
            return False
        # Change the actual settings object first.
        settings_profile: SettingsProfile = self.settings_profiles.get_object(
            settings_profile_name)
        settings: Settings = settings_profile.settings
        if not settings.set_value(attr, value):
            return False
        # Change the same attribute for all sources that are using this
        # setting profile.
        source_names = self.get_source_names_using_settings_profile(
            settings_profile_name)
        return all([self.set_source_settings_profile_attribute(
            source_name, attr, value) for source_name in source_names])

    def set_source_settings_profile_attribute(self, source_name: str,
                                              attr: Any, value: Any) -> bool:
        if not self.is_source_configured(source_name):
            return False
        source: Source = self.sources.get_object(source_name)
        settings: Settings = source.conversation.get_settings()
        if not settings.set_value(attr, value):
            return False
        source.conversation = self.organizer.apply_settings_to_conversation(
            source.conversation, settings)
        return True

    ######################### PRIVATE METHODS ###############################

    def _is_source_configurable(self, source_name: str) -> bool:
        source: Source = self.sources.get_object(source_name)
        return (source_name != None and self.is_source(source_name)) and \
            (self.io.is_file(source.source_path) or
             self.io.is_directory(source.source_path)) and \
            (source.settings_profile_name != None and
             self.is_settings_profile(source.settings_profile_name)) and \
            (source.hook != None) and \
            (source.transcriber_name != None) and \
            (source.hook.get_result_directory_path() != None and
                self.io.is_directory(source.hook.get_result_directory_path()))

    def _initialize_settings_profile(
            self, settings_type, new_settings_profile_name: str,
            data: Dict[str, Any]) -> bool:
        created, settings = self.organizer.create_settings(
            settings_type, data)
        if not created:
            return False
        hook = self.fs_service.generate_settings_hook(
            new_settings_profile_name)
        profile = SettingsProfile(
            new_settings_profile_name, settings, hook, settings_type)
        return self.settings_profiles.add_object(
            new_settings_profile_name, profile)
