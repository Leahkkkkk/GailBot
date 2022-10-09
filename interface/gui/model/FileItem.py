import datetime 
import os 


class FileItem:
    def __init__(self,fullPath:str,profile:str):
      date = datetime.date.today()
      datestr = date.strftime("%m-%d-%y")
      fullName, extension = os.path.splitext(fullPath)
      path_arr = fullName.split("/")
      filename = path_arr[- 1]
      self.name = filename
      self.type = extension 
      self.profile = profile 
      self.path = fullPath 
      self.date = datestr 
      self.status = "Untranscribed"
      self.size = round(os.stat(self.path).st_size/(1024**2),2)
    
    def convertToData(self):
        return [[self.type, 
                 self.name, 
                 self.profile, 
                 self.status, 
                 self.date, 
                 f"{self.size}mb", 
                 " "]]
      