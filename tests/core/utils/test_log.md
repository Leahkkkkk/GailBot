# general.py 
**modified function after test failure** 
1. write_test() variable d was referenced before assignment 
2. write_yaml() variable previous_data was referenced before assignment 
3. get_extension() return the extension without ".", which is consistent with the file type in media.py

**unsolved bug** 
1. write_txt & read_txt()
    - the output type of read_txt is str instead of list
    - when the input type of the write_txt() is list, the list is casted to string as a raw string with list format

# media.py
**modified function after test failure** 
1. static method is_supported needs to pass self as parameter when it is called in read_file() function
2. chunk method in media.py seems to check the chunk duration and the original segment duration in the opposite direction. It is changed to chunk duration should be smaller than the original segment 
3. add functions and some attributes to MediaHandler to make it consistent with the other AudioHandler and VideoHandler 
4. _SUPPORTED_FORMATS in VideoHandler is changed to a list of str instead of str 


**unsolved bug** 
1. change_volume function does not seem to change the volume
2. .opus format audio file does not pass the test for any function that need to read the audio stream 
