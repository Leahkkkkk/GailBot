from util import Adapter
import toml 
from dataclasses import dataclass

config = toml.load("config/style.toml")
text   = toml.load("config/text.toml")
forms  = toml.load("config/forms.toml")
about  = toml.load("config/about.toml")
assets = toml.load("config/assets.toml")

""" style data """
Color = Adapter.ColorData.from_dict(config["style"]["colors"])
FontSize = Adapter.FontSizeData.from_dict(config["style"]["fontSizes"])
Dimension = Adapter.DimensionData.from_dict(config["style"]["dimension"])
StyleSheet = Adapter.StyleSheet.from_dict(config["style"]["styleSheet"])
Asset = Adapter.Asset.from_dict(assets["asset"])
FileTableHeader = Adapter.FiletableHeader.from_dict(forms["filetable"]["header"])
FileTableDimension = Adapter.FileTableDimension.from_dict(forms["filetable"]["dimension"])
FontFamily = Adapter.FontFamilyData.from_dict(config["style"]["fontFamily"])

""" pages text data """
WelcomePageText = Adapter.WelcomePageTextData.from_dict(
    text["text"]["WelcomePageText"])
TranscribeProgressText = Adapter.TranscribeProgressTextData.from_dict(
    text["text"]["TranscribeProgressText"])
TranscribeSuccessText = Adapter.TranscribeSuccessTextData.from_dict(
    text["text"]["TranscribeSuccessText"])
FileUploadPageText = Adapter.FileUploadPageTextData.from_dict(
    text["text"]["FileUploadPageText"])
RecordPageText = Adapter.RecordPageTextData.from_dict(
    text["text"]["RecordPageText"])
ConfirmTranscribeText = Adapter.ConfirmTranscribeTextData.from_dict(
    text["text"]["ConfirmTranscriptionPageText"])
RecordInProgressPageText = Adapter.RecordPageProgressData.from_dict(
    text["text"]["RecordInProgressPageText"])
ProfilePageText = Adapter.ProfilePageTextData.from_dict(
    text["text"]["ProfilePageText"])
SystemSetPageText = Adapter.SystemSetPageTextData.from_dict(
    text["text"]["SystemSettingPage"])
CreateNewProfilePageText = Adapter.CreateNewProfileTextData.from_dict(
    text["text"]["CreateNewProfilePageText"])
CreatNewProfileTabText = Adapter.CreateNewProfileTabTextData.from_dict(
    text["text"]["CreateNewProfileTabText"]
)
ChooseFileTabText = Adapter.ChooseFileTabTextData.from_dict(
    text["text"]["ChooseFileTabText"]
)
WindowTitle = Adapter.WindowTitleData.from_dict(
    text["text"]["WindowTitle"]
)
MenuBarText = Adapter.MenuBarText.from_dict(
    text["text"]["MenuBar"]
)
OutputFormatFormText = Adapter.OutputFormatFormData.from_dict(
    text["text"]["OutputFormatForm"]
)

""" widgets text data """
BtnText = Adapter.BtnText.from_dict(text["text"]["btnText"])
FileTableText = Adapter.FileTableText.from_dict(text["text"]["fileTableText"])
MultipleComboText = Adapter.MultipleComboText.from_dict(text["text"]["multipleComboText"])
PopUpText = Adapter.PopUpText.from_dict(text["text"]["popUpText"])
TableText = Adapter.TableText.from_dict(text["text"]["tableText"])
MainStackText = Adapter.MainStackTextData.from_dict(text["text"]["MainStackText"])
""" about data"""
About = Adapter.aboutData.from_dict(about["about"])


""" setting form data  """
ProfileSettingForm = Adapter.ProfileSettingData.from_dict(forms["profile form"])
PostSettingForm = forms["profile form"]["PostTranscribe"]
EngineSettingForm = Adapter.EngineSetting.from_dict(
    forms["profile form"]["RequiredSetting"])
OutputFormatForm = Adapter.OutputFormatSetting.from_dict(
    forms["profile form"]["RequiredSetting"]["Output Format"])
SystemSettingForm = forms["system setting form"]


@dataclass
class Links: 
    link = text["text"]["links"]["HILAB"]
    _linkTemplate = "<a href={0}>{1}</a>"
    tutorialLink = _linkTemplate.format(
        link, WelcomePageText.tutorialText)
    guideLink = _linkTemplate.format(
        link, WelcomePageText.guideText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.gbLinkText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.guideText)




