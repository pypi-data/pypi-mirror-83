#Copyright STACKEO - INRIA 2020 .
import os
from typing import List
import copy
import json

import requests
from jinja2 import Environment, Template


import jsonschema
from jsonschema import validate
import yaml
from yaml.scanner import ScannerError

from Stkml import STACKML_URL_SCHEMA, MODULE_DIR
from Stkml.Stkml.LayerElement import Component
from Stkml.Stkml.ModelException import ModelException

from Stkml.Stkml.Region import Region
from Stkml.Stkml.StkmlSyntaxicError import StkmlSyntaxicError
from Stkml.Stkml.StkmlSyntaxicErrorList import StkmlSyntaxicErrorList
from Stkml.Stkml.Tier import Tier
from Stkml.Stkml.Link import Link
from Stkml.Stkml.Node import Node
from Stkml.Stkml.Topology import Topology
from Stkml.Stkml.WarningList import WarningList


class Stkml:

    def __init__(self, folder=None):
        self.stackmlfile = None
        if folder:
            self.stackmlfile = os.path.join(folder, 'main.stkml.yaml')
        self.tiers: List[Tier] = []
        self.links: List[Link] = []
        self.regions: List[Region] = []
        self.topology = Topology()
        self.schema = self.get_stackml_schema()
        self.errors = []
        self.libraries = {}

    def check_file(self, file) -> dict or ScannerError:
        stackml_yaml = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return stackml_yaml

    def get_library(self, file):#-> FileNotFoundError or str
        try:
            stackml_file = open(file, 'r')
        except FileNotFoundError:
            file = file.split('/')[-1]
            file = os.path.join(MODULE_DIR, 'templates', 'Stackml', file)
            print(file)
            try:
                stackml_file = open(file, 'r')
            except FileNotFoundError as error:
                raise FileNotFoundError(f'\nThe {file.split("/")[-1].split(".")[0]} library does not exist') from error
        return stackml_file

    def get_stackml_schema(self) -> dict or None:
        try:
            schema = None
            request = requests.get(STACKML_URL_SCHEMA)
        except requests.exceptions.ConnectionError :
            pass
        else:
            if request.status_code == 200:
                schema = json.loads(request.content.decode("utf-8"))
            request.close()
            return schema
    def validate_schema(self, file) -> dict or Exception:
        with open(file, 'r') as file_:
            file_ = yaml.load(file_, Loader=yaml.FullLoader)
            try:
                validate(file_, self.schema)
            except jsonschema.exceptions.ValidationError:
                self.errors.append(StkmlSyntaxicError(self.schema, file_, file))
            return file_


    def check_stackml_project(self) -> str or ScannerError:
        file = self.get_library(self.stackmlfile)
        stackml = self.check_file(file)
        path = os.path.dirname(self.stackmlfile)
        i = 0
        for import_ in (stackml.get('import') or []):
            imports = os.path.join(path, f'{import_}.stkml.yaml')
            imports_ = self.get_library(imports)
            self.libraries[import_] = imports_.name
            self.check_file(imports_)
            i += 1
        file.close()

    def validate_stackml_project(self) -> str or StkmlSyntaxicErrorList or None:
        if self.schema:
            stackml = self.validate_schema(self.stackmlfile)
            for import_ in (stackml.get('import') or []):
                self.validate_schema(self.libraries[import_])
            if len(self.errors) > 0:
                raise StkmlSyntaxicErrorList(self.errors)
            return None
        return 'Stackml schema does not found please verify your connection'

    def add_tier(self, tier_type: str) -> Tier:
        for tier in self.tiers:
            if tier.type == tier_type:
                return tier
        tier = Tier(name=tier_type, type_=tier_type)
        self.tiers.append(tier)
        return tier

    def create_architecture(self):
        with open(self.stackmlfile, 'r') as stackml_file:
            stackml = yaml.load(stackml_file, Loader=yaml.FullLoader)
            topology = stackml['topology']
            self.topology.name = topology.get('name')
            self.topology.usecase = topology.get('useCase')
            self.topology.type = topology.get('type')
            nodes = topology.get('Nodes')
            if nodes:
                self.create_tiers(nodes)
            links = topology.get('Links')
            if links:
                self.create_links(links)
            regions = topology.get('Regions')
            if regions:
                self.create_regions(regions)


    def create_regions(self, regions) -> None:
        for region in regions:
            region_ = Region(name=region.get('name'), type_=region.get('type'))
            for node in region.get('NodePopulation'):
                region_.add_node(node_id=node.get('nodeId'), number=node.get('number'))
            self.regions.append(region_)

    def create_links(self, links) -> None:
        for link in links:
            source = link.get('source')
            sink = link.get('sink')
            self.links.append(Link(source=source, sink=sink,
                                   layer=link.get('layer'), secure=link.get('secure')))
    def get_node_model(self, model_name):
        node = None
        if '.' in model_name:#extrenel model

            model = model_name.split('.')
            file = self.libraries.get(model[0])
            if file:
                with open(file, 'r') as s_file:
                    model_def = self.check_file(s_file)
                node_id = model[1]
            else:
                raise ModelException(msg=f'{model[0]} is not imported')
        else:#internal model
            file = self.stackmlfile
            with open(file, 'r') as s_file:
                model_def = self.check_file(s_file)
            node_id = model_name
        model_def = model_def.get('modeldef')
        if model_def:
            model_def = model_def.get('NodeModels')
            if model_def:
                for node_def in model_def:
                    if node_def.get('name') == node_id:
                        node = node_def
                        break
            else:
                raise ModelException(msg=f'The are no NodeModels on {file}')
        else:
            raise ModelException(msg=f'The are no modeldef for {node_id}')
        if not node:
            raise ModelException(msg=f'The {node_id} model does not exist on {file}')
        return node


    def create_tiers(self, nodes) -> None:
        #warnings = []
        for node in nodes:
            model = node.get('model')
            node_def = self.get_node_model(model)
            node_type = node_def.get('technology')
            tier = node.get('tier')
            #if tier not in node_type:
            #    warnings.append(f"you are using {node_type} in {tier} Tier")
            tier = self.add_tier(tier)
            node_ = tier.add_node(id_=node.get('id'), type_=node_type,
                                  cardinality=node.get('cardinality'))
            node_.set_nature(node_def.get('nature'))
            for layer in node_.element_types:
                elem = node_def.get(layer)
                if elem:
                    hub = elem[0].get('ElementType')
                    if not hub:
                        hub = 'EndPoint'
                    else:
                        elem = elem[1:]
                    layer_elem = node_.add_layer_element(layer, type_=layer, hub=hub)
                    layer_elem.set_components(elem)
        self.sort_tiers()
        #return warnings

    def generate_files(self, environment: Environment) -> Template:
        template = environment.get_template('StkmlIn/StkMl.yaml.j2')
        return template.render(Stackml=self)

    def get_node(self, id_: str) -> Node:
        node = None
        for tier in self.tiers:
            for node_ in tier.nodes:
                if node_.id_ == id_:
                    node = node_
                    break
        return node


    def get_node_tier(self, id_: str) -> Tier or None:
        tier = None
        for tier_ in self.tiers:
            for node in tier_.nodes:
                if node.id_ == id_:
                    tier = tier_
                    break
        return tier

    def get_tier(self, tier_name: str) -> Tier or None:
        tier = None
        for tier_ in self.tiers:
            if tier_.name == tier_name:
                tier = tier_
                break
        return tier

    def get_component(self, layer, cmp_id) -> Component or None:
        comp = None
        for tier in self.tiers:
            for node in tier.nodes:
                cmps = node.get_components(layer)
                for component in (cmps or []):
                    if component.id_ == cmp_id:
                        comp = component
                        break
                else:
                    continue
                break
        return comp

    def creat_referenced_components(self) -> None:
        for i_t in range(len(self.tiers)):
            tier = self.tiers[i_t]
            for i_n in range(len(tier.nodes)):
                node = tier.nodes[i_n]
                for i_layer in range(len(node.layers_element)):
                    layer = node.layers_element[i_layer]
                    for i_comp in range(len(layer.components)):
                        comp = layer.components[i_comp]
                        id_ = comp.id_ref
                        if id_:

                            comp = self.get_component(layer.type, id_)
                            id_ = comp.id_
                            comp = copy.deepcopy(comp)
                            layer.components[i_comp] = comp
                            layer.components[i_comp].id_ = id_


    def from_drawio(self, drawio) -> None:
        for tier in drawio.tiers:
            stackml_tier = Tier(name=tier.name, type_=tier.type)
            self.tiers.append(stackml_tier)
            for node in tier.nodes:
                stackml_node = stackml_tier.add_node(id_=node.name, cardinality=1, type_=node.type)
                for layer in reversed(node.layers):
                    if len(layer.components) > 0:
                        stackml_layer = stackml_node.add_layer_element(element='', type_=layer.type, hub=layer.hub)
                        for component in layer.components:
                            stackml_layer.add_component(Component(id_=component.name,
                                                                  type_=component.type.split('Component')[0]))

        for link in drawio.links:
            source = drawio.get_node(link.source)
            sink = drawio.get_node(link.source)
            stackml_link = Link(source=source.name,
                                sink=sink.name, layer=link.Layer)
            self.links.append(stackml_link)

    def sort_tiers(self):
        tiers_name = ['Thing', 'Edge', 'Network', 'Platform', 'Application']
        sorted_tiers = []
        for tier in tiers_name:
            tier_ = self.get_tier(tier)
            if tier_:
                sorted_tiers.append(tier_)

        self.tiers = sorted_tiers
