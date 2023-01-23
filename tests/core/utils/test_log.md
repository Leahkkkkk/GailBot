# general.py 
**modified function after test failure** 
1. write_test() variable d was referenced before assignment 
2. write_yaml() variable previous_data was referenced before assignment 
3. get_extension() return the extension without ".", which is consistent with the file type in media.py
4. write_txt()  now reads a list of str and write to a file with each str on a separate line 
5. read_txt() now returns a list of str read from the txt 

**unsolved bug** 


# media.py
**modified function after test failure** 
1. static method is_supported needs to pass self as parameter when it is called in read_file() function
2. chunk method in media.py seems to check the chunk duration and the original segment duration in the opposite direction. It is changed to chunk duration should be smaller than the original segment 
3. add functions and some attributes to MediaHandler to make it consistent with the other AudioHandler and VideoHandler 
4. _SUPPORTED_FORMATS in VideoHandler is changed to a list of str instead of str 


**unsolved bug** 
1. change_volume function does not seem to change the volume
2. .opus format audio file does not pass the test for any function that need to read the audio stream 
