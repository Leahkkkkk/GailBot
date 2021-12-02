# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:48:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-02 16:28:52
from typing import Dict, Any, List
from abc import abstractmethod

# Local imports
from ..io import IO
from ..plugin_manager import Plugin
from .payload import Payload
from ..shared_models import Utt


class OutputStage:

    def __init__(self) -> None:
        self.io = IO()

    ############################# MODIFIERS ##################################

    def output(self, payload: Payload) -> None:
        try:
            print("in output ")
            # Write the metadata
            self._write_metadata(payload)
            # Write the raw utterance files.
            # self._write_raw_utterances(payload)
            # Save the hook to the result directory.
            # payload.source.hook.save()
            print("output done")
        except Exception as e:
            print(e)

    ########################## PRIVATE METHODS ###############################

    def _write_metadata(self, payload: Payload) -> None:
        path = "{}/{}_{}.{}".format(
            payload.source.hook.get_temp_directory_path(),
            payload.source.identifier,
            "metadata",
            "json")
        print(path)
        data = {
            payload.source.identifier
        }
        self.io.write(path, data, True)

    def _write_raw_utterances(self, payload: Payload) -> None:
        for source_name, utterances in payload.utterances_map:
            data = list()
            for utt in utterances:
                utt: Utt
                msg = [utt.speaker_label, utt.text,
                       utt.start_time_seconds, utt.end_time_seconds]
                msg = msg.jon(",")
                data.append(msg)
            data = "\n".join(data)
            # Save to file
            path = "{}/{}.{}".format(
                payload.source.hook.get_temp_directory_path(),
                source_name, self.blackboard.RAW_EXTENSION)
            self.io.write(path, data, True)
