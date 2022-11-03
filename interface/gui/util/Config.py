from util import Adapter
import toml 
from dataclasses import dataclass


config = toml.load("controller/interface.toml")

""" style data """
Color = Adapter.ColorData.from_dict(config["style"]["colors"])
FontSize = Adapter.FontSizeData.from_dict(config["style"]["fontSizes"])
Dimension = Adapter.DimensionData.from_dict(config["style"]["dimension"])
StyleSheet = Adapter.styleSheet.from_dict(config["style"]["styleSheet"])
Asset = Adapter.asset.from_dict(config["asset"])
FileTableHeader = Adapter.filetableHeader.from_dict(config["filetable"]["header"])
FileTableDimension = Adapter.fileTableDimension.from_dict(config["filetable"]["dimension"])


""" text data """
WelcomePageText = Adapter.WelcomePageTextData.from_dict(
    config["text"]["WelcomePageText"])
TranscribeProgressText = Adapter.TranscribeProgressTextData.from_dict(
    config["text"]["TranscribeProgressText"])
TranscribeSuccessText = Adapter.TranscribeSuccessTextData.from_dict(
    config["text"]["TranscribeSuccessText"])
FileUploadPageText = Adapter.FileUploadPageTextData.from_dict(
    config["text"]["FileUploadPageText"])
RecordPageText = Adapter.RecordPageTextData.from_dict(
    config["text"]["RecordPageText"])
ConfirmTranscribeText = Adapter.ConfirmTranscribeTextData.from_dict(
    config["text"]["ConfirmTranscriptionPageText"])

RecordInProgressPageText = Adapter.RecordPageProgressData.from_dict(
    config["text"]["RecordInProgressPageText"])
ProfilePageText = Adapter.ProfilePageTextData.from_dict(
    config["text"]["ProfilePageText"])
SystemSetPageText = Adapter.SystemSetPageTextData.from_dict(
    config["text"]["SystemSettingPage"])
CreateNewProfilePageText = Adapter.CreateNewProfileTextData.from_dict(
    config["text"]["CreateNewProfilePageText"])
BtnText = Adapter.btnText.from_dict(
    config["text"]["btnText"])

""" about data"""
About = Adapter.aboutData.from_dict(config["about"])


""" setting form data  """
ProfileSettingForm = Adapter.ProfileSettingData.from_dict(config["profile form"])
PostSettingForm = config["profile form"]["PostTranscribe"]
EngineSettingForm = Adapter.EngineSetting.from_dict(
    config["profile form"]["RequiredSetting"])
OutputFormatForm = Adapter.OutputFormatSetting.from_dict(
    config["profile form"]["RequiredSetting"]["Output Format"])
SystemSettingForm = config["system setting form"]


@dataclass
class Links: 
    link = config["text"]["links"]["HILAB"]
    _linkTemplate = "<a href={0}>{1}</a>"
    tutorialLink = _linkTemplate.format(
        link, WelcomePageText.tutorialText)
    guideLink = _linkTemplate.format(
        link, WelcomePageText.guideText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.gbLinkText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.guideText)




