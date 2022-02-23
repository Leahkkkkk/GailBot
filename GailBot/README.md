# GailBot

## About

Researchers studying human interaction, such as conversation analysts, psychologists, and linguists all rely on detailed transcriptions of language use. Ideally, these should include so-called paralinguistic features of talk, such as overlaps, prosody, and intonation, as they convey important information. However, transcribing these features by hand requires substantial amounts of time by trained transcribers. There are currently no Speech to Text (STT) systems that are able to annotate these features. To reduce the resources needed to create transcripts that include paralinguistic features, we developed a program called GailBot. GailBot combines STT services with plugins to automatically generate first drafts of conversation analytic transcripts. It also enables researchers to add new plugins to transcribe additional features, or to improve the plugins it currently uses. We argue that despite its limitations, GailBot represents a substantial improvement over existing dialogue transcription software.

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

This is a python API only release i.e., users will import relevant components from the Src directory into custom python scripts.

**NOTE**: Currently, API documentation is only provided in the corresponding python files.

## Contribute

Users are encouraged to provide feedback, details regarding bugs, and development ideas by [email](mailto:hilab-dev@elist.tufts.edu).

## Acknowledgements

Special thanks to members of the[Human Interaction Lab](https://sites.tufts.edu/hilab/) at Tufts University and interns working on this project.

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
