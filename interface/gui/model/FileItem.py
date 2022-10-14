'''
File: FileItem.py
Project: GailBot GUI
File Created: Sunday, 9th October 2022 10:41:00 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 9th October 2022 11:51:27 am
Modified By:  Siara Small  & Vivian Li
-----
'''

import datetime 
import os 


class FileItem:
    """ represent a file object """
    def __init__(self,fullPath:str, path:str, profile:str):
      self.path = path 
      self.profile = profile 
      self.fullPath = fullPath
      date = datetime.date.today()
      datestr = date.strftime("%m-%d-%y")
      fullName, extension = os.path.splitext(fullPath)
      pathArr = fullName.split("/")
      fileName = pathArr[- 1]
      self.name = f"{fileName}{extension}"
      self.type = extension 
      self.date = datestr 
      self.status = "Untranscribed"
      print(self.path, os.stat(fullPath).st_size)
      self.size = round(os.stat(fullPath).st_size/(1024**2), 2)
    
    def convertToData(self):
        """ convert the file data to a list which can be stored in the file
            table
        """
        return [ " ",
                 self.type, 
                 self.name, 
                 self.profile, 
                 self.status, 
                 self.date, 
                 f"{self.size}mb", 
                 " "]
      