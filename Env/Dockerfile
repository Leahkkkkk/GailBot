#### Dockerfile for GailBot 0.3

# Base OS
FROM ubuntu:20.04

WORKDIR /root

ARG DEBIAN_FRONTEND=noninteractive

# Install necessary software for the installation of ROS2
RUN apt-get update && apt-get install -y \
                      locales \
                      curl \
                      gnupg2 \
                      lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*rm

# Setup of the locale
RUN locale-gen ja_JP ja_JP.UTF-8 \
    && update-locale LC_ALL=ja_JP.UTF-8 LANG=ja_JP.UTF-8 \
    && export LANG=ja_JP.UTF-8

# Installing python dpendencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python-dev

# Copy the requirements file 
COPY requirements.txt /tmp/requirements.txt

# Installing pip dependencies from requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Installng pyaduio and portaudio and ffmpeg 
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install \
    pyaudio \
    ffmpeg 


# Entrypoint
CMD ["bash"]
