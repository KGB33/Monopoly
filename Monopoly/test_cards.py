import unittest
from unittest.mock import patch
from Tiles import Card, Chance, CommunityChest, Utility, Railroad, Board
from UserEntity import Player


class TestInit(unittest.TestCase):

    def test_card_init(self):
        test_card = Card(7, "Card Name")
        self.assertEqual(7, test_card.location)
        self.assertEqual("Card Name", test_card.name)

    def test_chance_init(self):
        test_chance = Chance(13, "Chance Name")
        self.assertEqual(13, test_chance.location)
        self.assertEqual("Chance Name", test_chance.name)

    def test_community_chest_init(self):
        test_cc = CommunityChest(17, "Community Chest")
        self.assertEqual(17, test_cc.location)
        self.assertEqual("Community Chest", test_cc.name)


class TestLandedOn(unittest.TestCase):

    @patch("Tiles.randint", return_value=6)
    def test_landed_on_chance(self, choice):
        chance_test = Chance(7, "Chance")
        test_player = Player("Name")
        chance_test.landed_on(test_player)
        self.assertEqual(test_player.money, 1550)

    @patch("Tiles.randint", return_value=1)
    def test_landed_on_communty_chest(self, choice):
        cc_test = CommunityChest(17, "Communty Chest")
        test_player = Player("Name")
        cc_test.landed_on(test_player)
        self.assertEqual(test_player.money, 1700)


class TestAdvanceToTile(unittest.TestCase):

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_tile_dont_pass_go(self, get_yest_or_no_input):
        test_card = Card(7, "Card Name")
        test_player = Player("Name")
        test_player.position = 7
        test_card.active_player = test_player
        test_card.advance_to_tile(15)
        self.assertEqual(test_player.position, 15)
        self.assertEqual(test_player.money, 1300)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_tile_pass_go(self, get_yes_or_no_input):
        test_card = Card(7, "Card Name")
        test_player = Player("Name")
        test_player.position = 7
        test_card.active_player = test_player
        test_card.advance_to_tile(3)
        self.assertEqual(test_player.position, 3)
        self.assertEqual(test_player.money, 1550)


class TestAdvanceToNextUtility(unittest.TestCase):

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    @patch("Tiles.randint", return_value=5)
    def test_advance_to_1st_util(self, get_yes_or_no_input, randint):
        # Utils on Tiles 12 & 28
        test_card = Card(3, "Name")
        test_player = Player("Name")
        test_player.position = 3
        test_card.active_player = test_player
        test_card.advance_to_next(Utility)
        self.assertEqual(test_player.position, 12)
        self.assertEqual(test_player.money, 1480)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    @patch("Tiles.randint", return_value=5)
    def test_advance_to_2nd_util(self, get_yes_or_no_input, randint):
        # Utils on Tiles 12 & 28
        test_card = Card(22, "Name")
        test_player = Player("Name")
        test_player.position = 22
        test_card.active_player = test_player
        test_card.advance_to_next(Utility)
        self.assertEqual(test_player.position, 28)
        self.assertEqual(test_player.money, 1480)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    @patch("Tiles.randint", return_value=5)
    def test_advance_to_util_pass_go(self, get_yes_or_no_input, randint):
        # Utils on Tiles 12 & 28
        test_card = Card(33, "Name")
        test_player = Player("Name")
        test_player.position = 33
        test_card.active_player = test_player
        test_card.advance_to_next(Utility)
        self.assertEqual(test_player.position, 12)
        self.assertEqual(test_player.money, 1680)


class TestAdvanceToNextRailroad(unittest.TestCase):

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_1st_Railroad(self, get_yes_or_no_input):
        # railroads on Tiles 12 & 28
        test_card = Card(3, "Name")
        test_player = Player("Name")
        test_player.position = 3
        test_card.active_player = test_player
        test_card.advance_to_next(Railroad)
        self.assertEqual(test_player.position, 5)
        self.assertEqual(test_player.money, 1300)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_3rd_railroad(self, get_yes_or_no_input):
        # railroads on Tiles 12 & 28
        test_card = Card(22, "Name")
        test_player = Player("Name")
        test_player.position = 22
        test_card.active_player = test_player
        test_card.advance_to_next(Railroad)
        self.assertEqual(test_player.position, 25)
        self.assertEqual(test_player.money, 1300)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_railroad_pass_go(self, get_yes_or_no_input):
        # railroads on Tiles 12 & 28
        test_card = Card(37, "Name")
        test_player = Player("Name")
        test_player.position = 37
        test_card.active_player = test_player
        test_card.advance_to_next(Railroad)
        self.assertEqual(test_player.position, 5)
        self.assertEqual(test_player.money, 1650)

class TestAdvanceToTile(unittest.TestCase):

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_property(self, get_yes_or_no_input):
        test_card = Card(2, "Name")
        test_player = Player("Name")
        test_player.position = 2
        test_card.active_player = test_player
        test_card.advance_to_tile(3)
        self.assertEqual(test_player.money, 1350)
        self.assertEqual(test_player.position, 3)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_property_pass_go(self, get_yes_or_no_input):
        test_card = Card(33, "Name")
        test_player = Player("Name")
        test_player.position = 33
        test_card.active_player = test_player
        test_card.advance_to_tile(14)
        self.assertEqual(test_player.money, 1550)
        self.assertEqual(test_player.position, 14)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_railroad(self, get_yes_or_no_input):
        test_card = Card(2, "Name")
        test_player = Player("Name")
        test_player.position = 2
        test_card.active_player = test_player
        test_card.advance_to_tile(35)
        self.assertEqual(test_player.money, 1300)
        self.assertEqual(test_player.position, 35)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_railraod_pass_go(self, get_yes_or_no_input):
        test_card = Card(2, "Name")
        test_player = Player("Name")
        test_player.position = 33
        test_card.active_player = test_player
        test_card.advance_to_tile(15)
        self.assertEqual(test_player.money, 1500)
        self.assertEqual(test_player.position, 15)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_utility(self, get_yes_or_no_input):
        test_card = Card(2, "Name")
        test_player = Player("Name")
        test_player.position = 2
        test_card.active_player = test_player
        test_card.advance_to_tile(12)
        self.assertEqual(test_player.money, 1350)
        self.assertEqual(test_player.position, 12)


    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_advance_to_utility_pass_go(self, get_yes_or_no_input):
        test_card = Card(2, "Name")
        test_player = Player("Name")
        test_player.position = 31
        test_card.active_player = test_player
        test_card.advance_to_tile(28)
        self.assertEqual(test_player.money, 1550)
        self.assertEqual(test_player.position, 28)


class TestGainMoney(unittest.TestCase):


    def test_gain_money(self):
        test_player = Player("Name")
        test_card = Card(2, "Name")
        test_player.position = 2
        test_card.active_player = test_player
        test_card.gain_money(50)
        self.assertEqual(test_player.money, 1550)


class TestLoseMoney(unittest.TestCase):


    def test_lose_money(self):
        test_player = Player("Name")
        test_card = Card(2, "Name")
        test_player.position = 2
        test_card.active_player = test_player
        test_card.lose_money(500)
        self.assertEqual(test_player.money, 1000)
        self.assertEqual(Board.spaces[20].money, 500)


class TestGettingGetOutOfJailFreeCard(unittest.TestCase):


    def get_get_out_of_free_card(self):
        test_player = Player("Name")
        test_card = Card(2, "Name")
        test_player.position = 2
        test_card.active_player = test_player
        test_card.get_out_of_jail_free()
        self.assertEqual(test_player.get_out_of_jail_cards, 1)

class TestGoBack(unittest.TestCase):


    def go_back_pass_go(self):
        test_player = Player("Name")
        test_card = Card(2, "Name")
        test_player.position = 2
        test_card.active_player = test_player
        test_card.active_player = test_player
        self.assertEqual(test_player.position, 39)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def go_back_dont_pass_go(self):
        test_player = Player("Name")
        test_card = Card(22, "Name")
        test_player.position = 22
        test_card.active_player = test_player
        test_card.go_back(3)
        self.assertEqual(test_player.position, 19)
        self.assertEqual(test_player.money, 1350)


if __name__ == '__main__':
    unittest.main()
