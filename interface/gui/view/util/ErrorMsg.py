from dataclasses import dataclass

@dataclass 
class ERR:
    ERR_WHEN_DUETO = "ERROR: An error occurred when {0} due to {1}."
    FAIL_TO        = "ERROR: Fail to {0}."
    
@dataclass
class WARN:
    NO_FILE            = "WARNING: No file has been uploaded."
    NO_OUT_PATH        = "WARNING: No output path has been selected."
    EMPTY_PROFILE_NAME = "WARNING: A profile name must be specified."
    NO_PLUGIN          = "WARNING: No plugin suite has been added."
    INVALID_PLUGIN_URL = "WARNING: Invalid plugin suite url, plugin suite should be hosted in amazon s3 service." 