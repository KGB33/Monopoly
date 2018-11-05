import unittest
from Tiles import Utility
from UserEntity import Bank, Player
from unittest.mock import patch


def correct_data():
    return ["Name", 150]


class Testinit(unittest.TestCase):

    def test_init(self):
        test_util = Utility(28, correct_data())
        self.assertEqual(test_util.location, 28)
        self.assertFalse(test_util.is_morgaged)
        self.assertEqual(test_util.name, "Name")
        self.assertEqual(test_util.price, 150)
        self.assertEqual(test_util.owner, Bank)


class TestLandedOn(unittest.TestCase):

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_owned_by_bank_and_by(self, get_yes_or_no_input):
        test_util = Utility(28, correct_data())
        test_player = Player("Name")
        test_util.landed_on(test_player)
        self.assertEqual(test_util.owner, test_player)
        self.assertEqual(test_player.money, 1350)
        self.assertEqual(test_player.owned_properites,
                         {test_util.location: test_util})

    @patch("Tiles.get_yes_or_no_input", return_value=False)
    def test_landed_on_owned_by_bank_dont_buy(self, get_yes_or_no_input):
        test_util = Utility(12, correct_data())
        test_player = Player("Test Player")
        test_util.landed_on(test_player)
        self.assertEqual(test_util.owner, Bank)
        self.assertEqual(test_player.money, 1500)
        self.assertEqual(test_player.owned_properites, {})

    @patch("Tiles.randint", return_value=5)
    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_owned_by_diff_player_who_owns_one_util(
            self, randint, get_yes_or_no_input):
        test_util = Utility(12, correct_data())
        test_player_1 = Player("Test Player")
        test_player_2 = Player("Owning Player")
        test_util.landed_on(test_player_2)
        test_util.landed_on(test_player_1)
        self.assertEqual(test_util.owner, test_player_2)
        self.assertEqual(test_player_2.owned_properites, {12: test_util})
        self.assertEqual(test_player_1.money, 1480)
        self.assertEqual(test_player_2.money, 1370)

    @patch("Tiles.randint", return_value=5)
    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_owned_by_diff_player_who_owns_two_utils(
            self, randint, get_yes_or_no_input):
        test_util_1 = Utility(12, correct_data())
        test_util_2 = Utility(28, correct_data())
        test_player_1 = Player("Test Player")
        test_player_2 = Player("Owning Player")
        test_util_1.landed_on(test_player_2)
        test_util_2.landed_on(test_player_2)
        test_util_1.landed_on(test_player_1)
        self.assertEqual(test_util_1.owner, test_player_2)
        self.assertEqual(test_util_2.owner, test_player_2)
        self.assertEqual(test_player_2.owned_properites,
                         {12: test_util_1, 28: test_util_2})
        self.assertEqual(test_player_1.money, 1450)
        self.assertEqual(test_player_2.money, 1250)

    def test_landed_on_owned_by_same_player(self):
        test_util = Utility(12, correct_data())
        test_player = Player("Test Player")
        test_util.owner = test_player
        test_util.landed_on(test_player)
        self.assertEqual(test_util.owner, test_player)
        self.assertEqual(test_player.money, 1500)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_owned_by_bank_buy_while_morgaged(
            self, get_yes_or_no_input):
        test_util = Utility(12, correct_data())
        test_player = Player("Test Player")
        test_player_2 = Player("Morgageee")
        test_util.owner = test_player_2
        test_util.morgage()
        test_util.landed_on(test_player)
        self.assertEqual(test_util.owner, test_player)
        self.assertEqual(test_player.money, 1425)
        self.assertEqual(test_player.owned_properites,
                         {test_util.location: test_util})


if __name__ == '__main__':
    unittest.main()
