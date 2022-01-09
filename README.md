# GailBot

## About

Researchers studying human interaction, such as conversation analysts, psychologists, and linguists all rely on detailed transcriptions of language use. Ideally, these should include so-called paralinguistic features of talk, such as overlaps, prosody, and intonation, as they convey important information. However, transcribing these features by hand requires substantial amounts of time by trained transcribers. There are currently no Speech to Text (STT) systems that are able to annotate these features. To reduce the resources needed to create transcripts that include paralinguistic features, we developed a program called GailBot. GailBot combines STT services with plugins to automatically generate first drafts of conversation analytic transcripts. It also enables researchers to add new plugins to transcribe additional features, or to improve the plugins it currently uses. We argue that despite its limitations, GailBot represents a substantial improvement over existing dialogue transcription software.

## Status

GailBot version: 1.0.0

Supported OS: MacOs 11.6, Ubuntu 20.04

Release type: API

Plugin suites provided: rel_ca_0.0.1

## Installation

The root directory has the following structure:

```
|-- README.md
|-- Env/
    |-- docker-compose.yml
    |-- Dockerfile
    |-- quartz.sh
    |-- requirements.txt
    |-- start.sh
|-- Plugins/*
|-- Src
    |-- components/*
    |--  __init__.py
```

GailBot can be installed natively or using Docker.

### Docker

To install using Docker, ensure the [Docker engine](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) are installed.

Install and execute a docker container:

```
- cd ./Env
- docker-compose build
- docker-compose up -d
- docker exec -it gailbot /bin/bash
```

Note that the above will build and execute a docker image before opening an interactive session with the docker container. It will also mount the root directory as a volume i.e., changes in the root directory will be reflected inside the docker container.

### Native Installation

To install natively, we recommend first installing conda and creating an environment specific for GailBot.

To install program dependencies, execute the following:

```
pip install \
    pyaudio \
    ffmpeg
pip install -r ./Env/requirements.txt
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
