#Copyright STACKEO - INRIA 2020 .
from abc import abstractmethod

from Stkml.Stkml import Stkml


class Graphviz:

    def __init__(self, default_icons: str, icon_dir: str, diagram_attr: dict):
        self._icon_dir = icon_dir
        self.default_icons = default_icons
        self.diagram_attr = diagram_attr

    @abstractmethod
    def from_stackml(self, stackml: Stkml, output: str) -> str:
        return 'Ok'
