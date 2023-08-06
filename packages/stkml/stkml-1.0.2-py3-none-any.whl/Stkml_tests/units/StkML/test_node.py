import unittest


from Stkml.Stkml.Node import Node, EnergylayerElement



class TestNode(unittest.TestCase):

    def setUp(self):
        self.node = Node('1', 1, 'ThingNode')

    def test_add_layer_element_should_add_the_specific_element_type(self):
        # Assign
        element_type = 'EnergylayerElement'
        element = 'Buz'

        # Act
        e = self.node.add_layer_element(element, element_type, hub='False')

        # Assert
        self.assertIsInstance(e, EnergylayerElement)

    def test_get_layer_element_should_return_the_specific_element_type(self):
        # Assign
        element_type = 'EnergylayerElement'
        element = 'Buz'
        self.node.add_layer_element(element, element_type, hub='EndPoint')

        # Act
        e = self.node.get_layer_element(element_type)

        # Assert
        self.assertIsInstance(e, EnergylayerElement)
