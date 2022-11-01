from dataclasses import dataclass

@dataclass
class ErrorMsg:
    KEYERROR = "File key not found"
    DUPLICATEKEY = "Duplicate key"
    POSTERROR = "Fail to add to database"
    GETERROR = "Fail to get data"
    EDITERROR = "Fail to edit the data"
    DELETEEROR = "Unable to delete dat"

class DBExecption(Exception):
    def __init__(self, msg = None):
        self.msg = msg