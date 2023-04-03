from abc import ABC
class Request(ABC):
    data  = None
    def __init__() -> None:
        raise NotImplementedError
    def succeed(self, data):
        raise NotImplementedError
    def fail(self, msg: str):
        raise NotImplementedError