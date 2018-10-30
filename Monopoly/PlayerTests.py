from UserEntity import Player
from unittest.mock import patch, MagicMock
import unittest


class TestInit(unittest.TestCase):
    """
    Tests for Initalization of player class
    """

    def test_init_with_default_money(self):
        test_player = Player("Test")
        self.assertEqual(test_player.name, "Test")
        self.assertEqual(test_player.money, 1500)
        self.assertEqual(test_player.position, 0)
        self.assertEqual(test_player.owned_properites, {})

    def test_init_with_non_default_money(self):
        test_player = Player("Test", money_in=2000)
        self.assertEqual(test_player.name, "Test")
        self.assertEqual(test_player.money, 2000)


class TestLandedOn(unittest.TestCase):
    """
    Tests for landed_on method of Player Class
    """

    def test_landed_on_property(self):
        test_player = Player("test")
        test_player.position = 3
        self.assertEqual(test_player.landed_on(), "Brown 2")

    def test_landed_on_jail(self):
        test_player = Player("test")
        test_player.position = 'jail'
        self.assertEqual(test_player.landed_on(), "You're in Jail")

    def test_landed_on_action_spot(self):
        test_player = Player("test")
        test_player.position = 2
        self.assertEqual(test_player.landed_on(), "Community Chest")


class TestRollDice(unittest.TestCase):
    """
    Test for roll_dice method of Player Class
    """

    @patch("Player.randint", side_effect=[2, 3])
    def test_roll_dice_no_doubles(self, randint):
        test_player = Player("test")
        test_player.roll_dice()
        self.assertEquals(test_player.position, 5)

    @patch("Player.randint", side_effect=[3, 3, 4, 5])
    def test_roll_dice_one_double(self, randint):
        test_player = Player("test")
        test_player.roll_dice()
        self.assertEquals(test_player.position, 15)

    @patch("Player.randint", side_effect=[3, 3, 2, 2, 4, 5])
    def test_roll_dice_two_doubles(self, randint):
        test_player = Player("test")
        test_player.roll_dice()
        self.assertEquals(test_player.position, 19)

    @patch("Player.randint", return_value=3)
    def test_roll_dice_three_doubles(self, randint):
        test_player = Player("test")
        test_player.roll_dice()
        self.assertEquals(test_player.position, 'jail')

    @patch("Player.randint", side_effect=[6, 4])
    def test_roll_dice_pass_go_no_doubles(self, randint):
        test_player = Player("test")
        test_player.position = 35
        test_player.roll_dice()
        self.assertEquals(test_player.position, 5)

    @patch("Player.randint", side_effect=[6, 6, 6, 4])
    def test_roll_dice_pass_go_one_doubles(self, randint):
        test_player = Player("test")
        test_player.position = 35
        test_player.roll_dice()
        self.assertEquals(test_player.position, 17)

    @patch("Player.randint", side_effect=[2, 4])
    @patch("Player.get_yes_or_no_input", return_value = False)
    def test_roll_dice_while_in_jail_not_doubles(self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 'jail')

    @patch("Player.randint", side_effect = [3, 3, 2, 4])
    @patch("Player.get_yes_or_no_input", return_value = False)
    def test_roll_dice_while_in_jail_with_doubles(self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 22)

    @patch("Player.randint", side_effect=[2, 4])
    @patch("Player.get_yes_or_no_input", return_value = True)
    def test_roll_dice_while_in_jail_pay_bail_no_doubles(self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 16)
        self.assertEqual(test_player.money, 1450)

    @patch("Player.randint", side_effect = [3, 3, 2, 4])
    @patch("Player.get_yes_or_no_input", return_value = True)
    def test_roll_dice_while_in_jail_pay_bail_with_doubles(self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 22)
        self.assertEqual(test_player.money, 1450)

    @patch("Player.randint", side_effect = [5, 3, 2, 4])
    @patch("Player.get_yes_or_no_input", return_value = False)
    def test_roll_dice_while_in_jail_stay_in_jail(self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 'jail')
        self.assertEqual(test_player.money, 1500)


if __name__ == '__main__':
    unittest.main()
