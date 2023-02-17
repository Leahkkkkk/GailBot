class TrancrcibeComponent(Component):
    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError()