# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-04-29 14:07:03
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-29 15:31:00

from .vardefs import *
import pytest
import os
import shutil


@pytest.fixture(scope='session', autouse=True)
def reset_testing_output_directory() -> None:
    """
    Create all the directories required for output
    """
    assert TESTING_FRAMEWORK_ROOT != "."
    if TESTING_FRAMEWORK_ROOT != ".":
        if os.path.isdir(TESTING_FRAMEWORK_ROOT):
            shutil.rmtree(TESTING_FRAMEWORK_ROOT)
        os.makedirs(TESTING_FRAMEWORK_ROOT)
    # Roots
    os.makedirs(RESULTS_ROOT_DIR)
    os.makedirs(WORKSPACES_ROOT_DIR)
    # Component results
    os.makedirs(CONTROLLER_RESULTS)
    os.makedirs(ENGINES_RESULTS)
    os.makedirs(IO_RESULTS)
    os.makedirs(NETWORK_RESULTS)
    os.makedirs(ORGANIZER_SERVICE_RESULTS)
    os.makedirs(PIPELINE_RESULTS)
    os.makedirs(PIPELINE_SERVICE_RESULTS)
    os.makedirs(PLUGIN_MANAGER_RESULTS)
    os.makedirs(SHARED_MODELS_RESULT)
    os.makedirs(TRANSCRIPTION_RESULT)
    # Component workspaces
    os.makedirs(CONTROLLER_WORKSPACE)
    os.makedirs(ENGINES_WORKSPACE)
    os.makedirs(IO_WORKSPACE)
    os.makedirs(NETWORK_WORKSPACE)
    os.makedirs(ORGANIZER_SERVICE_WORKSPACE)
    os.makedirs(PIPELINE_WORKSPACE)
    os.makedirs(PIPELINE_SERVICE_WORKSPACE)
    os.makedirs(PLUGIN_MANAGER_WORKSPACE)
    os.makedirs(SHARED_MODELS_WORKSPACE)
    os.makedirs(TRANSCRIPTION_WORKSPACE)
