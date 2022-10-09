import datetime 
import os 


class FileItem:
    def __init__(self,fullPath:str,path:str, profile:str):
      self.path = path 
      self.profile = profile 
      date = datetime.date.today()
      datestr = date.strftime("%m-%d-%y")
      fullName, extension = os.path.splitext(fullPath)
      pathArr = fullName.split("/")
      fileName = pathArr[- 1]
      self.name = fileName
      self.type = extension 
      self.date = datestr 
      self.status = "Untranscribed"
      self.size = round(os.stat(self.path).st_size/(1024**2),2)
    
    def convertToData(self):
        return [self.type, 
                 self.name, 
                 self.profile, 
                 self.status, 
                 self.date, 
                 f"{self.size}mb", 
                 " "]
      