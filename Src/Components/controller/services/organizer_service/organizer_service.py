# Standard library imports
from typing import List, Dict
# Local imports
from ....io import IO
from ....organizer import Organizer,Conversation, Settings, Conversation
from .source import Source
from .source_details import SourceDetails
from .setting_details import SettingDetails
from .settings import GailBotSettings
from ..status import TranscriptionStatus
# Third party imports

# TODO: Make sure each method only works if configured!!!!
class OrganizerService:

    def __init__(self) -> None:
        # Variables.
        self.workspace_dir_path = None
        self.conversation_workspace_dir_path = None
        # TODO: Change IO to be able to read custom extensions (gailbot) by specifying reader
        self.settings_file_extension = "json"
        self.default_settings_type = "GailBotSettings"
        self.default_settings_name = "default"
        self.default_settings_creator = lambda data : GailBotSettings(data)
        self.is_default_setting_loaded = False
        self.sources = dict() # source_name (str) to source (Source)
        self.settings = dict() # settings_name (str) to settings (Settings)
        self.io = IO()
        self.organizer = Organizer(IO())
        self.organizer.register_settings_type(
            self.default_settings_type, self.default_settings_creator)

    ################################## MODIFIERS #############################

    # TODO: Work on organizer buildConversation to ensure invalid source is checked.
    def add_source(self, source_name : str, source_path : str,
            result_dir_path : str, transcriber_name : str,
            settings_name : str = "default") -> bool:
        # Check if the source can be added
        if not self._can_add_source() or \
                self.is_source(source_name) or \
                not self.is_setting(settings_name):
            return False
        # Check if the conversation information is valid
        if not (self.io.is_directory(source_path) or \
                    self.io.is_file(source_path)) or \
                not (self.io.is_directory(result_dir_path) or
                    self.io.create_directory(result_dir_path)):
            return False
        # Create settings
        settings = self.settings[settings_name]
        # Create conversation
        # TODO: Change hard-coding of the number of speakers
        is_created, conversation = self.organizer.create_conversation(
            source_path,source_name,1,transcriber_name,result_dir_path,
            self.conversation_workspace_dir_path,settings)
        conversation.set_transcription_status(TranscriptionStatus.ready)
        if not is_created:
            return False
        self.sources[source_name] = Source(conversation)
        return True

    def remove_source(self, source_name : str) -> bool:
        if self.is_source(source_name):
            del self.sources[source_name]
            return True
        return False

    def clear_sources(self) -> bool:
        self.sources.clear()
        return True

    def save_source_settings(self, source_name : str, setting_name : str) \
            -> bool:
        if not self.is_source(source_name):
            return False
        # Cannot resave a loaded setting.
        if self.is_setting(setting_name):
            return False
        save_path = "{}/{}.{}".format(
            self.workspace_dir_path,setting_name,self.settings_file_extension)
        # Cannot save if already saved
        if self.io.is_file(save_path):
            return False
        # Save the settings to the given file
        # Get the settings of the specified source.
        settings = self.get_source_settings(source_name)
        settings.save_to_file(lambda data : self.io.write(save_path,data,True))
        return self.load_setting_from_path(setting_name,save_path)

    def delete_setting(self, setting_name : str) -> bool:
        if not self.is_setting(setting_name):
            return False
        save_path = "{}/{}.{}".format(
            self.workspace_dir_path,setting_name,self.settings_file_extension)
        if not self.io.is_file(save_path):
            return False
        if not self.io.delete(save_path):
            return False
        del self.settings[setting_name]
        return True

    ################################## GETTERS #############################

    def is_fully_configured(self) -> bool:
        return self._can_add_source()

    def is_setting(self, setting_name : str) -> bool:
        return setting_name in self.settings

    def is_source(self, source_name : str) -> bool:
        return source_name in self.sources

    def get_source_names(self) -> List[str]:
        return list(self.sources.keys())

    def get_source_paths(self) -> Dict[str,str]:
        paths = dict()
        for name, source in self.sources.items():
            conversation : Conversation = source.conversation
            paths[name] = conversation.get_source_path()
        return paths

    def get_source_settings(self, source_name : str) -> Settings:
        if not self.is_source(source_name):
            return
        source = self.sources[source_name]
        conversation : Conversation = source.conversation
        return conversation.get_settings()

    def get_source_settings_name(self, source_name : str) -> str:
        if not self.is_source(source_name):
            return
        source : Source = self.sources[source_name]
        return source.settings_name

    def get_available_setting_details(self) -> List[SettingDetails]:
        pass

    def get_available_setting_names(self) -> List[str]:
        return list(self.settings.keys())

    def get_source_details(self, source_name : str) -> SourceDetails:
        pass

    def get_all_sources_conversations(self) -> List[Conversation]:
        conversations = list()
        for source in self.sources.values():
            conversations.append(source.conversation)
        return conversations

    def get_source_conversation(self, source_name : str) -> Conversation:
        if not self.is_source(source_name):
            return
        source = self.sources[source_name]
        return source.conversation

    ################################## SETTERS #############################

    def set_workspace_path(self, path : str) -> bool:
        if not self.io.is_directory(path):
            return False
        self.settings.clear()
        # Load all settings from the workspace path
        if not self._load_all_settings_from_path(path):
            return False
        if not self.is_setting(self.default_settings_name):
            self.settings.clear()
            return False
        self.is_default_setting_loaded = True
        self.workspace_dir_path = path
        return True

    # TODO: Change to make sure directory is created if it does not exist.
    def set_conversation_workspace_path(self, path : str) -> bool:
        if not self.io.is_directory(path):
            return False
        self.conversation_workspace_dir_path = path
        return True

    # TODO: Eventually change to have multiple types of settings
    def load_setting_from_path(self, setting_name : str, path : str) -> bool:
        # Cannot reload settings
        if self.is_setting(setting_name):
            return False
        if not self.io.is_file(path) or \
                self.io.get_file_extension(path)[1] !=\
                     self.settings_file_extension:
            return False
        data = self.io.read(path)[1]
        created, settings = self.organizer.create_settings(
            self.default_settings_type,data)
        if not created or not settings.is_configured():
            return False
        self.settings[setting_name] = settings
        return True

    ################################ PRIVATE METHODS ########################

    def _load_all_settings_from_path(self, path : str) -> bool:
        if not self.io.is_directory(path):
            return False
        settings_paths = self.io.path_of_files_in_directory(
            path,[self.settings_file_extension],False)[1]
        for setting_path in settings_paths:
            self.load_setting_from_path(
                self.io.get_name(setting_path),setting_path)
        return True

    def _can_add_source(self) -> bool:
        return self.workspace_dir_path != None and \
            self.io.is_directory(self.workspace_dir_path) and \
            self._can_create_conversation() and \
            self.is_default_setting_loaded

    def _can_create_conversation(self) -> bool:
        return self.conversation_workspace_dir_path != None and \
            self.io.is_directory(self.conversation_workspace_dir_path)


