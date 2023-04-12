from dataclasses import dataclass 

@dataclass
class PLUGIN_CONFIG:
    HILAB_BUCKET = "gailbot-plugin"
    # ENCRYPTED_API_ID = b"gAAAAABkNd8AP7Q472BV75v2rKpdcJ4Zzw5mdRZixIFD3l5q9UsDQKr0agJZub8q0Q0HNLO9am2pll-b_DacyuUmEMiSBjkHAQ=="
    ENCRYPTED_API_ID = b"gAAAAABkNd7pnDm4xp6E8GhbBoXGNzU5SFN5SSdGhDpzr0i61Fi2EyVxIBe6L5D1YtWmQY0Y4oeokSeLASWNUO4njEfLtUT5SKFx7g4Dyd2HCOV0SZiZywQ="
    ENCRYPTED_API_KEY =b"gAAAAABkNr-Od9fWNwWxlZGmsH5AvnTuqCFowq0OqnOlQtN2S6EyW-QZQIghFOZzdwXDp2EyYwJqqIuIMMklOnB6d1f1J3yOvMtWO7keDg7fs2-3esZ7MQ74Bmtbh_YE5TZTayY50MFS"
    EN_KEY = b"25T_bNAjTALUgva1C-au0IKwESptsLAztLRVVEyCtZs="
    THREAD_NUM = 1
    DOCUMENT = "DOCUMENT.md"
    REQUIREMENT = "requirement.txt"
    CONFIG = "config.toml"
    HILAB_SUITE_ZIP = "https://gailbot-plugin.s3.us-east-2.amazonaws.com/gb_hilab_suite.zip" 

