import unittest

from Stkml.Stkml.LayerElement.BusinesslayerElement import BusinesslayerElement


class TestBusinessLayerElement(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_create_business_layer_element(self):
        # Assign
        element = 'Buz'

        # Act
        e = BusinesslayerElement(element, hub='EndPoint')

        # Assert
        self.assertIsInstance(e, BusinesslayerElement)
