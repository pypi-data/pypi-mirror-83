from unittest import TestCase

from Stkml.Drawio.Component import Component
from Stkml.Drawio.Layer import Layer


class TestLayer(TestCase):

    def setUp(self):
        self.layer = Layer(type_="Physical", hub=False)

    def test_set_component_position_should_set_the_components_beside_when_layer_is_not_hub(self):
        # Assign
        c = Component('cmp1', 'type')
        x0 = c.position[0]
        y0 = c.position[1]

        #Act
        self.layer.set_component_position(c)

        #Assert
        self.assertEqual(x0, c.position[0])
        self.assertEqual(c.position[1], y0 + c.dimension[1] * len(self.layer.components) + (len(self.layer.components) +1 ) * 10)



    def test_set_component_position_should_set_the_components_in_stack_when_layer_is_hub(self):
        # Assign
        self.layer.hub = True
        c = Component('cmp1', 'type')
        y0 = c.position[1]
        x0 = c.position[0]
        d0 = c.dimension[0]

        #Act
        self.layer.set_component_position(c)

        #Assert
        self.assertEqual(y0, c.position[1])
        self.assertEqual(c.position[0], x0 + (d0 + 10) * len(self.layer.components) - 8)

    def test_add_component_position_should_increase_layer_height_when_they_are_more_then_one_component(self):
        # Assign
        height = self.layer.dimension[1]

        #Act
        self.layer.add_component('cmp1', 'type')
        c2 = self.layer.add_component('cmp2', 'type')

        #Assert
        self.assertEqual(self.layer.dimension[1], 10 + height + c2.dimension[1])
