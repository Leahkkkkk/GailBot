'''
File: Model.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 9:48:10 am
Modified By:  Siara Small  & Vivian Li
-----
'''


from model import FileModel
from model import SettingModel 

class Model():
    """ stores the data, has two fields: 
        1.FileModel: stores file data 
        2.SettingModel: stores the setting data
    """
    def __init__(self):
      self.FileModel = FileModel.FileModel()
      self.ConfirmFileModel = FileModel.ConfirmFileModel()
      self.ProcessingFileModel = FileModel.ProgressFileMode()
      self.SuccessedFileMode = FileModel.SuccessFileModel()
      self.SettingModel = SettingModel.SettingModel()
      self.FileData = dict()
    #   self.FileData = {
    #         "1": {
    #             "Name": "hello.wav",
    #             "Type": "🔈",
    #             "Profile":"Coffee Study",
    #             "Status": "Not Transcribed",
    #             "Date": "10-13-22",
    #             "Size":"135.26kb",
    #             "Output": "/Users/yike/Desktop/",
    #             "FullPath": "/Users/yike/Desktop/hello.wav",
    #         },
    #     }
      
      
      