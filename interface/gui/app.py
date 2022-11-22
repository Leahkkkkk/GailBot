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


if __name__ == '__main__':
    
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
    
