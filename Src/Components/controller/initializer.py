from typing import Tuple
from dataclasses import dataclass
from ..services import FileSystemService, OrganizerService
from .helpers.gb_settings import GailBotSettings, GBSettingAttrs
from .pipeline import GBPipeline


@dataclass
class Services:
    fs_service: FileSystemService = None
    organizer_service: OrganizerService = None
    pipeline: GBPipeline = None
    is_initialized: bool = False


class GBInitializer:

    DEFAULT_SETTINGS_TYPE = "gb"

    def __init__(self, ws_dir_path: str) -> None:
        fs_service = FileSystemService()
        organizer_service = OrganizerService(fs_service)
        pipeline = GBPipeline()
        configured = fs_service.configure_from_workspace_path(ws_dir_path)
        profile_added = organizer_service.add_settings_profile_type(
            self.DEFAULT_SETTINGS_TYPE, lambda data: GailBotSettings(data))
        if configured and profile_added:
            self.services = Services(
                fs_service, organizer_service, pipeline, True)
        else:
            self.services = Services()

    def initialize(self) -> Services:
        return self.services
