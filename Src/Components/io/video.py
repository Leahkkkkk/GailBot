# Standard library imports 
from Src.utils import threads
from typing import Dict, List, Any, Tuple
from enum import IntEnum
# Local imports 
from ...utils.threads import ThreadPool
# Third party imports
from moviepy.editor import *


class VideoWriteTypes(IntEnum):
    video_audio = 0
    video = 1 
    audio = 2 

class VideoIO:

    # Video formats that are currently supported.
    VIDEO_FORMATS = ("mxf","mov","mp4","wmv","flv","avi","swf","m4v")

    def __init__(self) -> None:
        """
        Params:
            streams (Dict[str, Dict]]):
                Mapping of a unique identifier / name of the video stream 
                to a dictionary containing:
                    1. "path" --> Path of the file.
                    2. "video_clip" --> Video clip associated with that file.
            default_video_format (str): 
                Format video files are written in.
            default_audio_format (str):
                Format audio file are written in.
            num_threads (int): No. of threads used by the thread pool.
            thread_pool (ThreadPool)
        """
        # Params
        self.streams = dict() 
        self.default_video_format = "mp4"
        self.default_audio_format = "wav"
        self.num_threads = 10
        # Starting thread pool
        self.thread_pool = ThreadPool(self.num_threads)
        self.thread_pool.spawn_threads()
    
    ################################# SETTERS ###############################
    def read_streams(self, file_paths : Dict[str,str]) -> bool:
        """
        Read the audio files at the given paths for future operations. 
        Clears all previously read streams from memory. 
        Intended to be used after using the write method to save operations 
        performed on previous streams.

        Args:  
            file_paths (Dict[str,str]):
                Mapping from unique file name to its path.
        
         Returns:
            (bool): True if all files are successfully read. False otherwise.
        """
        # Clears all the previous streams when reading new ones.
        self.streams.clear()
        # If all files exist, they are read as VideoClip objects. 
        for name, file_path in file_paths.items():
            if not self._is_video_file(file_path):
                self.streams.clear()
                return False
            self.streams[name] = {
                "file_path" : file_path,
                "video_clip" : VideoFileClip(file_path)}
        return True

    ################################# GETTERS #############################

    def get_stream_names(self) -> List[str]:
        """
        Get the unique identifiers / names of all the files that are currently 
        ready to have operations performed on.

        Returns:
            (List): Name of all files in stream.
        """
        return  list(self.streams.keys())

    def get_supported_formats(self) -> Tuple:
        """
        Get the video file formats that are supported.

        Returns:
            (Tuple): Supported video file formats
        """
        return tuple(self.VIDEO_FORMATS) 

    ############################### PUBLIC METHODS ########################

    def write(self, output_paths : Dict[str,Dict]) -> bool:
        """
        Write the video streams that were previously read as either a file 
        containing both audio and video, only video, and only audio.

        Args:
            output_paths (Dict[str,Dict]):
                Mapping from stream identifier to a dictionary containing:
                    1. "path" --> Output file path. Must be a directory path.
                    2. "type" --> Type of the output. Must be in VideoWriteTypes

        Returns:
            (bool): True if all files were successfully written. False otherwise.
        """
        # Create a closure to determine thread success
        closure = dict()
        for name in output_paths.keys():
            closure[name] = False 
        for name in output_paths.keys():
            # Verify that all the given output paths have streams associated.
            # and that the output paths are directories.
            if not name in self.streams.keys() or \
                not self._is_directory(output_paths[name]["path"]):
                    return False 
            # Determine output type and file name 
            output_dir_path = output_paths[name]["path"] 
            output_type = output_paths[name]["type"]
            # Write correct type by creating thread.
            if output_type == VideoWriteTypes.video_audio:
                output_file_name = "{}/{}.{}".format(
                output_dir_path,name,self.default_video_format)
                self.thread_pool.add_task(
                    self._write_video_audio,[name,output_file_name,closure]) 
            elif output_type == VideoWriteTypes.audio:
                output_file_name = "{}/{}.{}".format(
                output_dir_path,name,self.default_audio_format)
                self.thread_pool.add_task(
                    self._write_audio,[name,output_file_name,closure])  
            else:
                output_file_name = "{}/{}.{}".format(
                output_dir_path,name,self.default_video_format)
                self.thread_pool.add_task(
                    self._write_video,[name,output_file_name,closure])   
        # Run and wait for all tasks in the pool to finish 
        is_success =  self.thread_pool.wait_completion()
        return is_success and all(closure.values())

    ############################# PRIVATE METHODS ###########################

    def _write_video_audio(self, name : str, output_file_name : str,
            closure : Dict[str,bool]):
        """
        Write an output file containing both video and audio.
        Intended to be used as a thread function.

        Args:
            name (str): Unique identifier for the stream.
            output_file_name (str): Name of the output file.
            closure (Dict[str,bool]): Mapping from unique identifier to True 
                    if successfully written. False otherwise 
        """
        try:
            video_clip = self.streams[name]["video_clip"]
            video_clip.write_videofile(output_file_name)
            closure[name] = True  
        except:
            closure[name] = False  

    def _write_audio(self, name : str, output_file_name : str,
            closure : Dict[str,bool]):
        """
        Write an output file containing only audio.
        Intended to be used as a thread function.

        Args:
            name (str): Unique identifier for the stream.
            output_file_name (str): Name of the output file.
            closure (Dict[str,bool]): Mapping from unique identifier to True 
                    if successfully written. False otherwise 
        """
        try:
            video_clip = self.streams[name]["video_clip"]
            audio = video_clip.audio
            audio.write_audiofile(output_file_name)
            closure[name] = True 
        except:
            closure[name] = False  

    def _write_video(self, name : str, output_file_name : str,
            closure : Dict[str,bool]):
        """
        Write an output file containing only video.
        Intended to be used as a thread function.

        Args:
            name (str): Unique identifier for the stream.
            output_file_name (str): Name of the output file.
            closure (Dict[str,bool]): Mapping from unique identifier to True 
                    if successfully written. False otherwise 
        """
        try:
            video_clip = self.streams[name]["video_clip"]
            video_clip.write_videofile(output_file_name,audio=False)
            closure[name] = True 
        except:
            closure[name] = False  

    #### Others 
    def _does_file_exist(self, file_path : str) -> bool:
        """
        Determines if the file exists.

        Args:
            file_path (str)
        
        Returns:
            (bool): True if file exists. False otherwise.
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def _is_video_file(self, file_path : str) -> bool:
         return self._does_file_exist(file_path) and \
            self._get_file_extension(file_path).lower() in self.VIDEO_FORMATS

    def _get_file_extension(self, file_path : str) -> str:
        """
        Obtain file extension /format, which is the substring after the right-
        most "." character.

        Args:
            file_path (str)
        
        Returns:
            (str): File extension / format.
        """
        return os.path.splitext(file_path.strip())[1][1:] 

    def _is_directory(self, dir_path : str) -> bool:
        """
        Determine if path is a directory.

        Args:
            (str): Path 
        
        Returns:
            (bool): True if path is a directory. False otherwise.
        """
        return os.path.isdir(dir_path)