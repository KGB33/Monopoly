import unittest
from Tiles import Property
from unittest.mock import patch
from UserEntity import Player, Bank


def correct_data(self):
    return ["Color", 150, 5, 10, 20, 40, 80, 160]


class Testinit(unittest.TestCase):
    """
    Testing for initalization of Property Class
    """

    def test_init_with_correct_data(self):
        test_property = Property(12, "Name", correct_data(self))
        self.assertEqual(test_property.name, "Name")
        self.assertEqual(test_property.color, "Color")
        self.assertEqual(test_property.price, 150)
        self.assertEqual(test_property.rent, [5, 10, 20, 40, 80, 160])
        self.assertEqual(test_property.number_of_houses, 0)
        self.assertEqual(test_property.owner, Bank)
        self.assertFalse(test_property.is_mortgaged)
        self.assertEqual(test_property.location, 12)


class TestLandedOn(unittest.TestCase):
    """
    Testing for landed on method
    """

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_owned_by_bank_and_buy(self, get_yes_or_no_input):
        test_property = Property(12, "Name", correct_data(self))
        test_player = Player("Test Player")
        test_property.landed_on(test_player)
        self.assertEqual(test_property.owner, test_player)
        self.assertEqual(test_player.money, 1350)
        self.assertEqual(test_player.owned_properites,
                         {test_property.location: test_property})

    @patch("Tiles.get_yes_or_no_input", return_value=False)
    def test_landed_on_owned_by_bank_dont_buy(self, get_yes_or_no_input):
        test_property = Property(12, "Name", correct_data(self))
        test_player = Player("Test Player")
        test_property.landed_on(test_player)
        self.assertEqual(test_property.owner, Bank)
        self.assertEqual(test_player.money, 1500)
        self.assertEqual(test_player.owned_properites, {})

    def test_landed_on_owned_by_diff_player(self):
        test_property = Property(12, "Name", correct_data(self))
        test_player_1 = Player("Test Player")
        test_player_2 = Player("Owning Player")
        test_property.owner = test_player_2
        test_property.landed_on(test_player_1)
        self.assertEqual(test_property.owner, test_player_2)
        self.assertEqual(test_player_1.money, 1495)

    def test_landed_on_owned_by_same_player(self):
        test_property = Property(12, "Name", correct_data(self))
        test_player = Player("Test Player")
        test_property.owner = test_player
        test_property.landed_on(test_player)
        self.assertEqual(test_property.owner, test_player)
        self.assertEqual(test_player.money, 1500)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_owned_by_bank_buy_while_morgaged(
            self, get_yes_or_no_input):
        test_property = Property(12, "Name", correct_data(self))
        test_player = Player("Test Player")
        test_player_2 = Player("Morgageee")
        test_property.owner = test_player_2
        test_property.mortgage()
        test_property.landed_on(test_player)
        self.assertEqual(test_property.owner, test_player)
        self.assertEqual(test_player.money, 1425)
        self.assertEqual(test_player.owned_properites,
                         {test_property.location: test_property})


if __name__ == '__main__':
    unittest.main()
