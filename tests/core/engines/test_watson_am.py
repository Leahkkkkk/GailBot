from gailbot.core.engines.watson.am import WatsonAMInterface
from ...logger import makelogger

WATSON_API_KEY         = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID  = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION          = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"

logger = makelogger("watson_am")
def test_init_lm():
    model = WatsonAMInterface(WATSON_API_KEY, WATSON_REGION)
    assert model != None

def test_create_model():
    model = WatsonAMInterface(WATSON_API_KEY, WATSON_REGION)
    original = model.get_custom_models()
    model.create_custom_model("test", WATSON_BASE_LANG_MODEL, "for testing")
    logger.info(model.get_custom_models())
    new_model_id = model.get_custom_models()["test"]
    model.delete_custom_model(new_model_id)
    logger.info(model.get_custom_models())
    assert original == model.get_custom_models()