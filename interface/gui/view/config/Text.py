'''
File: Text.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Wednesday, 9th November 2022 12:36:45 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

import os 
from .interface import TextParser
import toml 
from dataclasses import dataclass
from ..config.Style import Color
from config_frontend.ConfigPath import TextDataPath, FRONTEND_CONFIG_ROOT


text   = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.string))
forms  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.form))
about  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.about))


""" pages text data """
FileTableHeader          = TextParser.FiletableHeader.from_dict(text["filetable"]["header"])
WelcomePageText          = TextParser.WelcomePageTextData.from_dict(text["WelcomePageText"])
TranscribeProgressText   = TextParser.TranscribeProgressTextData.from_dict(text["TranscribeProgressText"])
TranscribeSuccessText    = TextParser.TranscribeSuccessTextData.from_dict(text["TranscribeSuccessText"])
FileUploadPageText       = TextParser.FileUploadPageTextData.from_dict(text["FileUploadPageText"])
RecordPageText           = TextParser.RecordPageTextData.from_dict(text["RecordPageText"])
ConfirmTranscribeText    = TextParser.ConfirmTranscribeTextData.from_dict(text["ConfirmTranscriptionPageText"])
RecordInProgressPageText = TextParser.RecordPageProgressData.from_dict(text["RecordInProgressPageText"])
ProfilePageText          = TextParser.ProfilePageTextData.from_dict(text["ProfilePageText"])
SystemSetPageText        = TextParser.SystemSetPageTextData.from_dict(text["SystemSettingPage"])
CreateNewProfilePageText = TextParser.CreateNewProfileTextData.from_dict(text["CreateNewProfilePageText"])
CreateNewProfileTabText  = TextParser.CreateNewProfileTabTextData.from_dict(text["CreateNewProfileTabText"])
ChooseFileTabText        = TextParser.ChooseFileTabTextData.from_dict(text["ChooseFileTabText"])
WindowTitle              = TextParser.WindowTitleData.from_dict(text["WindowTitle"])
MenuBarText              = TextParser.MenuBarText.from_dict(text["MenuBar"])
OutputFormatFormText     = TextParser.OutputFormatFormData.from_dict(text["OutputFormatForm"])

""" widgets text data """
BtnText           = TextParser.BtnText.from_dict(text["btnText"])
FileTableText     = TextParser.FileTableText.from_dict(text["fileTableText"])
MultipleComboText = TextParser.MultipleComboText.from_dict(text["multipleComboText"])
PopUpText         = TextParser.PopUpText.from_dict(text["popUpText"])
TableText         = TextParser.TableText.from_dict(text["tableText"])
MainStackText     = TextParser.MainStackTextData.from_dict(text["MainStackText"])
""" about data"""
About = TextParser.aboutData.from_dict(about["about"])


""" setting form data  """
ProfileSettingForm = TextParser.ProfileSettingData.from_dict(forms["profile form"])
PostSettingForm    = forms["profile form"]["PostTranscribe"]
RecordForm         = forms["record form"]
EngineSettingForm  = TextParser.EngineSetting.from_dict(forms["profile form"]["RequiredSetting"])
OutputFormatForm   = TextParser.OutputFormatSetting.from_dict(forms["profile form"]["RequiredSetting"]["Output Format"])
SystemSettingForm  = forms["system setting form"]
LogDeleteTimeDict  = forms["log deletion"]


@dataclass
class Links: 
    hilab_link = text["links"]["HILAB"]
    manual_link = text["links"]["USER_MANUAL"]
    guide_link = text ["links"]["GUIDE"]

    _linkTemplate    = "<a style='color:{0}; font-weight: 500;' href={1}>{2}</a>"
    tutorialLink     = _linkTemplate.format(Color.LINK, manual_link, WelcomePageText.tutorialText)
    guideLink        = _linkTemplate.format(Color.LINK, guide_link, WelcomePageText.guideText)
    gbWebLink        = _linkTemplate.format(Color.LINK, hilab_link, WelcomePageText.gbLinkText)
    guideLinkSideBar = _linkTemplate.format(Color.LINK, manual_link, WelcomePageText.tutorialText)




