from pydantic import BaseModel, ValidationError
from typing import Dict, List 

class WatsonInterface(BaseModel):
    engine: str = "watson"
    WATSON_API_KEY         : str
    WATSON_LANG_CUSTOM_ID  : str
    WATSON_REGION          : str
    WATSON_BASE_LANG_MODEL : str

def load_watson_setting(setting: Dict[str, str]):
    if not setting["engine"] == "watson": return False
    try:
        setting = WatsonInterface(**setting)
        return setting
    except ValidationError as e:
        return False