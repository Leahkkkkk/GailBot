from typing import Dict

class SettingProfile():
    """
    Store a single setting item 
    """
    def __init__(self) -> None:
        engine_setting : engineOption
        plugin_setting: pluginOption
        setting_path: str
        name: str

    def load_engine_setting(setting : Dict[str, str]) -> bool:
        raise NotImplementedError()

    def load_plugin_setting(setting : Dict[str, str]) -> bool:
        raise NotImplementedError()

    def update_setting(setting : Dict[str, str]) -> bool:
        raise NotImplementedError()

    def delete_setting() -> bool:
        raise NotImplementedError()

    def rename(name : str) -> None:
        raise NotImplementedError()

class EngineOption():
    """
    Provides an interface to validate setting based on setting schema 
    """
    def __init__(self) -> None:
        pass

    def is_valid(setting : Dict [str, str]) -> bool:
        raise NotImplementedError()

    def setting_schema(self) -> Dict [str, str]:
        raise NotImplementedError()

class PluginOption():
    """
    Provides an interface to validate plugin setting
    """
    def __init__(
        self,
        plugin : Plugin) -> None:
        pass

    def is_valid_plugin(plugin_name:str) -> bool:
        raise NotImplementedError()
