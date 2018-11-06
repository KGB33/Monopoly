import unittest
from unittest.mock import patch
from Tiles import Card, Chance, CommunityChest
from UserEntity import Player

class TestLandedOn(unittest.TestCase):
    
    @patch("Tiles.randint", return_value=0)
    def test_landed_on_card(self, randint):
        card_test = Card(22, "Card")
        test_player = Player("Name")
        result = card_test.landed_on(test_player)
        self.assertEqual(result, "Cards not implemented.")

    @patch("Tiles.randint", return_value=6)
    def test_landed_on_chance(self, randint):
        chance_test = Chance(7, "Chance")
        test_player = Player("Name")
        chance_test.landed_on(test_player)
        self.assertEqual(test_player.money, 1550)

    @patch("Tiles.randint", return_value=1)
    def test_landed_on_communty_chest(self, randint):
        cc_test = CommunityChest(17, "Communty Chest")
        test_player = Player("Name")
        cc_test.landed_on(test_player)
        self.assertEqual(test_player.money, 1700)

if __name__ == '__main__':
    unittest.main()
