from view.widgets.MsgBox import WarnBox

class Request:
    def __init__(self, data, succeed: callable = None) -> None:
        self.data = data
        self.succeed = succeed
    
    def fail(self, msg: str):
        WarnBox(msg)