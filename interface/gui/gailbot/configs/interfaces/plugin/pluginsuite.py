from dataclasses import dataclass 

@dataclass
class PLUGIN_CONFIG:
    HILAB_BUCKET = "gailbot-plugin"
    THREAD_NUM = 1
    DOCUMENT = "DOCUMENT.md"
    REQUIREMENT = "requirement.txt"
    CONFIG = "config.toml"
    HILAB_SUITE_ZIP = "https://gailbot-plugin.s3.us-east-2.amazonaws.com/gb_hilab_suite.zip" 
