#### Dockerfile for GailBot 0.3

# Base OS
FROM ubuntu:20.04


# Setup of the locale
RUN locale-gen ja_JP ja_JP.UTF-8 \
    && update-locale LC_ALL=ja_JP.UTF-8 LANG=ja_JP.UTF-8 \
    && export LANG=ja_JP.UTF-8

# Installing python dpendencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python-dev

# Installing pip dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Entrypoint
CMD ["bash"]
