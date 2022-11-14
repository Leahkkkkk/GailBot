'''
File: Path.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 3:19:10 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: provides function  to get the project root path
'''

import os

dir = os.path.dirname(os.path.dirname(__file__))

def getProjectRoot() -> str:
    """return the root path of the program """
    dir = os.path.dirname(os.path.dirname(__file__))

    return dir
print(getProjectRoot())




