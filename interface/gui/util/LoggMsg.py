from dataclasses import dataclass


@dataclass
class LogMsgFormatter: 
    INITIALIZE = "{source} initialized" 
    SIGNAL = "signal {signal} send"
    