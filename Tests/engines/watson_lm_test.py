
# Local imports
from Src.components.engines import WatsonLanguageModel
from Tests.engines.vardefs import *

############################### GLOBALS #####################################

########################## TEST DEFINITIONS ##################################


def test_watson_lm_get_base_model() -> None:
    """
    Tests:
        1. Get a valid base model.
        2. Get an invalid base model.
    """
    resp_keys = [
        "name", "language", "rate", "url", "supported_features", "description"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    resp = lm.get_base_model(BASE_LANG_MODEL)
    assert resp != None and \
        all([key in resp_keys for key in resp.keys()]) and \
        lm.get_base_model("invalid") == None


def test_watson_lm_get_base_models() -> None:
    """
    Tests:
        1. Make sure there is at least one base model.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    resp = lm.get_base_models()
    assert resp != None and len(resp) > 0


def test_watson_lm_get_custom_model() -> None:
    """
    Tests:
        1. Obtain a valid model and check return keys
        2. Ensure invalid key returns None.
    """
    resp_keys = [
        "customization_id", "created", "updated", "language", "dialect",
        "versions", "owner", "name", "description", "base_model_name", "status",
        "progress"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    resp = lm.get_custom_model(LANG_CUSTOM_ID)
    assert resp != None and \
        all([key in resp_keys for key in resp.keys()]) and \
        lm.get_custom_model("invalid") == None


def test_watson_lm_get_custom_models() -> None:
    """
    Tests:
        1. Ensure that all the ids for the custom model returned and valid ids.
    """
    resp_keys = [
        "customization_id", "created", "updated", "language", "dialect",
        "versions", "owner", "name", "description", "base_model_name", "status",
        "progress"]
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    models = lm.get_custom_models()
    assert models != None
    for custom_id in models.values():
        resp = lm.get_custom_model(custom_id)
        assert resp != None and all([key in resp_keys for key in resp.keys()])


def test_watson_lm_delete_custom_model() -> None:
    """
    Tests:
        1. Create a model and delete it.
        2. Delete a model that does not exist
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    s1 = lm.create_custom_model("test_1", BASE_LANG_MODEL, "test model 1")
    models = lm.get_custom_models()
    assert s1 and lm.delete_custom_model(models["test_1"]) and \
        not lm.delete_custom_model("invalid id")


def test_watson_lm_create_custom_model() -> None:
    """
    Tests:
        1. Create a new model with a valid base model.
        2. Create a model with an invalid base model.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    models = lm.get_custom_models()
    s1 = lm.create_custom_model("test_1", BASE_LANG_MODEL, "test model 1")
    s2 = lm.create_custom_model("test_2", "invalid base model", "test model 1")
    models = lm.get_custom_models()
    assert s1 and not s2 and \
        lm.delete_custom_model(models["test_1"])


def test_watson_lm_train_custom_model() -> None:
    """
    Tests:
        1. Create a model, add a resource and train it.
        2. Create a model and train it without adding a resource.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name, BASE_LANG_MODEL, "test model 1")
    models = lm.get_custom_models()
    s1 = lm.add_custom_words(models[model_name], ["pie"])
    s2 = lm.train_custom_model(models[model_name])
    s3 = lm.delete_custom_model(models[model_name])
    assert s1 and s2 and s3


def test_watson_lm_reset_custom_model() -> None:
    """
    Tests:
        1. Reset a model that has already been trained.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name, BASE_LANG_MODEL, "test model 1")
    models = lm.get_custom_models()
    assert lm.reset_custom_model(models[model_name]) and \
        lm.delete_custom_model(models[model_name])


def test_watson_lm_upgrade_custom_model() -> None:
    """
    Tests:
        1. Upgrade the base model of a custom model that has been created.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name, BASE_LANG_MODEL, "test model 1")
    models = lm.get_custom_models()
    assert lm.upgrade_custom_model(models[model_name]) and \
        lm.delete_custom_model(models[model_name])


def test_watson_lm_get_corpora() -> None:
    """
    Tests:
        1. Obtain the corpora of a model that has already been trained.
        2. Obtain the corpora of a model that has not been trained.
    """
    lm = WatsonLanguageModel()
    lm.connect_to_service(API_KEY, REGION)
    model_name = "test_1"
    lm.create_custom_model(model_name, BASE_LANG_MODEL, "test model 1")
    models = lm.get_custom_models()
    assert lm.get_corpora(LANG_CUSTOM_ID) != None and \
        lm.get_corpora(models[model_name]) != None and \
        lm.delete_custom_model(models[model_name])


def test_watson_lm_add_corpus() -> None:
    """
    Tests:
        1.
    """
    pass


def test_watson_lm_delete_corpus() -> None:
    pass


def test_watson_lm_get_corpus() -> None:
    pass


def test_watson_lm_get_custom_words() -> None:
    pass


def test_watson_lm_add_custom_words() -> None:
    pass


def test_watson_lm_delete_custom_word() -> None:
    pass


def test_watson_lm_get_custom_grammars() -> None:
    pass


def test_watson_lm_get_custom_grammar() -> None:
    pass


def test_watson_lm_add_custom_grammar() -> None:
    pass


def test_watson_lm_delete_custom_grammar() -> None:
    pass
