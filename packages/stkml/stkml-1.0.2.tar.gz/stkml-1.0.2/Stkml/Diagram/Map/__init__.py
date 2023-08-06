#Copyright STACKEO - INRIA 2020 .
from abc import abstractmethod

from Stkml.Stkml import Stkml


class RegionsMap:

    def __init__(self, default_icons: str, icon_dir: str):
        self._icon_dir = icon_dir
        self.default_icons = default_icons

    @abstractmethod
    def from_stackml(self, stackml: Stkml, output: str):
        pass
