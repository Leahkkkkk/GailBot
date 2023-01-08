# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-06 15:03:40
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-08 16:29:05



from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from .types import dtype

#########

#########

class BaseHandler:

    def __init__(self):
        pass

    ############################## PUBLIC METHODS ###########################

    #######
    #  All dtype methods
    #######

    def get_type(self, path: str) -> bool:
        """Get the type of the file. """
        pass

    def get_supported_formats(self, dtype : dtype) -> List:
        """Get supported types for specified dtype"""
        pass

    def get_size(self, path : str) -> bytes:
        """Size of file or dir. """
        pass

    def get_name(self, path : str) -> str:
        """Name of file or dir"""
        pass

    def get_extension(self, path : str) -> str:
        pass

    def get_parent_path(self, path : str) -> str:
        pass

    def read(
        self,
        dtype: dtype = None,
        reader_fn : Callable = None
    ) -> Any:
        """
        Read the given file and return the data. If reader_fn given, then
        use it, otherwise try all internal readers.
        """
        pass

    def write(
        self,
        path : str,
        data : Any,
        overwrite : bool = False,
        writer_fn : Callable = None
    ):
        """
        Write data tp file. If writer_fn given, use it, otherwise internal
        writers
        """
        pass

    def convert_format(
        self,
        from_path : str,
        to_path : str
    ) -> bool:
        """
        Convert from given to output path if possible. Format is inferred
        from the specified output path.
        """
        pass

    def move(self, src_path : str, tgt_path : str) -> str:
        """Move file or dir and return the new path"""
        pass

    def copy(self, src_path : str, tgt_path : str) -> str:
        """Copy file or dir and return the new path"""
        pass

    def rename(self, path : str, new_name : str) -> str:
        """Rename file or dir and return new path"""
        pass

    def delete(self, path : str) -> bool:
        """Delete file or dir and return new path"""
        pass

    def reset_dir(self, path : str) -> bool:
        pass

    #######
    # DATA dtype methods
    #######

    def is_directory(self, path: str) -> bool:
        """Determine if path is a directory"""
        pass

    def is_file(self, path: str) -> bool:
        """Determine if the given path is a file"""
        pass


    def get_num_items_in_dir(
        self,
        path: str,
        extensions: List[str],
        check_subdirectories: bool = False,
        only_dirs : bool = False
    ) -> int:
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
            only_dirs (bool): Only applies to dirs.
        """

        pass

    def get_path_items_in_dir(
        self,
        path: str,
        extensions: List[str],
        check_subdirectories: bool,
        only_dirs : bool = False
    ) -> List[str]:
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
            only_dirs (bool): Only applies to dirs.
        """
        pass

    def create_dir(self, path, overwrite : bool = False) -> bool:
        pass

    def record(
        self,
        dtype : dtype,
        duration_secs : float,
        outfile_path : str,
        **kwargs
    ):
        """Record for supported dtype"""
        pass

    #######
    # AUDIO dtype methods
    #######

    def mono_to_stereo(
        self,
        left_path : str,
        right_path : str,
        outdir : str
    ) -> str:
        """
        Convert two mono streams into a single stereo stream.
        The files must have the same number of frames and the same extension.
        The output file has the same extension as both the input files.
        """
        pass

    def stereo_to_mono(
        self,
        path : str,
        outdir : str,
        left_name : str = None,
        right_name : str = None
    ) -> List[str]:
        """
        Convert a stereo stream to two mono streams i.e. left stream and right
        stream, with the same extension as the input file.
        left and right filenames can be optionally specified.
        """
        pass

    def concat(self, paths : List[str], outdir : str) -> str:
        """
        Combine all the streams into a single stream, one after another, in the
        specific order in which they are provided.
        At least one file must be provided and the files must have the same
        extension.
        """
        pass

    def overlay(self, paths : List[str], outdir : str) -> str:
        """
        Overlays two audio streams on top of each other.
        The two files must have the same extensions.
        The overlaid file has the same extension as the input files.
        """
        pass


    def change_volume(
        self,
        path: str,
        change_db : float,
        outdir: str,
        inpace : bool = False
    ) -> str:
        """
        Change the volume, in decibels, of the given file.
        If inplace is True, replace the original file.
        """
        pass

    def reverse(
        self,
        path : str,
        outdir : str,
        inplace : bool = False
    ) -> str:
        """
        Reverse the stream for the file at the given path.
        The name and extension of the reversed file is the same as the
        original file.
        """
        pass

    def chunk(self,
        path : str,
        outdir : str,
        chunk_duration_secs : float
    ) -> str:
        """
        Chunk the given file into chunks of duration
        chunk_duration_seconds.
        """
        pass

    #######
    # VIDEO dtype methods
    #######

    def remove_video(self, path : str, outdir : str) -> str:
        pass

    def remove_audio(self, path : str, outdir : str) -> str:
        pass

    #######
    # SHELL methods
    #######

    def run_cmd(
        self,
        cmd : str,
        stdin : Any,
        stdout : Any,
        on_start : Callable,
        on_end : Callable
    ) -> str:
        """
        Run the command as a shell command and obtain an identifier.
        The identifier can be used to obtain the shell command  status using
        get_shell_process_status.
        """
        pass

    def get_cmd_status(self, identifier : str) -> str:
        """
        Obtain the status of the shell command associated with this identifier
        """
        pass












