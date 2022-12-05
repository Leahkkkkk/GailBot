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

import time
import os
import glob

from util.GailBotData import getWorkPath, FileManage


def clearLog():
    """ clear the log that is  """
    currentTime = int(time.time())
    deleteTime = currentTime - FileManage.AUTO_DELETE_TIME * 24 * 60 * 60
    logdir = getWorkPath().logFiles
    files = glob.iglob(os.path.join(logdir, "*.log"))
    for file in files:
        fileTime = int(os.path.getctime(file))
        if fileTime <= deleteTime :
            os.remove(file)

def clearAllLog():
    logdir = getWorkPath().logFiles
    files = glob.iglob(os.path.join(logdir, "*.log"))
    for file in files:
        os.remove(file)