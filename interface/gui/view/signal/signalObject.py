from .interface import DataSignal, ViewSignals, StyleSignals, FileSignals, TranscribeSignal 

ProfileSignal     = DataSignal()
EngineSignal      = DataSignal()
PluginSignal      = DataSignal()
FileSignal        = DataSignal()
GBTranscribeSignal = TranscribeSignal()
GuiSignal         = ViewSignals()
GlobalStyleSignal = StyleSignals()
# FileSignal        = FileSignals()