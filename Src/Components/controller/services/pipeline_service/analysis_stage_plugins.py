# Standard library imports
from abc import abstractmethod
# Local imports
from ....analyzer import Plugin

class AnalysisPlugins(Plugin):

    @abstractmethod
    def apply_plugin(self) -> None:
        pass

    @abstractmethod
    def was_successful(self) -> bool:
        pass


