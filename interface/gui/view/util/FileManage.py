'''
File: FileManage.py
Project: GailBot GUI
File Created: Sunday, 4th December 2022 7:33:52 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 4th December 2022 7:34:56 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

import os
import glob
import shutil
from config_frontend import getWorkPath, getFileManagementData


def clearAllLog():
    """ clear all the log file  """
    logdir = getWorkPath().frontendLogFiles
    files = glob.iglob(os.path.join(logdir, "*.log"))
    for file in files:
        print(file)
        os.remove(file)
        
    backendDir = getWorkPath().backendLogFiles
    for root, dirs, files in os.walk(backendDir):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))