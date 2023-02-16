class Organizer:
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_source(self, source_name: str, source_path: str) -> bool:
        raise NotImplementedError()
    
    def remove_source(self, source_name: str) -> bool:
        raise NotImplementedError() 
    
    def is_source(self, source_name: str) -> bool:
        raise NotImplementedError()
    
    def get_source(self, source_name: str) -> bool:
        raise NotImplementedError()
    
    def get_source_setting(self, source_name:str) :
        raise NotImplementedError()
    
    def is_setting_applied(self, source_name: str) -> bool:
        raise NotImplementedError()
    
    def apply_setting_to_source(self, source_name: str, setting_name:str) -> bool:
        raise NotImplementedError()
    
    def create_new_setting(self, setting_name: str, setting) -> bool: 
        raise NotImplementedError()
    
    def save_setting_profile(self, setting_name: str, output_dir: str) -> bool:
        raise NotImplementedError()
    
    def change_setting_name(self, setting_name: str, new_name: str) -> bool:
        raise NotImplementedError()
    
    def is_setting(self, setting_name: str) -> bool:
        raise NotImplementedError()
    
    def remove_setting_from_source(self, source_name: str) -> bool:
        raise NotImplementedError() 
    
    def get_setting(self, setting_name: str):
        raise NotImplementedError()