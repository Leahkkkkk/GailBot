from gailbot.core.engines.watson.lm import WatsonLMInterface
from gailbot.core.utils.logger import makelogger
import pytest
WATSON_API_KEY         = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID  = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION          = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"

logger = makelogger("watson_lm")
def test_init_lm():
    model = WatsonLMInterface(WATSON_API_KEY, WATSON_REGION)
    assert model != None
    assert model.get_base_model
    logger.info(model.get_base_model(WATSON_BASE_LANG_MODEL))
    logger.info(model.get_base_models())
    logger.info(model.get_custom_model(WATSON_LANG_CUSTOM_ID))
    logger.info(model.get_custom_models())
    
def test_create_model():
    model = WatsonLMInterface(WATSON_API_KEY, WATSON_REGION)
    original = model.get_custom_models()
    model.create_custom_model("test", WATSON_BASE_LANG_MODEL, "for testing")
    logger.info(model.get_custom_models())
    new_model_id = model.get_custom_models()["test"]
    model.delete_custom_model(new_model_id)
    logger.info(model.get_custom_models())
    assert original == model.get_custom_models()

def _failed_test_train_model():
    """ error:   No input data available for training """
    model = WatsonLMInterface(WATSON_API_KEY, WATSON_REGION)
    model.create_custom_model("test", WATSON_BASE_LANG_MODEL, "for testing")
    new_model_id = model.get_custom_models()["test"]
    assert model.train_custom_model(new_model_id)
    model.delete_custom_model(new_model_id)
    logger.info(model.get_custom_models())
    

