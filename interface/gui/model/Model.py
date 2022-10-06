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
      self.SettingModel = SettingModel.SettingModel()