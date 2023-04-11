from dataclasses import dataclass 

@dataclass
class PLUGIN_CONFIG:
    HILAB_BUCKET = "gailbot-plugin"
    ENCRYPTED_API_KEY = b"yrTw50nWlIzTtSLKplGdYTkPjeGHgChIdjDKkj7S9Fs="
    EN_KEY = b"gAAAAABkNdIg3vorysUl8XC81I3KeIgnvAVI281wPp0KoOfyR1fnbKyu5Vz8ToTd4nvHU2fWmPgHxA3prRZAQp0bzJr93SsmxtprexkMB-vazN2Fuscs4YE="
    THREAD_NUM = 1
    DOCUMENT = "DOCUMENT.md"
    REQUIREMENT = "requirement.txt"
    CONFIG = "config.toml"
    HILAB_SUITE_ZIP = "https://gailbot-plugin.s3.us-east-2.amazonaws.com/gb_hilab_suite.zip" 

