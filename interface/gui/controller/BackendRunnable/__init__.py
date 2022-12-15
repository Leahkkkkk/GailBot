""" QRunnable Object That can be run on separate thread 
    able to send thread safe messages through QSignal
    
    DummyRunnable:
        use time.sleep function 
        for testing 
        
    GBRunnable:
        run actual gailbot function
        args:
            @filename: str
            @filepath: str
            @key: int

"""