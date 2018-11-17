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


class TestRollDice(unittest.TestCase):
    """
    Test for roll_dice method of Player Class
    """

    @patch("UserEntity.randint", side_effect=[2, 3])
    def test_roll_dice_no_doubles(self, randint):
        test_player = Player("test")
        test_player.roll_dice()
        self.assertEqual(test_player.position, 5)

    @patch("UserEntity.randint", side_effect=[4, 5])
    def test_roll_dice_one_double(self, randint):
        test_player = Player("test")
        test_player.roll_dice(num_doubles=1)
        self.assertEquals(test_player.position, 9)

    @patch("UserEntity.randint", side_effect=[4, 5])
    def test_roll_dice_two_doubles(self, randint):
        test_player = Player("test")
        test_player.roll_dice(num_doubles=2)
        self.assertEquals(test_player.position, 9)

    @patch("UserEntity.randint", return_value=3)
    def test_roll_dice_three_doubles(self, randint):
        test_player = Player("test")
        test_player.roll_dice(num_doubles=2)
        self.assertEquals(test_player.position, 'jail')

    @patch("UserEntity.randint", side_effect=[6, 4])
    def test_roll_dice_pass_go_no_doubles(self, randint):
        test_player = Player("test")
        test_player.position = 35
        test_player.roll_dice()
        self.assertEqual(test_player.money, 1700)
        self.assertEquals(test_player.position, 5)

    @patch("UserEntity.randint", side_effect=[6, 4])
    def test_roll_dice_pass_go_one_doubles(self, randint):
        test_player = Player("test")
        test_player.position = 35
        test_player.roll_dice(num_doubles=1)
        self.assertEquals(test_player.money, 1700)
        self.assertEquals(test_player.position, 5)

    @patch("UserEntity.randint", side_effect=[2, 4])
    @patch("UserEntity.get_yes_or_no_input", return_value=False)
    def test_roll_dice_while_in_jail_not_doubles(
            self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 'jail')

    @patch("UserEntity.randint", side_effect=[3, 3, 2, 4])
    @patch("UserEntity.get_yes_or_no_input", return_value=False)
    def test_roll_dice_while_in_jail_with_doubles(
            self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        num_dubs = test_player.roll_dice()
        test_player.roll_dice(num_doubles=num_dubs)
        self.assertEqual(test_player.position, 22)

    @patch("UserEntity.randint", side_effect=[2, 4])
    @patch("UserEntity.get_yes_or_no_input", return_value=True)
    def test_roll_dice_while_in_jail_pay_bail_no_doubles(
            self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 16)
        self.assertEqual(test_player.money, 1450)

    @patch("UserEntity.randint", side_effect=[3, 3, 2, 4])
    @patch("UserEntity.get_yes_or_no_input", return_value=True)
    def test_roll_dice_while_in_jail_pay_bail_with_doubles(
            self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        num_dubs = test_player.roll_dice()
        test_player.roll_dice(num_doubles=num_dubs)
        self.assertEqual(test_player.position, 22)
        self.assertEqual(test_player.money, 1450)

    @patch("UserEntity.randint", side_effect=[5, 3, 2, 4])
    @patch("UserEntity.get_yes_or_no_input", return_value=False)
    def test_roll_dice_while_in_jail_stay_in_jail(
            self, randint, get_yes_or_no_input):
        test_player = Player("test")
        test_player.position = 'jail'
        test_player.roll_dice()
        self.assertEqual(test_player.position, 'jail')
        self.assertEqual(test_player.money, 1500)

    @patch("UserEntity.randint", side_effect=[2, 3])
    def test_roll_dice_pass_go(self, randint):
        test_player = Player("test")
        test_player.position = 37
        test_player.roll_dice()
        self.assertEqual(test_player.money, 1700)
        self.assertEqual(test_player.position, 2)


if __name__ == '__main__':
    unittest.main()
