import unittest
from Tiles import Property
from unittest.mock import patch
from UserEntity import Player


def correct_data(self):
       return ["Name", "Color", 150, 5, 10, 20, 40, 80, 160]


class Testinit(unittest.TestCase):
    """
    Testing for initalization of Property Class
    """

    
    def test_init_with_correct_data(self):
        test_property = Property(12, correct_data(self))
        self.assertEqual(test_property.name, "Name")
        self.assertEqual(test_property.color, "Color")
        self.assertEqual(test_property.price, 150)
        self.assertEqual(test_property.rent, [5, 10, 20, 40, 80, 160])
        self.assertEqual(test_property.number_of_houses, 0)
        self.assertEqual(test_property.owner, 'bank')
        self.assertFalse(test_property.is_morgaged)
        self.assertEqual(test_property.location, 12)


class TestLandedOn(unittest.TestCase):
    """
    Testing for landed on method
    """

    @patch("Tiles.Property.owned_by_bank", return_value=True)
    def test_landed_on_owned_by_bank(self, owned_by_bank):
        test_property = Property(12, correct_data(self))
        self.assertTrue(test_property.landed_on(Player("Test Player")))


if __name__ == '__main__':
    unittest.main()
