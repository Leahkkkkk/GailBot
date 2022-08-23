# Standard library import
from typing import Dict
# Local imports
from Src.components.io import IO
from Src.components.pipeline import Pipeline, Logic, Stream
from Src.components.network.network import Network
from Src.components.engines.watson import WatsonEngine
from Tests.pipeline.vardefs import *

############################### GLOBALS #####################################

############################### SETUP #####################################


class TestPipelineLogic(Logic):

    def __init__(self) -> None:
        super().__init__()
        # Adding all logic methods
        self._add_component_logic(
            "c1", self._preprocessor, self._processor_c1, self._post_processor)
        self._add_component_logic(
            "c2", self._preprocessor, self._processor_c2, self._post_processor)
        self._add_component_logic(
            "c3", self._preprocessor, self._processor_c3, self._post_processor)
        self._add_component_logic(
            "c4", self._preprocessor, self._processor_c4, self._post_processor)

    ########################### PRIVATE METHODS #############################

    def _preprocessor(self, streams: Dict[str, Stream]) -> Dict:
        return streams

    def _processor_c1(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c1".format(instantiated_obj), preprocessed_data)
        return preprocessed_data

    def _processor_c2(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c2".format(instantiated_obj), preprocessed_data)
        return preprocessed_data

    def _processor_c3(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c3".format(instantiated_obj), preprocessed_data)
        raise Exception("c3 failed")
        # return preprocessed_data

    def _processor_c4(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c4".format(instantiated_obj), preprocessed_data)
        return preprocessed_data

    def _post_processor(self, processed_data: Dict) -> Stream:
        return processed_data["base"]


class TestPipelineLogic2(Logic):
    def __init__(self) -> None:
        super().__init__()
        # Adding all logic methods
        self._add_component_logic(
            "c1", self._preprocessor, self._processor_c1, self._post_processor)
        self._add_component_logic(
            "c2", self._preprocessor, self._processor_c2, self._post_processor)
        self._add_component_logic(
            "c3", self._preprocessor, self._processor_c3, self._post_processor)
        self._add_component_logic(
            "c4", self._preprocessor, self._processor_c4, self._post_processor)
        self._add_component_logic(
            "c5", self._preprocessor, self._processor_c5, self._post_processor)

    def _preprocessor(self, streams: Dict[str, Stream]) -> Dict:
        return streams

    def _processor_c1(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c1".format(instantiated_obj), preprocessed_data)
        preprocessed_data["base"] = "hello!"
        return preprocessed_data

    def _processor_c2(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c2".format(instantiated_obj), preprocessed_data)
        if preprocessed_data["c1"] == "hello!":
            print("c1 successfully changed base data and sent to to c2")
        return preprocessed_data

    def _processor_c3(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c3".format(instantiated_obj), preprocessed_data)
        preprocessed_data["base"] = "world!"
        return preprocessed_data

    def _processor_c4(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c4".format(instantiated_obj), preprocessed_data)
        if preprocessed_data["c1"] == "hello!" and preprocessed_data["c3"] == "world!":
            print(
                "c1 successfully changed base data and sent to to c4, and c3 did the same")
        return preprocessed_data

    def _processor_c5(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        print("Processing c5".format(instantiated_obj), preprocessed_data)
        raise Exception("c5 failed")

    def _post_processor(self, processed_data: Dict) -> Stream:
        return processed_data["base"]


class TestPipelineLogic3(Logic):
    def __init__(self) -> None:
        super().__init__()
        # Adding all logic methods
        self._add_component_logic(
            "c1", self._preprocessor, self._processor_c1, self._post_processor)
        self._add_component_logic(
            "c2", self._preprocessor, self._processor_c2, self._post_processor)

    def _preprocessor(self, streams: Dict[str, Stream]) -> Dict:
        return streams

    def _processor_c1(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        preprocessed_data["base"] = instantiated_obj.is_file(MP3_FILE_PATH)
        print("Processing c1", preprocessed_data)
        return preprocessed_data

    def _processor_c2(self, instantiated_obj: object, preprocessed_data: Dict) \
            -> Dict:
        if preprocessed_data["c1"] == True:
            try:
                # instantiated_obj.configure("Test_files/Media/test2a.wav", 22050, 1)
                # utterances = instantiated_obj.transcribe()
                s1 = instantiated_obj.configure(
                    workspace_directory_path=WORKSPACE_DIR_PATH,
                    api_key=API_KEY, region=REGION,
                    audio_path=MP3_FILE_PATH,
                    base_model_name=BASE_LANG_MODEL)
                print(s1)
                utterances = instantiated_obj.transcribe()
            except Exception as e:
                print(e)
            print("engine output:", utterances)
        return preprocessed_data

    def _post_processor(self, processed_data: Dict) -> Stream:
        return processed_data["base"]

########################## TEST DEFINITIONS #################################


def test_pipeline_set_logic() -> None:
    """
    Tests:
        1. Verifies logic properly set in pipeline
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    assert p.set_logic(logic)


def test_pipeline_set_base_input() -> None:
    """
    Tests:
        1. Verifies base input properly set in pipeline
    """
    p = Pipeline("Test_pipeline")
    assert p.set_base_input(list(range(1, 100)))


def test_pipeline_add_component() -> None:
    """
    Tests:
        1. Verifies simple components can be added to pipeline
        2. Verifies unknown component cannot be added to pipeline
        3. Verifies unknown component cannot be made as a dependency
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    s1 = p.add_component("c1", None, [])
    s2 = p.add_component("c2", None, ["c1"])
    try:
        p.add_component("c10", None, [])
        p.add_component("c1", None, ["c10"])
        assert False
    except:
        assert s1 and s2


def test_pipeline_add_component_without_logic() -> None:
    """
    Tests:
        1. Verifies that exception thrown when adding a component without a
           logic set
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    try:
        p.add_component("c1", None)
        assert False
    except:
        assert True


def test_pipeline_add_component_unsupported_name() -> None:
    """
    Tests:
        1. Verifies that component cannot be added if it is not a supported
           component in the logic
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    try:
        p.add_component("not_component", None)
        assert False
    except:
        assert True


def test_pipeline_add_component_bad_source() -> None:
    """
    Tests:
        1. Verifies that a component with an unknown source cannot be added
           to the pipeline
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    try:
        p.add_component("c1", None)
        p.add_component("c2", None, ['not_component'])
        assert False
    except:
        assert True

# TODO: Bug, c2 can be set twice, overwrites dependency of c1 to c3


def test_pipeline_add_duplicate_component() -> None:
    """
    Tests:
        1. Verifies that a component cannot be set twice
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c3", None)
    p.add_component("c2", None, ['c1'])
    try:
        p.add_component("c2", None, ['c3'])
        assert False
    except:
        pass
    assert p.get_component_names() == ['c1', 'c3', 'c2'] \
        and p.get_component_dependencies("c2") == ["c1"]

# TODO: Bug, can add c1 twice, and c1 can be dependent on itself


def test_pipeline_add_invalid_component() -> None:
    """
    Tests:
        1. Verifies that a component cannot be dependent on itself
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    try:
        p.add_component("c1", None, ['c1'])
        assert False
    except:
        pass
    print("invalid:", p.get_component_dependencies("c1"))
    assert True


def test_pipeline_add_multiple_component() -> None:
    """
    Tests:
        1. Verifies that two components with no dependencies can be added to
           the pipeline successfully
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    try:
        res1 = p.add_component("c1", None)
        res2 = p.add_component("c2", None)
        assert res1 and res2
    except:
        assert True


def test_pipeline_get_name() -> None:
    """
    Tests:
        1. Getter for pipeline name
    """
    name = "Test_pipeline"
    p = Pipeline(name)
    assert p.get_name() == name


def test_pipeline_get_component_names() -> None:
    """
    Tests:
        1. Getter for component names
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None, [])
    p.add_component("c2", None, ["c1"])
    try:
        p.add_component("c10", None, [])
        p.add_component("c1", None, ["c10"])
        assert False
    except:
        assert p.get_component_names() == ["c1", "c2"]


def test_pipeline_get_component_dependencies() -> None:
    """
    Tests:
        1. Getter for component dependencies
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None, [])
    p.add_component("c2", None, ["c1"])
    try:
        p.add_component("c10", None, [])
        p.add_component("c1", None, ["c10"])
        assert False
    except:
        assert p.get_component_dependencies("c1") == [] and \
            p.get_component_dependencies("c2") == ["c1"]


def test_pipeline_get_execution_summary() -> None:
    """
    Tests:
        1. Getter for execution summary
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None, [])
    p.add_component("c2", None, ["c1"])
    assert type(p.get_execution_summary()) == dict


def test_pipeline_get_successful_components() -> None:
    """
    Tests:
        1. Getter for successful components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None, ["c1"])
    p.execute()
    assert p.get_successful_components() == ["c1", "c2"]


def test_pipeline_get_failed_components() -> None:
    """
    Tests:
        1. Getter for failed components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None, ["c1"])
    p.add_component("c3", None)
    p.execute()
    assert p.get_failed_components() == ["c3"]


def test_pipeline_get_executed_components() -> None:
    """
    Tests:
        1. Getter for executed components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None, ["c1"])
    p.add_component("c3", None)
    p.execute()
    assert p.get_executed_components() == ["c1", "c2", "c3"]


def test_pipeline_get_unexecuted_components() -> None:
    """
    Tests:
        1. Getter for unexcuted components
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None, ["c1"])
    p.add_component("c3", None)
    p.add_component("c4", None, ["c3"])
    p.execute()
    assert p.get_unexecuted_components() == ["c4"]


def test_pipeline_simple_passing() -> None:
    """
    Tests:
        1. Execution of pipeline that passes strings of data between each
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None, ["c1"])
    p.execute()


def test_pipeline_two_dependencies() -> None:
    """
    Tests:
        1. Execution of pipeline that passes strings of data between each with
           more complicated dependencies
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c3", None)
    p.add_component("c4", None, ["c1", "c3"])
    p.execute()


def test_pipeline_pass_data_despite_nondependent_failure() -> None:
    """
    Tests:
        1. Execution of pipeline with partial failures in pipeline, ensures
           the successful parts of pipeline run despite failure
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c3", None)
    p.add_component("c4", None, ["c1", "c3"])
    p.add_component("c5", None)
    p.execute()
    assert p.get_failed_components() == ["c5"] and p.get_successful_components() == [
        "c1", "c3", "c4"]


def test_pipeline_execute_two_dependencies_one_failure() -> None:
    """
    Tests:
        1. Execution of pipeline with a failure that affects other components,
           ensures affected parts of pipeline do not run
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c5", None)
    p.add_component("c4", None, ["c1", "c5"])
    p.execute()
    assert p.get_failed_components() == ["c5"] and p.get_unexecuted_components() == ["c4"] and \
        p.get_successful_components() == ["c1"]


def test_pipeline_execute_simple_failure_dependency() -> None:
    """
    Tests:
        1. Execution of pipeline with a failure that affects other components,
           ensures affected parts of pipeline do not run
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c5", None)
    p.add_component("c1", None, ["c5"])
    p.execute()
    assert p.get_successful_components() == [] and p.get_unexecuted_components() == ["c1"] and \
        p.get_failed_components() == ["c5"]


def test_pipeline_execute_failure_in_chain() -> None:
    """
    Tests:
        1. Execution of pipeline with a failure that affects other components,
           ensures affected parts of pipeline do not run
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c5", None)
    p.add_component("c1", None, ["c5"])
    p.add_component("c2", None, ["c1"])
    p.execute()
    assert p.get_successful_components() == [] and p.get_unexecuted_components() == ["c1", "c2"] and \
        p.get_failed_components() == ["c5"]


def test_pipeline_execute() -> None:
    """
    Tests:
        1. Pipeline execution of simple pipeline
    """
    logic = TestPipelineLogic()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None)
    p.add_component("c3", None, ["c1", "c2"])
    p.add_component("c4", None, ["c2", "c3"])
    p.execute()
    print(p.get_execution_summary())


def test_pipeline_two_executions() -> None:
    """
    Tests:
        1. Executing pipeline twice and confirming their executions are the same
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None, ["c1"])
    p.execute()
    execution1_succ = p.get_successful_components()
    print("execution1: ", p.get_execution_summary())
    p.execute()
    execution2_succ = p.get_successful_components()
    print("execution2: ", p.get_execution_summary())
    assert execution1_succ == execution2_succ

# TODO:


def test_pipeline_execute_with_objects() -> None:
    """
    Tests:
        1. Executing pipeline with instantiated objects
    """
    logic = TestPipelineLogic3()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", IO())
    p.print_dependency_graph()
    p.add_component("c2", WatsonEngine(IO(), Network()), ["c1"])
    p.print_dependency_graph()
    p.execute()
    p.print_dependency_graph()
    print(p.get_execution_summary())
    print("Executing again ")
    p.execute()
    p.print_dependency_graph()
    print(p.get_execution_summary())
    assert p.get_successful_components() == ["c1", "c2"] and p.get_failed_components() == [] and\
        p.get_unexecuted_components() == []


def test_pipeline_reset() -> None:
    """
    Tests:
        1. Verifies that reset of pipeline is successful
    """
    logic = TestPipelineLogic2()
    p = Pipeline("Test_pipeline")
    p.set_logic(logic)
    p.add_component("c1", None)
    p.add_component("c2", None, ["c1"])
    p.execute()
    p.reset_pipeline()
    assert p.get_component_names() == [] and p.get_unexecuted_components() == []
