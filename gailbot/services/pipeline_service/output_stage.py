# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-12-02 13:48:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 11:46:24
import time
from datetime import datetime
import os
# Local imports
from .payload import Payload
from gailbot.core.io import GailBotIO
from gailbot.services.objects import Utt


class OutputStage:

    def __init__(self) -> None:
        self.io = GailBotIO()

    ############################# MODIFIERS ##################################

    def output(self, payload: Payload) -> None:
        try:
            start_time = time.time()
            # Create the different output directories.
            self._create_media_dir(payload)
            self._create_gb_results_dir(payload)
            # Write the metadata
            # Set the times
            payload.source_addons.stats.process_end_time = datetime.now()
            payload.source_addons.stats.output_time_sec = \
                time.time() - start_time
            payload.source_addons.stats.elapsed_time_sec = \
                payload.source_addons.stats.process_end_time - \
                payload.source_addons.stats.process_start_time
            # Nothing should be left outside the directory structure
            self._clear_files(payload)
            # Write metadata
            self._write_metadata(payload)
            # Save the hook to the result directory.
            payload.source.hook.save()
            # Cleanup
            payload.source.hook.cleanup()
            # Write logs
            payload.source_addons.logger.info("Results written to {}".format(
                payload.source.hook.get_result_directory_path()))

        except Exception as e:
            payload.source_addons.logger.error("Output exception {}".format(e))

    ########################## PRIVATE METHODS ###############################

    def _create_media_dir(self, payload: Payload):
        """
        Create a directory containing all the used audio files
        """
        # Save in the temp directory.
        dir_path = "{}/{}".format(
            payload.source.hook.get_temp_directory_path(), "media")
        self.io.create_directory(dir_path)
        # Save all the audio files
        for data_file in payload.source.conversation.data_files:
            media_path = self.io.copy(data_file.audio_path, dir_path)
            payload.source_addons.data_file_paths[data_file.identifier]["media_path"] \
                = "{}/{}.{}".format("media", self.io.get_name(media_path),
                                    self.io.get_file_extension(media_path))

    def _create_gb_results_dir(self, payload: Payload):
        # Save in the temp directory.
        dir_path = "{}/{}".format(
            payload.source.hook.get_temp_directory_path(), "gb_results")
        self.io.create_directory(dir_path)
        self._write_raw_utterances(payload, dir_path)

    def _write_raw_utterances(self, payload: Payload, save_dir_path: str)\
            -> None:
        for identifier, utterances in payload.source_addons.utterances_map.items():
            data = list()
            for utt in utterances:
                utt: Utt
                msg = [str(utt.speaker_label), utt.text,
                       str(utt.start_time_seconds), str(utt.end_time_seconds)]
                msg = ",".join(msg)
                data.append(msg)
            data = "\n".join(data)
            # Save to file
            path = "{}/{}.{}".format(
                save_dir_path, identifier, "gb")
            self.io.write(path, data, True)
            payload.source_addons.data_file_paths[identifier]["raw_path"] = \
                "gb_results/{}.{}".format(identifier, "gb")

    def _write_metadata(self, payload: Payload) -> None:
        save_path = "{}/{}_{}.{}".format(
            payload.source.hook.get_temp_directory_path(),
            payload.source.identifier,
            "metadata", "json")

        result_dir_path = payload.source.hook.get_result_directory_path()

        data_files_info = dict()
        for df in payload.source.conversation.data_files:
            data_files_info[df.identifier] = {
                "original_paths": {
                    "source": df.path,
                    "audio": df.audio_path,
                    "video": df.video_path
                },
                "generated_paths": {
                    "media": payload.source_addons.data_file_paths[df.identifier]["media_path"],
                    "raw": payload.source_addons.data_file_paths[df.identifier]["raw_path"]
                }
            }
        data = {
            "source_identifier": payload.source.identifier,
            "source_info": {
                "settings_profile_name": payload.source.settings_profile.name,
                "result_directory_path": result_dir_path,
                "stats": {
                    "process_date": payload.source_addons.stats.process_date,
                    "process_start_time": payload.source_addons.stats.process_start_time.strftime("%H:%M:%S"),
                    "process_end_time": payload.source_addons.stats.process_end_time.strftime("%H:%M:%S"),
                    "elapsed_time_sec": payload.source_addons.stats.elapsed_time_sec.total_seconds(),
                    "transcription_time_sec": payload.source_addons.stats.transcription_time_sec,
                    "plugin_application_time_sec": payload.source_addons.stats.plugin_application_time_sec,
                    "output_time_sec": payload.source_addons.stats.output_time_sec
                }},
            "data_files": data_files_info
        }
        self.io.write(save_path, data, True)

    def _clear_files(self, payload: Payload) -> None:
        dir_path = payload.source.hook.get_temp_directory_path()
        paths = self.io.path_of_files_in_directory(
            dir_path, ["*"], False)
        for path in paths:
            self.io.delete(path)
