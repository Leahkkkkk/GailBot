from pydantic import BaseModel, ValidationError
from typing import Dict, List 

class WatsonInterface(BaseModel):
    WATSON_API_KEY         : str
    WATSON_LANG_CUSTOM_ID  : str
    WATSON_REGION          : str
    WATSON_BASE_LANG_MODEL : str

def load_watson_setting(setting: Dict[str, str]):
    try:
        setting = WatsonInterface(**setting)
        return True
    except ValidationError as e:
        return False