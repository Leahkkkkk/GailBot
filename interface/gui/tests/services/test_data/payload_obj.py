from gailbot.services.converter.payload.conversationDirectoryPayload import ConversationDirectoryPayload, load_conversation_dir_payload
from gailbot.services.converter.payload.transcribedDirPayload import TranscribedDirPayload, load_transcribed_dir_payload
from gailbot.services.converter.payload.audioPayload import AudioPayload, load_audio_payload    
# create Audio payload
from ..test_data import SETTING_DATA, AudioPath, PATH
from gailbot.services.organizer.source import SourceObject, SourceManager
from gailbot.services.organizer.settings import SettingObject
from gailbot.workspace.manager import WorkspaceManager
from gailbot.core.utils.general import get_name
from dataclasses import dataclass
TEST_SETTING = SettingObject (SETTING_DATA.PROFILE, "test_setting")
ws_manager = WorkspaceManager(PATH.USER_ROOT)
audio_source = SourceObject(AudioPath.MEDIUM_AUDIO, get_name(AudioPath.MEDIUM_AUDIO), output=AudioPath.RESULT_OUTPUT)
audio_source.apply_setting(TEST_SETTING)
audio_payload: AudioPayload = load_audio_payload(audio_source, ws_manager)[0]

# create the directory payload 
dir_source = SourceObject(AudioPath.CONVERSATION_DIR, get_name(AudioPath.CONVERSATION_DIR), AudioPath.RESULT_OUTPUT)
dir_source.apply_setting(TEST_SETTING)
dir_payload: ConversationDirectoryPayload = load_conversation_dir_payload(dir_source, ws_manager)[0]


# transcribed directory output 
trans_dir_source = SourceObject(PATH.TRANSCRIBED, get_name(PATH.TRANSCRIBED),AudioPath.RESULT_OUTPUT)
trans_dir_source.apply_setting(TEST_SETTING)
trans_dir_payload: TranscribedDirPayload = load_transcribed_dir_payload(trans_dir_source, ws_manager)[0]


@dataclass
class PAYLOAD_OBJ:
    AUDIO: AudioPayload = audio_payload
    CON_DIR: ConversationDirectoryPayload = dir_payload
    TRAN_DIR: TranscribedDirPayload = trans_dir_payload 