from payload import PayLoadObject

class Loader: 
    def __init__(self) -> None:
        raise NotImplementedError 
    
    def load_source(self, source) -> PayLoadObject:
        raise NotImplementedError