'''
File: Request.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/18
Modified By:  Siara Small  & Vivian Li
-----
Description: Request interface that will be accepted by the controller
'''
from view.widgets.MsgBox import WarnBox

class Request:
    def __init__(self, data, succeed: callable = None) -> None:
        self.data = data
        self.succeed = succeed
    
    def fail(self, msg: str):
        WarnBox(msg)