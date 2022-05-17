# GailBot

**NOTE**: This documentation is a work in progress and will be updated.


## About

Researchers studying human interaction, such as conversation analysts, psychologists, and linguists all rely on detailed transcriptions of language use. Ideally, these should include so-called paralinguistic features of talk, such as overlaps, prosody, and intonation, as they convey important information. However, transcribing these features by hand requires substantial amounts of time by trained transcribers. There are currently no Speech to Text (STT) systems that are able to annotate these features. To reduce the resources needed to create transcripts that include paralinguistic features, we developed a program called GailBot. GailBot combines STT services with plugins to automatically generate first drafts of conversation analytic transcripts. It also enables researchers to add new plugins to transcribe additional features, or to improve the plugins it currently uses. We argue that despite its limitations, GailBot represents a substantial improvement over existing dialogue transcription software.

Find the full paper published by Dialogue and Discourse [here](https://journals.uic.edu/ojs/index.php/dad/article/view/11392).

## Status

GailBot version: 0.0.1x (Pre-release)

Supported OS: MacOs 11.6, Ubuntu 20.04

Release type: API

## Installation

GailBot can be installed using pip or from the Github repository.

### Pip installation

To install program dependencies, execute the following:

```
pip install \
    pyaudio \
    ffmpeg
```

To install via pip, run the following commands:

```
pip install --upgrade pip

python3 -m pip install GailBot
```

## Usage

This GailBot release features a convenient API to use GailBot and create custom plugin suites.

GailBot usage will consist of two main components: a driver code and optional plugin suites that may need to be applied.

### GailBot API

To support the driver code, GailBot provides two main classes that may be imported as follows in a python script:

```
from gailbot.core import GailBotController, GailBotSettings
```

The GailBotController class provides the main API for transcribing sources, applying settings to different sources, and starting the transcription process. On the other hand, GailBotSettings are applied to each source and specify how that source is handled by the controller.

The following code specifies how a GailBotController class is initialized and a GailBotSettings object is used to create a unique settings profile that then be applied to sources.


```
from gailbot.core import GailBotController, GailBotSettings

settings_dictionary = {
        "core": {},
        "plugins": {
            "plugins_to_apply": ["demoPlugin"]
        },
        "engines": {
            "engine_type": "watson",
            "watson_engine": {
                "watson_api_key": WATSON_API_KEY,
                "watson_language_customization_id": WATSON_LANG_CUSTOM_ID,
                "watson_base_language_model": WATSON_BASE_LANG_MODEL,
                "watson_region": WATSON_REGION,

            }
        }
    }

controller = GailBotController(WORKSPACE_DIRECTORY_PATH)
controller.create_new_settings_profile(
        "demo_profile", settings_dictionary)
```

In the above example, we first create a dictionary with key-value pairs that are required to create a GailBotSettings object. Note that "plugins_to_apply" is a list of plugin names that will be applied for that specific settings profile. Since GailBot currently supports IBM Watson STT, users must first create an [IBM Bluemix account](https://cloud.ibm.com/registration?target=catalog%3fcategory=watson&cm_mmc=Earned-_-Watson+Core+-+Platform-_-WW_WW-_-intercom&cm_mmca1=000000OF&cm_mmca2=10000409&). Next, a watson api key and region must be created with [IBM](https://cloud.ibm.com/catalog/services/speech-to-text) and specified in the settings profile.

With the settings dictionary specified, we create an instance of GailBotController, specifying a path to a directory that GailBot will use as a private workspace. Finally, we create a new settings profile called "demo_profile" with the values defined in the settings dictionary.


With the controller defined and at least one settings profile created, we are ready to transcribe a source as follows:

```

controller.add_source("demo_audio_source", <PATH TO AUDIO FILE>, <PATH TO RESULT DIRECTORY>)
controller. apply_settings_profile_to_source(
    "demo_audio_source","demo_profile")
assert controller.is_source_ready_to_transcribe("demo_audio_source)
controller.transcribe()
```


In the above code example, we first add an audio source to an instance of GailBotController, giving it a unique identifier, the path to the audio source, and a result directory. Next, we apply the settings profile created earlier to the audio source we added. We then verify that the settings profile has been correctly applied and that the audio source is ready to transcribe. Finally, we start the transcription process and wait for results in the  specified results directory.

### Custom Plugins


**NOTE**: This documentation is in progress and a more detailed version will be available soon!

A core GailBot feature is its ability to allow researchers to develop and add custom plugins that may be applied during the transcription process.

The following is an example of how a minimal plugin may be developed.

```
from typing import Dict, Any, List
# Local imports
from gailbot.plugins import GBPlugin, PluginMethodSuite, Utt


class CombineTurns(GBPlugin):

    def __init__(self) -> None:
        super().__init__()

    def apply_plugin(self, dependency_outputs: Dict[str, Any],
                     plugin_input: PluginMethodSuite) -> List[Utt]:
        # Combine all the utterances in the utterance map into a single
        # conversation.
        combined = list()
        turns_map: Dict[str, List[Utt]
                        ] = dependency_outputs["turn_construct"]
        for turns in turns_map.values():
            combined.extend(turns)
        combined.sort(key=lambda utt: utt.start_time_seconds)
        self.successful = True
        return combined
```


## Contribute

Users are encouraged to direct installation and usage questions, provide feedback, details regarding bugs, and development ideas by [email](mailto:hilab-dev@elist.tufts.edu).

## Acknowledgements

Special thanks to members of the [Human Interaction Lab](https://sites.tufts.edu/hilab/) at Tufts University and interns that have worked on this project.

## Cite

Users are encouraged to cite GailBot using the following BibTex:
```
@article{umair2022gailbot,
  title={GailBot: An automatic transcription system for Conversation Analysis},
  author={Umair, Muhammad and Mertens, Julia Beret and Albert, Saul and de Ruiter, Jan P},
  journal={Dialogue \& Discourse},
  volume={13},
  number={1},
  pages={63--95},
  year={2022}
}
```

## Liability Notice

Gailbot is a tool to be used to generate specialized transcripts. However, it
is not responsible for output quality. Generated transcripts are meant to
be first drafts that can be manually improved. They are not meant to replace
manual transcription.

GailBot may use external Speech-to-Text systems or third-party services. The
development team is not responsible for any transactions between users and these
services. Additionally, the development team does not guarantee the accuracy or correctness of any plugin. Plugins have been developed in good faith and we hope
that they are accurate. However, users should always verify results.

By using GailBot, users agree to cite Gailbot and the Tufts Human Interaction Lab
in any publications or results as a direct or indirect result of using Gailbot.
