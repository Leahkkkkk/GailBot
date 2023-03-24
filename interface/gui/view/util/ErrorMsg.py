from dataclasses import dataclass

@dataclass 
class ERR:
    ERR_WHEN_DUETO = "ERROR: an error occurred when {0} due to {1} "
    FAIL_TO        = "ERROR: fail to {0}"
    
@dataclass
class WARN:
    NO_FILE            = "WARNING: no file uploaded"
    NO_OUT_PATH        = "WARNING: no output path is chosen"
    EMPTY_PROFILE_NAME = "WARNING: profile name cannot be empty"
    NO_PLUGIN          = "WARNING: no plugin added"
    BUSY_THREAD        = "WARNING: GailBot is too busy to receive your request!"