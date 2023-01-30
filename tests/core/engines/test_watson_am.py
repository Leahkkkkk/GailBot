from gailbot.core.engines.watson.am import WatsonAMInterface
WATSON_API_KEY         = "MSgOPTS9CvbADe49nEg4wm8_gxeRuf4FGUmlHS9QqAw3"
WATSON_LANG_CUSTOM_ID  = "41e54a38-2175-45f4-ac6a-1c11e42a2d54"
WATSON_REGION          = "dallas"
WATSON_BASE_LANG_MODEL = "en-US_NarrowbandModel"

def test_init_lm():
    lm_model = WatsonAMInterface(WATSON_API_KEY, WATSON_REGION)
    assert lm_model != None