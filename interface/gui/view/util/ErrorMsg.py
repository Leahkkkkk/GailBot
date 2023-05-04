from dataclasses import dataclass

@dataclass 
class ERR:
    ERR_WHEN_DUETO = "ERROR 040: An error occurred when {0} due to {1}."
    FAIL_TO        = "ERROR 041: Fail to {0}."
    
@dataclass
class WARN:
    NO_FILE            = "WARNING 050: No file has been uploaded."
    NO_OUT_PATH        = "WARNING 050: No output path has been selected."
    EMPTY_PROFILE_NAME = "WARNING 051: A profile name must be specified."
    NO_PLUGIN          = "WARNING 050: No plugin suite has been added."
    INVALID_PLUGIN_URL = "WARNING 052: Invalid plugin suite url, plugin suite should be hosted in amazon s3 service." 