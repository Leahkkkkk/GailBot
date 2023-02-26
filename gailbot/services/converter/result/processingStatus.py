from dataclasses import dataclass 
from datetime import date, time


@dataclass 
class ProcessingStats:
    date: date = date.today().strftime("%m/%d/%y") 
    start_time: time = None
    end_time: time = None
    elapsed_time_sec: float = None