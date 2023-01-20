# general.py 
**modified function after test failure** 
1. write_test() variable d was referenced before assignment 
2. write_yaml() variable previous_data was referenced before assignment 
3. get_extension() return the extension without ".", which is consistent with 
   the file type in media.py

**unsolved bug** 
1. write_txt & read_txt()
    - the output type of read_txt is str instead of list
    - when the input type of the write_txt() is list, the list is casted to string as a raw string with list format

# media.py
**modified function after test failure** 
1. static method is_supported needs to pass self as parameter when it is called in read_file() function
**unsolved bug** 
1. change_volume function does not seem to change the volume
2. stereo_to_mono function does not return a list with two audio segment; with some tracing, the split_to_mono ()  function under the AudioSegment class does not return a list with two audio segments