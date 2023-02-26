from ..test_data import PAYLOAD_OBJ
from gailbot.services.pipeline.components.transcribeComponent import TranscribeComponent
import pytest

def test_transcribe():
    component = TranscribeComponent()
    dependency = {"base":[PAYLOAD_OBJ.AUDIO]}
    component(dependency_output=dependency)

def test_transcribe_dir():
    component = TranscribeComponent()
    dependency = {"base":[PAYLOAD_OBJ.CON_DIR]}
    component(dependency_output=dependency)
    
def test_multiple_transcribe():
    component = TranscribeComponent()
    dependency = {"base": [PAYLOAD_OBJ.AUDIO, PAYLOAD_OBJ.CON_DIR, PAYLOAD_OBJ.TRAN_DIR]}
    component(dependency_output=dependency)
    
def test_transcribed_dir():
    component = TranscribeComponent()
    dependency = {"base":[PAYLOAD_OBJ.TRAN_DIR]}
    component(dependency_output=dependency)