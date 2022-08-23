# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-30 17:58:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-23 10:11:47

# Standard library imports
from typing import List, Tuple, Any
# Local imports
from gailbot.core.io.audio import AudioIO
from gailbot.core.io.video import (
    VideoIO, VideoWriteTypes
)
from gailbot.core.io.general import GeneralIO
from gailbot.core.io.shell import (
    ShellIO,
    ShellStatus
)


class GailBotIO:
    """
    Responsible for providing the main API for all input/operations.
    """

    def __init__(self) -> None:
        """
        audio (AudioIO): Provides audio manipulation methods
        video (VideoIO): Provides video manipulation methods
        general (GeneralIO): Provides file system manipulation methods.
        shell (ShellIO): Provides access to running subprocesses in a shell.
        """
        # Objects for IO
        self.audio = AudioIO()
        self.video = VideoIO()
        self.general = GeneralIO()
        self.shell = ShellIO()

    ############################## PUBLIC METHODS ###########################

    # Inspectors

    def is_directory(self, path: str) -> bool:
        """
        Determine if path is a directory.
        """
        return self.general.is_directory(path)

    def is_file(self, path: str) -> bool:
        """
        Determine if the given path is a file.
        """
        return self.general.is_file(path)

    def is_supported_audio_file(self, path: str) -> bool:
        """
        Determine if the given file is a supported audio file.
        """
        return self.audio.is_readable(path)

    def is_supported_video_file(self, path: str) -> bool:
        """
        Determine if the given file is a supported video file.
        """
        return self.video.is_readable(path)

    def number_of_files_in_directory(
            self, path: str, extensions: List[str],
            check_subdirectories: bool = False) -> int:
        """
        Determine the number of files in the directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for.
                        Ex: ["pdf"]. '*' is a wildcard and considers all
                        extensions. Does not consider sub-directories.
                        default = ["*"]
            check_subdirectories (bool): True to check subdirectories.
                                False otherwise. default = False
        """
        success, num = self.general.number_of_files_in_directory(
            path, extensions, check_subdirectories)
        if not success:
            raise Exception()
        return num

    def path_of_files_in_directory(
            self, path: str, extensions: List[str],
            check_subdirectories: bool) -> List[str]:
        """
        Determine the paths, relative to dir_path, of all files in the
        directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for.
                        Ex: ["pdf"]. '*' is a wildcard and considers all
                        extensions. Does not consider sub-directories.
                        default = ["*"]
            check_subdirectories (bool): True to check subdirectories.
                                        False otherwise. default = False
        """
        success, paths = self.general.path_of_files_in_directory(
            path, extensions, check_subdirectories)
        if not success:
            raise Exception()
        return paths

    def number_of_subdirectories(self, dir_path: str) -> int:
        """
        Obtain the number of subdirectories in a ditrectory
        """
        success, num = self.general.number_of_subdirectories(dir_path)
        if not success:
            raise Exception()
        return num

    def paths_of_subdirectories(self, dir_path: str) -> List[str]:
        """
        Obtain the paths of all subdirectories in a directory.

        Args:
            dir_path (str): path to the directory.

        Returns:
            (Tuple[bool,List[str]]):
                True + paths of subdirectories if successful.
                False + None if unsuccessful.
        """
        success, paths = self.general.paths_of_subdirectories(dir_path)
        if not success:
            raise Exception()
        return paths

    def get_supported_audio_formats(self) -> List[str]:
        """
        Obtain a list of supported audio formats.
        """
        return self.audio.get_supported_input_formats()

    def get_supported_video_formats(self) -> List[str]:
        """
        Obtain a list of suppoorted video formats.
        """
        return self.video.get_supported_formats()

    # Audio, video, and general manipulation methods

    def read(self, path: str) -> Tuple[bool, Any]:
        """
        Read and obtain the raw data from a file.
        """
        success = False
        data = None
        # Use the appropriate object to read the file
        if self.audio.is_readable(path):
            success = self.audio.read_streams({"audio_file": path})
            if success:
                data = self.audio.get_streams()["audio_file"]
        else:
            success, data = self.general.read_file(path)
        return (success, data)

    def write(self, file_path: str, data: Any, overwrite: bool) -> bool:
        """
        Write the given data to a file. The file extension must be supported.

        Args:
            file_path (str): Path to output file, including name and extension.
            data (Any)
            overwrite (bool): True to overwrite any existing file.
                            False to append to existing file.

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.general.write_to_file(file_path, data, overwrite)

    def convert_format(self, file_path: str, output_format: str,
                       output_dir_path: str) -> str:
        """
        Convert the given input file to a new format.

        Args:
            file_path (str): Path to original file, including name and extension
            output_format (str): Extension of the new file.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if self.general.is_readable(file_path):
            did_read, data = self.general.read_file(file_path)
            if not did_read:
                return
            output_file_name = self._get_file_name_from_path(file_path)
            output_path = "{}/{}.{}".format(
                output_dir_path, output_file_name, output_format)
            success = self.general.write_to_file(output_path, data, True)
            if success:
                return output_path
        elif self.audio.is_readable(file_path):
            output_file_name = self._get_file_name_from_path(file_path)
            self.audio.read_streams({output_file_name: file_path})
            self.audio.set_output_formats({output_file_name: output_format})
            self.audio.set_output_paths({output_file_name: output_dir_path})
            success, paths = self.audio.write([output_file_name])
        elif self.video.is_readable(file_path):
            output_file_name = self._get_file_name_from_path(file_path)
            self.video.read_streams({output_file_name: file_path})
            self.video.set_output_formats({output_file_name: output_format})
            self.video.set_output_paths({output_file_name: output_dir_path})
            success, paths = self.video.write([output_file_name])
        if success:
            return paths[output_file_name]
        raise Exception()

    # General only methods

    def get_size(self, path: str) -> bytes:
        """
        Gets size of file with given path. If a directory, the total size is
        the size of all items in the directory, including any sub-directories.

        Args:
            path (str): Path of the file/directory to get size.

        """
        return self.general.get_size(path)[1]

    def get_name(self, path: str) -> str:
        """
        Obtains name of file/directory of given path.

        Args:
            path (str): Path of the file/directory to get name.

        Returns:
            (str): Name of the file or directory, without extension
        """
        return self.general.get_name(path)

    def get_file_extension(self, file_path: str) -> str:
        """
        Obtains file extension of file of given path.

        Args:
            file_path (str): File path of the file to get extension.

        Returns:
            (Tuple[bool,str])
                True + file extension if successful.
                False + None if unsuccessful (i.e. not valid path to file).
        """
        if not self.general.is_file(file_path):
            raise Exception()
        return self.general.get_file_extension(file_path)

    def get_parent_path(self, path: str) -> str:
        """
        Obtain the absolute path of the parent directory given a path to a file or
        directory.

        Returns:
            (str): Absolute parent directory path for the given file or directory.
                    Empty string if parent directory cannot be determined.
        """
        return self.general.get_parent_directory(path)

    def create_directory(self, dir_path: str) -> bool:
        """
        Create a new directory with the given path.

        """
        return self.general.create_directory(dir_path)

    def move_file(self, src_file_path: str, dst_dir_path: str) -> str:
        """
        Move a source file to the destination directory.

        Args:
            src_file_path (str): Source file or directory path
            dst_dir_path (str): Path to destination directory. Must be an
                                existing directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, output_path = self.general.move_file(
            src_file_path, dst_dir_path)
        if not success:
            raise Exception()
        return output_path

    def copy(self, src_path: str, dst_path: str) -> str:
        """
        Copy the source file or directory to the destination file or directory.

        Args:
            src_path (str): Path of source file / directory
            dst_path (str): Path of destination file / directory
        """
        success, output_path = self.general.copy(src_path, dst_path)
        if not success:
            raise Exception()
        return output_path

    def rename(self, src_path: str, new_name: str) -> str:
        """
        Rename the source file or directory.

        Args:
            src_path (str): Path to the source file / directory.
            new_name (str): name of the new file or directpry only, NOT
                            the complete path. Should not contain extension or
                            backslashes.

        Returns:
            (bool): True if successful. False otherwise.
        """
        success, output_path = self.general.rename(src_path, new_name)
        if not success:
            raise Exception()
        return output_path

    def delete(self, path: str) -> bool:
        """
        Delete the given file or directory. For a directory, deletes all
        sub-directories as well.

        Args:
            path (str): Path of file / directory to delete .

        Returns:
           (bool): True if successful. False otherwise
        """
        return self.general.delete(path)

    def clear_directory(self, dir_path: str) -> bool:
        """
        Remove the files in a directory
        """
        return self.general.clear_directory(dir_path)

    # Audio only manipulation methods

    def record_audio(self, duration_seconds: float, output_file_name: str,
                     output_dir_path: str = None) -> Tuple[bool, Any]:
        """
        Record audio from the primary microphone of the current device.
        Always returns the raw recorded data.

        Args:
            duration_seconds (float): Duration of the recording in seconds.
            output_file_name (str): Name of the output file, without extension
            output_dir_path (str):
                Path of the output directory. If this is None, the file is not
                written but simply stored internally.

        Returns:
            (Tuple[bool,Any]): True + raw data if successful.
                                False + None if unsuccessful.
        """
        # Recording and getting raw data
        is_recorded = self.audio.record_stream(
            output_file_name, duration_seconds)
        if is_recorded:
            raw_data = self.audio.get_streams()[output_file_name]
            if output_dir_path != None:
                self.audio.set_output_paths(
                    {output_file_name: output_dir_path})
                success, _ = self.audio.write([output_file_name])
                return success, raw_data
            return (True, raw_data)
        else:
            return (False, None)

    def mono_to_stereo(self, file_1_path: str, file_2_path: str,
                       output_dir_path: str) -> str:
        """
        Convert two mono streams into a single stereo stream.
        The files must have the same number of frames and the same extension.
        The output file has the same extension as both the input files.

        Args:
            file_1_path (str): Path to first mono file.
            file_2_path (str): Path to second mono file.
            output_dir_path (str): Path to the output directory.

        """
        if not self.audio.is_readable(file_1_path) or \
                not self.audio.is_readable(file_2_path):
            raise Exception()
        # Getting the file names
        name_1 = self._get_file_name_from_path(file_1_path)
        name_2 = self._get_file_name_from_path(file_2_path)
        self.audio.read_streams(
            {name_1: file_1_path, name_2: file_2_path})
        _, identifier = self.audio.mono_to_stereo()
        self.audio.set_output_paths({identifier: output_dir_path})
        success, paths = self.audio.write([identifier])
        if success:
            return paths[identifier]
        raise Exception()

    def stereo_to_mono(self, file_path: str, output_dir_path: str) \
            -> List[str]:
        """
        Convert a stereo stream to two mono streams i.e. left stream and right
        stream, with the same extension as the input file.

        Args:
            file_path (str): Path to stereo file.
            output_dir_path (str): Path to the output directory.

        Returns:
            [name of file 1, name of file 2]

        """
        if not self.audio.is_readable(file_path):
            raise Exception()
        # Getting the file name
        file_name = file_path[file_path.rfind("/")+1:file_path.rfind(".")]
        self.audio.read_streams({file_name: file_path})
        _, identifiers = self.audio.stereo_to_mono()
        self.audio.set_output_paths({
            identifiers[0]: output_dir_path,
            identifiers[1]: output_dir_path})
        success, paths = self.audio.write(identifiers)
        if success:
            return [paths[id] for id in identifiers]
        raise Exception()

    def concat(self, file_paths: List[str], output_dir_path: str) \
            -> str:
        """
        Combine all the streams into a single stream, one after another, in the
        specific order in which they are provided.
        At least one file must be provided and the files must have the same
        extension.

        Args:
            file_paths (List[str]): Path to files to concat in a specific order
            output_dir_path (str): Path to the output directory.

        Returns:
            (Tuple[bool,str]):
                True + name of the output file, without extension, if successful.
                False + None otherwise.
        """
        if len(file_paths) < 1:
            raise Exception()
        name_to_path = dict()
        for path in file_paths:
            if not self.audio.is_readable(path):
                raise Exception()
            file_name = self._get_file_name_from_path(path)
            name_to_path[file_name] = path
        # Reading and concatenating.
        self.audio.read_streams(name_to_path)
        _, combined_identifier = self.audio.concat()
        self.audio.set_output_paths({combined_identifier: output_dir_path})
        did_write, paths = self.audio.write([combined_identifier])
        if did_write:
            return paths[combined_identifier]
        else:
            raise Exception()

    def overlay(self, file_paths: List[str], output_dir_path: str) \
            -> str:
        """
        Overlays two audio streams on top of each other.
        The two files must have the same extensions.
        The overlaid file has the same extension as the input files.

        Args:
            file_paths (List[str]): Path to files to overlay. Must be two only.
            output_dir_path (str): Path to the output directory.

        Returns:
            (Tuple[bool,str]):
                True + name of the output file, without extension, if successful
                False + None otherwise.
        """
        if len(file_paths) != 2 or \
                not self.audio.is_readable(file_paths[0]) or \
                not self.audio.is_readable(file_paths[1]):
            raise Exception()
        # Getting names
        name_1 = self._get_file_name_from_path(file_paths[0])
        name_2 = self._get_file_name_from_path(file_paths[1])
        # Overlaying
        self.audio.read_streams({name_1: file_paths[0], name_2: file_paths[1]})
        _, identifier = self.audio.overlay()
        self.audio.set_output_paths({identifier: output_dir_path})
        return identifier

    def change_volume(self, file_path: str, change_in_decibels: float,
                      output_dir_path: str) -> str:
        """
        Change the volume, in decibels, of the given file. The output file has
        the same name and extension as the input file.

        Args:
            file_path (str): Path to the input file.
            change_in_decibels (float):
                Can be a positive or negative value representing the volume
                change in decibels.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.audio.is_readable(file_path):
            raise Exception()
        # Getting file name
        name = self._get_file_name_from_path(file_path)
        self.audio.read_streams({name: file_path})
        if self.audio.change_volume({name: change_in_decibels}) and \
                self.audio.set_output_paths({name: output_dir_path}) and \
                self.audio.write([name])[0]:
            return "{}/{}.{}".format(
                output_dir_path, self.general.get_name(file_path),
                self.general.get_file_extension(file_path))
        raise Exception()

    def reverse_audio(self, file_path: str, output_dir_path: str) -> str:
        """
        Reverse the audio stream for the file at the given path.
        The name and extension of the reversed file is the same as the
        original file.

        Args:
            file_path (str): Path to the audio file.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.audio.is_readable(file_path):
            raise Exception()
        name = self._get_file_name_from_path(file_path)
        if self.audio.read_streams({name: file_path}) and \
                self.audio.reverse([name]) and \
                self.audio.set_output_paths({name: output_dir_path}) and \
                self.audio.write([name])[0]:
            return "{}/{}.{}".format(
                output_dir_path, self.general.get_name(file_path),
                self.general.get_file_extension(file_path))
        raise Exception()

    def chunk(self, file_path: str, output_dir_path: str,
              chunk_duration_seconds: float) -> List[str]:
        """
        Chunk the given audio file into chunks of duration
        chunk_duration_seconds.

        Args:
            file_path (str): Path to the audio file.
            output_dir_path (str): Path to the output directory.
            chunk_duration_seconds (float): Duration of each chunk in seconds.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.audio.is_readable(file_path):
            raise Exception()
        name = self._get_file_name_from_path(file_path)
        self.audio.read_streams({name: file_path})
        did_chunk, chunk_names = self.audio.chunk(
            {name: chunk_duration_seconds})
        if not did_chunk:
            raise Exception()
        paths = dict()
        all_chunk_names = list(chunk_names.values())[0]
        for chunk_name in all_chunk_names:
            paths[chunk_name] = output_dir_path
        self.audio.set_output_paths(paths)
        _, paths = self.audio.write(all_chunk_names)
        return list(paths.values())

    # Video only manipulation methods

    def extract_video_from_file(self, file_path: str, output_dir_path: str) \
            -> str:
        """
        Extract the video only, without audio, from the video file at the
        given path. The name of the output file, without extension, is the
        same as the name for the input file.

        Args:
            file_path (str): Path to the audio file.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        # Ensure readability
        if not self.video.is_readable(file_path) or \
                not self.general.is_directory(output_dir_path):
            return False
        # Extract video
        name = self._get_file_name_from_path(file_path)
        self.video.read_streams({name: file_path})
        self.video.set_output_paths({name: output_dir_path})
        _, paths = self.video.write({name: VideoWriteTypes.video})
        return paths[name]

    def extract_audio_from_file(self, file_path: str, output_dir_path: str)\
            -> str:
        """
        Extract the audio from the video file at the given path.

        Args:
            file_path (str): Path to the audio file.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        # Ensure readability
        if not self.video.is_readable(file_path) or \
                not self.general.is_directory(output_dir_path):
            return
        # Extract audio
        name = self._get_file_name_from_path(file_path)
        self.video.read_streams({name: file_path})
        self.video.set_output_paths({name: output_dir_path})
        success, paths = self.video.write({name: VideoWriteTypes.audio})
        return paths[name]

    # Shell methods

    def run_shell_command(self, shell_command: str, stdin: Any,
                          stdout: Any) -> Tuple[bool, str]:
        """
        Run the command as a shell command and obtain an identifier.
        The identifier can be used to obtain the shell command  status using
        get_shell_process_status.

        Args:
            shell_command (str): Command to run in the shell.
            stdin (Any): Input pipe for the shell.
            stdout (Any): Output pipe for the shell.

        Returns
            (Tuple[bool,str]):
                True + the identifier associated with this command. False + None
                otherwise.
        """
        cmd_name = str(shell_command)
        self.shell.add_command(cmd_name, shell_command, stdout, stdin)
        return (self.shell.run_command(cmd_name), cmd_name)

    def get_shell_process_status(self, identifier: str) -> str:
        """
        Obtain the status of the shell command associated with this identifier.

        Args:
            identifier (str): Command identifier obtained from run_shell_command
                            method.

        Returns:
            (str): Status of the shell command. Can be one of:
                    1. running
                    2. finished
                    3. error
                    4. ready
                    5. Empty string if identifier incorrect.
        """
        success, status = self.shell.get_status(identifier)
        if not success:
            return ""
        if status == ShellStatus.running:
            return "running"
        elif status == ShellStatus.finished:
            return "finished"
        elif status == ShellStatus.error:
            return "error"
        else:
            return "ready"

    ################################ PRIVATE METHODS #########################

    def _get_file_name_from_path(self, path: str) -> str:
        """
        Extract the file name, without the extension, from the path.
        Path must be valid.

        Args:
            path (str): Path to file.

        Returns:
            (str): Extracted file name, without extension
        """
        return self.general.get_name(path)
