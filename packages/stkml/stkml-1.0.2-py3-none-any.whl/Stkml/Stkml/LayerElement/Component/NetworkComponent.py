#Copyright STACKEO - INRIA 2020 .
from Stkml.Stkml.LayerElement.Component import Component


class NetworkComponent(Component):

    def __init__(self, id_: str, c_type: str, id_ref: str):
        super().__init__(id_=id_, type_=c_type, id_ref=id_ref)
        self.value = None
