# Standard library imports 
from os import stat
from typing import List, Tuple, Any
# Local imports 
from .audio import AudioIO
from .video import VideoIO, VideoWriteTypes
from .general import GeneralIO
from .shell import ShellIO, ShellStatus
# Third party imports

class IO:
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

    #### Inspectors 

    def is_directory(self, path : str) -> bool:
        """
        Determine if path is a directory.

        Args:
            (str): Path 
        
        Returns:
            (bool): True if path is a directory. False otherwise.
        """
        return self.general.is_directory(path)

    def is_file(self, path : str) -> bool:
        """
        Determine if the given path is a file.

        Args:
            path (str): Path to file.
        
        Returns:
            (bool): True if path is a file. False otherwise.
        """
        return self.general.is_file(path) 

    def number_of_files_in_directory(self, path : str, extensions : List[str],
            check_subdirectories : bool) -> Tuple[bool,int]:
        """
        Determine the number of files in the directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for. 
                        Ex: ["pdf"]. '*' is a wildcard and considers all 
                        extensions. default = ["*"]
            check_subdirectories (bool): True to check subdirectories. 
                                False otherwise. default = False 
        
        Returns:   
            (Tuple[bool,int]): True + number of files if successful.
                                False + None if unsuccessful.
        """
        return self.general.number_of_files_in_directory(
            path, extensions,check_subdirectories) 

    def names_of_file_in_directory(self, path : str, extensions : List[str],
            check_subdirectories : bool) -> Tuple[bool,List[str]]:
        """
        Determine the names of files in the directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for. 
                        Ex: ["pdf"]. '*' is a wildcard and considers all 
                        extensions. default = ["*"]
            check_subdirectories (bool): True to check subdirectories. 
                                        False otherwise. default = False 
        
        Returns:   
            (Tuple[bool,List[str]]): True + names of files if successful.
                                False + None if unsuccessful.
        """
        return self.general.names_of_file_in_directory(
            path,extensions,check_subdirectories) 

    #### Audio, video, and general manipulation methods 

    def read(self, path : str) -> Tuple[bool,Any]:
        """
        Read and obtain the raw data from a file.

        Args:
            path (str): Path to the file.
        
        Returns:
            (Tuple[bool,Any]): True + raw data is successful.
                                False + None if unsuccessful.
        """
        success = False 
        data = None
        # Use the appropriate object to read the file
        if self.general.is_readable(path):
            success, data = self.general.read_file(path)
        elif self.audio.is_readable(path):
            success = self.audio.read_streams({"audio_file" : path})
            if success:
                data = self.audio.get_streams()["audio_file"]
        return (success,data)

    def write(self, file_path : str, format : str, data : Any ,
            overwrite : bool) -> bool:
        """
        Write the given data to a file.
        NOTE: Only json, yaml, txt formats supported.

        Args:
            file_path (str): Path to output file, including name and extension.
            format (str): Format the file should be written in.
            data (Any)
            overwrite (bool): True to overwrite any existing file. 
                            False to append to existing file.

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.general.write_to_file(file_path,format,data,overwrite)

    def convert_format(self, file_path : str, output_format : str,
            output_dir_path : str) -> bool:
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
                return False 
            output_file_name = self._get_file_name_from_path(file_path)
            output_path = "{}/{}.{}".format(
                output_dir_path,output_file_name,output_format)
            return self.general.write_to_file(output_path,data,True)
        elif self.audio.is_readable(file_path):
            output_file_name = self._get_file_name_from_path(file_path)
            self.audio.read_streams({output_file_name : file_path})
            self.audio.set_output_formats({output_file_name : output_format})
            self.audio.set_output_paths({output_file_name : output_dir_path})
            return self.audio.write([output_file_name])
        elif self.video.is_readable(file_path):
            output_file_name = self._get_file_name_from_path(file_path)
            self.video.read_streams({output_file_name : file_path})
            self.video.set_output_formats({output_file_name : output_format})
            self.video.set_output_paths({output_file_name : output_dir_path})
            return self.video.write([output_file_name])
        return False 

    #### General only methods

    def create_directory(self, dir_path : str) -> bool:
        """
        Create a new directory with the given path.

        Args:
            dir_path (str): Path of the new directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.general.create_directory(dir_path) 

    def move_file(self, src_file_path : str, dst_dir_path : str) -> bool:
        """
        Move a source file to the destination directory.
        
        Args:
            src_file_path (str): Source file or directory path
            dst_dir_path (str): Path to destination directory. Must be an 
                                existing directory.
    
        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.general.move_file(src_file_path,dst_dir_path)

    def copy(self, src_path : str, dst_path : str) -> bool:
        """
        Copy the source file or directory to the destination file or directory.

        Args:
            src_path (str): Path of source file / directory 
            dst_path (str): Path of destination file / directory 
            
        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.general.copy(src_path, dst_path)

    def rename(self, src_path : str, new_name : str) -> bool:
        """
        Rename the source file or directory.

        Args:
            src_path (str): Path to the source file / directory.
            new_name (str): New names 
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.general.rename(src_path, new_name) 

    def delete(self, path : str) -> bool:
        """
        Delete the given file or directory. For a directory, deletes all 
        sub-directories as well.

        Args:
            path (str): Path of file / directory to delete .
        
        Returns:
           (bool): True if successful. False otherwise  
        """
        return self.general.delete(path) 

    #### Audio only manipulation methods 

    def record_audio(self, duration_seconds : float, output_file_name : str,
            output_dir_path : str = None) -> Tuple[bool, Any]:
        """
        Record audio from the primary microphone of the current device.
        Always returns the raw recorded data.

        Args:
            duration_seconds (float): Duration of the recording.
            output_file_name (str): Name of the output file, without extension
            output_dir_path (str): 
                Path of the output directory. If this is None, the file is not 
                written.
            
        Returns:
            (Tuple[bool,Any]): True + raw data if successful.
                                False + None if unsuccessful.
        """
        # Recording and getting raw data 
        self.audio.record_stream(output_file_name,duration_seconds)
        raw_data = self.audio.get_streams()[output_file_name]
        if output_dir_path != None:
            return (self.write({output_file_name : output_dir_path}),raw_data)
        return (True, raw_data)

    def mono_to_stereo(self, file_1_path : str, file_2_path : str, 
            output_dir_path : str) -> bool:
        """
        Convert two mono streams into a single stereo stream. 
        The files must have the same numbfer of frames.
     
        Args:
            file_1_path (str): Path to first mono file.
            file_2_path (str): Path to second mono file.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise  
        """
        if not self.audio.is_readable(file_1_path) or \
                not self.audio.is_readable(file_2_path):
            return False 
        # Getting the file names 
        name_1 = self._get_file_name_from_path(file_1_path)
        name_2 =  self._get_file_name_from_path(file_2_path)
        self.audio.read_streams(
            {name_1 : file_1_path, name_2 : file_2_path})
        _ , identifier = self.audio.mono_to_stereo()
        self.audio.set_output_paths({identifier : output_dir_path})
        return self.audio.write([identifier])

    def stereo_to_mono(self, file_path : str, output_dir_path : str) -> bool:
        """
        Convert a stereo stream to two mono streams i.e. left stream and right 
        stream. 

        Args:
            file_path (str): Path to stereo file.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise  
        """
        if not self.audio.is_readable(file_path):
            return False  
        # Getting the file name 
        file_name = file_path[file_path.rfind("/")+1:file_path.rfind(".")]
        self.audio.read_streams({file_name : file_path})
        _ , identifiers = self.audio.stereo_to_mono()
        self.audio.set_output_paths({
            identifiers[0] : output_dir_path,
            identifiers[1] : output_dir_path})
        return self.audio.write(identifiers)

    def concat(self, file_paths : List[str], output_dir_path : str) -> bool:
        """
        Combine all the streams into a single stream, one after another, in the 
        specific order in which they are provided.
        At least one file must be provided.

        Args:
            file_paths (List[str]): Path to files to concat in a specific order
            output_dir_path (str): Path to the output directory.
        
        Returns:
            (bool): True if successful. False otherwise 
        """
        if len(file_paths) < 1:
            return False 
        name_to_path = dict()
        for path in file_paths:
            if not self.audio.is_readable(path):
                return False 
            file_name = self._get_file_name_from_path(path)
            name_to_path[file_name] = path 
        # Reading and concatenating.
        self.audio.read_streams(name_to_path)
        _, combined_identifier = self.audio.concat()
        return self.audio.write({combined_identifier : output_dir_path})

    def overlay(self, file_paths : List[str], output_dir_path : str) -> bool:
        """
        Overlays two audio streams on top of each other.

        Args:
            file_paths (List[str]): Path to files to overlay. Must be two only.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise
        """
        if len(file_paths) != 2 or \
                not self.audio.is_readable(file_paths[0]) or \
                not self.audio.is_readable(file_paths[1]):
            return False
        # Getting names 
        name_1 = self._get_file_name_from_path(file_paths[0])
        name_2 = self._get_file_name_from_path(file_paths[1])
        # Overlaying 
        self.audio.read_streams({name_1: file_paths[0], name_2 : file_paths[1]}) 
        _, identifier = self.audio.overlay()
        return self.audio.write({identifier : output_dir_path})

    def change_volume(self, file_path : str, change_in_decibels : float, 
            output_dir_path : str) -> bool:
        """
        Change the volume of the given file .

        Args:
            file_path (str): Path to the input file.
            change_in_decibels (float): Can be a positive or negative value 
                                representing the volume change in decibels.
            output_dir_path (str): Path to the output directory.
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.audio.is_readable(file_path):
            return False 
        # Getting file name
        name = self._get_file_name_from_path(file_path)
        self.audio.read_streams({name : file_path})
        return self.audio.change_volume({name : change_in_decibels}) and \
            self.write({name : output_dir_path})
    
    def reverse_audio(self, file_path : str, output_dir_path : str) -> bool:
        """
        Reverse the audio stream for the file at the given path.

        Args:
            file_path (str): Path to the audio file.
            output_dir_path (str): Path to the output directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.audio.is_readable(file_path):
            return False
        name = self._get_file_name_from_path(file_path)
        return self.audio.read_streams({name : file_path}) and \
            self.audio.reverse() and \
            self.audio.write({name : output_dir_path})

    def chunk(self, file_path : str, output_dir_path : str,
            chunk_duration_seconds : float) -> bool:
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
            return False
        name = self._get_file_name_from_path(file_path)
        self.audio.read_streams({name : file_path})
        did_chunk, chunk_names = self.audio.chunk(
            {name : chunk_duration_seconds})
        if not did_chunk:
            return False
        paths = dict()
        for chunk_name in chunk_names:
            paths [chunk_name] = output_dir_path
        self.audio.set_output_paths(paths)
        return self.audio.write(chunk_names)

    #### Video only manipulation methods

    def extract_video_from_file(self, file_path : str,output_dir_path : str ) \
            -> bool:
        """
        Extract the video only, without audio, from the video file at the 
        given path.

        Args:
            file_path (str): Path to the audio file.
            output_dir_path (str): Path to the output directory.
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        # Ensure readability
        if not self.video.is_readable(file_path):
            return False 
        # Extract video 
        name = self._get_file_name_from_path(file_path)
        self.video.read_streams({name : file_path})
        self.video.set_output_paths({name : output_dir_path})
        return self.video.write({name : VideoWriteTypes.video})

    def extract_audio_from_file(self, file_path : str,output_dir_path : str )\
             -> bool:
        """
        Extract the audio from the video file at the given path.

        Args:
            file_path (str): Path to the audio file.
            output_dir_path (str): Path to the output directory.
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        # Ensure readability
        if not self.video.is_readable(file_path):
            return False 
        # Extract audio
        name = self._get_file_name_from_path(file_path)
        self.video.read_streams({name : file_path})
        self.video.set_output_paths({name : output_dir_path})
        return self.video.write({name : VideoWriteTypes.audio})

    #### Shell methods 

    def run_shell_command(self, shell_command : str, stdin : Any, 
            stdout : Any) -> Tuple[bool,str]:
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
        self.shell.add_command("cmd", shell_command,stdout,stdin)
        return self.shell.run_command("cmd")
    
    def get_shell_process_status(self, identifier : str) -> str:
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

    def _get_file_name_from_path(self, path : str) -> str:
        """
        Extract the file name, without the extension, from the path.
        Path must be valid.

        Args:
            path (str): Path to file.

        Returns:
            (str): Extracted file name, without extension
        """ 
        return path[path.rfind("/")+1:path.rfind(".")]