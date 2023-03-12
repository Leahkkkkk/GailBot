'''
File: main.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:19:06 am
Modified By:  Siara Small  & Vivian Li
-----
Description: main driver for a GUI app that support front and interface to 
             allow user transcribe file using gailbot 
'''

import hooks
import ssl
import os 

if __name__ == '__main__':
    # add project path to program environment path
    # this is added for the packaged app to be able to tun binary file ffmpeg 
    os.environ["PATH"] += os.pathsep + os.path.dirname(__file__)
    print(os.path.dirname(__file__))
    ssl._create_default_https_context = ssl._create_unverified_context
    
    import multiprocessing
    multiprocessing.freeze_support()
    from multiprocessing import Process, Queue
    from controller.Driver import run 
    
    EXIT_CODE_REBOOT = -20000
    exitCodeQueue = Queue()
    exitCode = EXIT_CODE_REBOOT   
    while exitCode == EXIT_CODE_REBOOT:
        process = Process(target = run, args = (exitCodeQueue,))
        process.start()
        exitCode = exitCodeQueue.get()
        process.join()
        del process
    
