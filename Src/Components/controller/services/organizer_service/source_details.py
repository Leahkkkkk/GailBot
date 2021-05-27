# Standard library imports
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SourceDetails:
    name : str
    settings_profile_name : str
    source_size : str
    source_type : str
    transcription_date : str
    transcription_status : str
    transcription_time : str
    transcriber_name : str
    number_of_source_files : int
    number_of_speakers : int
    source_file_names : List[str]
    source_file_types : Dict[str, str]
    result_directory_path : str
    source_path : str


