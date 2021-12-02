# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-05 21:08:42
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 16:15:20
from typing import Dict, Any, List
from abc import abstractmethod

# Local imports
from ...io import IO
from ...plugin_manager import Plugin
from ...organizer import Conversation
from .models import ExternalMethods, Payload, Utt, ProcessStatus
from ...plugin_manager import PluginManager, PluginManagerSummary, ApplyConfig
from ..configurables.gb_settings import GBSettingAttrs, GailBotSettings
# from Src.components.controller.initializer import PipelineBlackBoard
from ..configurables.blackboards import PipelineBlackBoard


class OutputStage:

    def __init__(self, blackboard: PipelineBlackBoard,
                 external_methods: ExternalMethods) -> None:
        self.io = IO()
        self.blackboard = blackboard
        self.external_methods = external_methods

    ############################# MODIFIERS ##################################

    def output(self, payload: Payload) -> None:
        try:
            # Write the metadata
            self._write_metadata(payload)
            # Write the raw utterance files.
            self._write_raw_utterances(payload)
            # Save the hook to the result directory.
            payload.source.hook.save()
        except Exception as e:
            print(e)

    ########################## PRIVATE METHODS ###############################

    def _write_metadata(self, payload: Payload) -> None:
        # Generate metadata.
        data = self.external_methods.create_metadata(payload)
        path = "{}/{}_{}.{}".format(
            payload.source.hook.get_temp_directory_path(),
            payload.source.source_name,
            self.blackboard.METADATA_NAME,
            self.blackboard.METADATA_EXTENSION)
        self.io.write(path, data, True)

    def _write_raw_utterances(self, payload: Payload) -> None:
        # Has to be transcribed or plugins applied
        if payload.status != ProcessStatus.PLUGINS_APPLIED and \
                payload.status != ProcessStatus.TRANSCRIBED:
            return
        conversation = payload.source.conversation
        for source_name, utterances in conversation.get_utterances().items():
            data = list()
            for utt in utterances:
                msg = self.external_methods.stringify_utt(utt)
                data.append(msg)
            data = "\n".join(data)
            # Save to file
            path = "{}/{}.{}".format(
                payload.source.hook.get_temp_directory_path(),
                source_name, self.blackboard.RAW_EXTENSION)
            self.io.write(path, data, True)
