#! /bin/bash
# shell script to use requirements.txt to create a venv virtual environment 
# this is an alternative to using conda environment
python -m venv gb-dev
source gb-dev/bin/activate
pip install -r requirements.txt
pip install --upgrade soundfile   
 # the newest sound file has a fix for arm64 , 
 # but it conflicts with pyannote.audio, so has to be installed separately     
 # related github issue https://github.com/ohmtech-rdi/eurorack-blocks/issues/444
