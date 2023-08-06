from unittest import TestCase

from Stkml.Drawio import Node


class TestNode(TestCase):

    def setUp(self) -> None:
        self.node = Node(name='Node', type_='ThingNode', nature='Hardware')

    def test_set_dimension_should_get_the_require_dimension_to_put_all_layers_in_the_node(self):
        # Assign
        self.node.add_layer(type_='Physical', hub=False)
        l = self.node.add_layer(type_='Network', hub=False)

        #Act
        self.node.generate_layers_position()
        self.node.set_dimensions()

        #Assert
        self.assertEqual(self.node.dimension[0], l.dimension[0] + 20)
        self.assertEqual(self.node.dimension[1], l.position[1] + l.dimension[1] + 10)
