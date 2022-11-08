from util import TextParser
import toml 
from dataclasses import dataclass

text   = toml.load("config/text/text.toml")
forms  = toml.load("config/text/forms.toml")
about  = toml.load("config/text/about.toml")


""" pages text data """
FileTableHeader = TextParser.FiletableHeader.from_dict(
    text["filetable"]["header"])
WelcomePageText = TextParser.WelcomePageTextData.from_dict(
    text["WelcomePageText"])
TranscribeProgressText = TextParser.TranscribeProgressTextData.from_dict(
    text["TranscribeProgressText"])
TranscribeSuccessText = TextParser.TranscribeSuccessTextData.from_dict(
    text["TranscribeSuccessText"])
FileUploadPageText = TextParser.FileUploadPageTextData.from_dict(
    text["FileUploadPageText"])
RecordPageText = TextParser.RecordPageTextData.from_dict(
    text["RecordPageText"])
ConfirmTranscribeText = TextParser.ConfirmTranscribeTextData.from_dict(
    text["ConfirmTranscriptionPageText"])
RecordInProgressPageText = TextParser.RecordPageProgressData.from_dict(
    text["RecordInProgressPageText"])
ProfilePageText = TextParser.ProfilePageTextData.from_dict(
    text["ProfilePageText"])
SystemSetPageText = TextParser.SystemSetPageTextData.from_dict(
    text["SystemSettingPage"])
CreateNewProfilePageText = TextParser.CreateNewProfileTextData.from_dict(
    text["CreateNewProfilePageText"])
CreatNewProfileTabText = TextParser.CreateNewProfileTabTextData.from_dict(
    text["CreateNewProfileTabText"]
)
ChooseFileTabText = TextParser.ChooseFileTabTextData.from_dict(
    text["ChooseFileTabText"]
)
WindowTitle = TextParser.WindowTitleData.from_dict(
    text["WindowTitle"]
)
MenuBarText = TextParser.MenuBarText.from_dict(
    text["MenuBar"]
)
OutputFormatFormText = TextParser.OutputFormatFormData.from_dict(
    text["OutputFormatForm"]
)

""" widgets text data """
BtnText = TextParser.BtnText.from_dict(text["btnText"])
FileTableText = TextParser.FileTableText.from_dict(text["fileTableText"])
MultipleComboText = TextParser.MultipleComboText.from_dict(text["multipleComboText"])
PopUpText = TextParser.PopUpText.from_dict(text["popUpText"])
TableText = TextParser.TableText.from_dict(text["tableText"])
MainStackText = TextParser.MainStackTextData.from_dict(text["MainStackText"])
""" about data"""
About = TextParser.aboutData.from_dict(about["about"])


""" setting form data  """
ProfileSettingForm = TextParser.ProfileSettingData.from_dict(forms["profile form"])
PostSettingForm = forms["profile form"]["PostTranscribe"]
RecordForm = forms["record form"]
EngineSettingForm = TextParser.EngineSetting.from_dict(
    forms["profile form"]["RequiredSetting"])
OutputFormatForm = TextParser.OutputFormatSetting.from_dict(
    forms["profile form"]["RequiredSetting"]["Output Format"])
SystemSettingForm = forms["system setting form"]


@dataclass
class Links: 
    link = text["links"]["HILAB"]
    _linkTemplate = "<a href={0}>{1}</a>"
    tutorialLink = _linkTemplate.format(
        link, WelcomePageText.tutorialText)
    guideLink = _linkTemplate.format(
        link, WelcomePageText.guideText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.gbLinkText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.guideText)




