from view.config.Text import ProfilePageText as Text
from view.signal.interface import DataSignal
from view.util.ErrorMsg import ERR  
from ..SettingConfig import EditProfile
from ..SettingDetail import ProfileDetail
from view.widgets.Table import BaseTable

class ProfileTable(BaseTable):
    def __init__(self, signal: DataSignal, engineSignal, parent):
        super().__init__(Text.tableHeader)
        self.signal = signal
        self.engineSignal = engineSignal
        self.parent = parent
        self.resizeCol(Text.tableDimension)
        self.dataKeyToCol = {"engine_setting_name": 1,
                             "plugin_setting": 2}
    
    def openEditDialog(self, data):
        editDialog = EditProfile(data, 
                                 self.parent.availableEngineSettings, 
                                 self.parent.availablePluginSettings,
                                 self.engineSignal)
        editDialog.signals.editProfile.connect(self.sendEditRequest)
        editDialog.exec()
    
    def displayDetail(self, data):
        name, setting = data 
        ProfileDetail(name, setting)
        