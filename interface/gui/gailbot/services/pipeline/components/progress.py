
from dataclasses import dataclass
@dataclass 
class ProgressMessage: 
    Start = "\u25B6 Start" 
    Waiting = "\U0001F551 Waiting"
    Transcribing = "\u25CC Transcribing"
    Finished = "\u2705 Completed"
    Transcribed = "\u2705 Transcribed"
    Error = "\U0001F6AB Error"
    Analyzing  = "\U0001F4AC Analyzing" 
    Analyzed = "\u2705 Analyzed" 
    
