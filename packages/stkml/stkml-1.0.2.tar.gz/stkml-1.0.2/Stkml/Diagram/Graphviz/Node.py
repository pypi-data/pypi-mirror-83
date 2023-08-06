#Copyright STACKEO - INRIA 2020 .
from diagrams import Node

class DiagramNode(Node):

    def __init__(self, icon_dir, icon, label, quantity=0):
        self._icon_dir = icon_dir
        self._icon = f'{icon}.png'
        self.label = label
        if quantity and quantity > 1:
            self.label = f'{quantity}\n{self.label}'
        super().__init__(self.label)
