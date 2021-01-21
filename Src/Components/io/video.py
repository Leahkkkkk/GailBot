# Standard library imports 

# Local imports 

# Third party imports 

class VideoIO:

    VIDEO_FORMATS = ("mxf","mov","mp4","wmv","flv","avi","swf","m4v")

    def __init__(self) -> None:
        pass 


    ############################# PRIVATE METHODS ###########################


    def _is_video_file(self, file_path : str) -> bool:
         return self._does_file_exist(file_path) and \
            self._get_file_extension(file_path) in self.VIDEO_FORMATS
