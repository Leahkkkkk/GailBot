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
from view.config import getWorkPaths

def clearAllLog():
    """ clear all the log file  """
    logdir = getWorkPaths().frontendLogFiles
    files = glob.iglob(os.path.join(logdir, "*.log"))
    for file in files:
        print(file)
        os.remove(file)
        
    backendDir = getWorkPaths().backendLogFiles
    for root, dirs, files in os.walk(backendDir):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))