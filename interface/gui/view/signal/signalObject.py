'''
File: signalObject.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/18
Modified By:  Siara Small  & Vivian Li
-----
Description: Global Signal objects
'''

from .interface import (
    DataSignal, 
    SystemSignal, 
    StyleSignals, 
    TranscribeSignal, 
    FileDataSignal)


ProfileSignal     = DataSignal()
EngineSignal      = DataSignal()
PluginSignal      = DataSignal()
FileSignal        = FileDataSignal()
GBTranscribeSignal = TranscribeSignal()
GuiSignal         = SystemSignal()
GlobalStyleSignal = StyleSignals()