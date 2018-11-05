import unittest
from Tiles import Railroad
from UserEntity import Player
from unittest.mock import patch


def getData():
    return ["Name", 200]


class TestInit(unittest.TestCase):

    def test_init(self):
        test_rr = Railroad(5, getData())
        self.assertEqual(test_rr.name, "Name")
        self.assertEqual(test_rr.price, 200)
        self.assertEqual(test_rr.location, 5)


class TestLandedOn(unittest.TestCase):

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_one_owned(self, get_yes_or_no_input):
        test_rr_1 = Railroad(5, getData())
        owner = Player("Owner")
        rider = Player("Rider")
        test_rr_1.landed_on(owner)
        test_rr_1.landed_on(rider)
        self.assertEqual(owner.money, 1350)
        self.assertEqual(owner.owned_properites,
                         {5: test_rr_1})
        self.assertEqual(rider.money, 1450)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_two_owned(self, get_yes_or_no_input):
        test_rr_1 = Railroad(5, getData())
        test_rr_2 = Railroad(15, getData())
        owner = Player("Owner")
        rider = Player("Rider")
        test_rr_1.landed_on(owner)
        test_rr_2.landed_on(owner)
        test_rr_1.landed_on(rider)
        self.assertEqual(owner.money, 1200)
        self.assertEqual(owner.owned_properites,
                         {5: test_rr_1, 15: test_rr_2})
        self.assertEqual(rider.money, 1400)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_three_owned(self, get_yes_or_no_input):
        test_rr_1 = Railroad(5, getData())
        test_rr_2 = Railroad(15, getData())
        test_rr_3 = Railroad(25, getData())
        owner = Player("Owner")
        rider = Player("Rider")
        test_rr_1.landed_on(owner)
        test_rr_2.landed_on(owner)
        test_rr_3.landed_on(owner)
        test_rr_1.landed_on(rider)
        self.assertEqual(owner.money, 1050)
        self.assertEqual(owner.owned_properites,
                         {5: test_rr_1, 15: test_rr_2,
                          25: test_rr_3})
        self.assertEqual(rider.money, 1350)

    @patch("Tiles.get_yes_or_no_input", return_value=True)
    def test_landed_on_four_owned(self, get_yes_or_no_input):
        test_rr_1 = Railroad(5, getData())
        test_rr_2 = Railroad(15, getData())
        test_rr_3 = Railroad(25, getData())
        test_rr_4 = Railroad(35, getData())
        owner = Player("Owner")
        rider = Player("Rider")
        test_rr_1.landed_on(owner)
        test_rr_2.landed_on(owner)
        test_rr_3.landed_on(owner)
        test_rr_4.landed_on(owner)
        test_rr_1.landed_on(rider)
        self.assertEqual(owner.money, 900)
        self.assertEqual(owner.owned_properites,
                         {5: test_rr_1, 15: test_rr_2,
                          25: test_rr_3, 35: test_rr_4})
        self.assertEqual(rider.money, 1300)


if __name__ == '__main__':
    unittest.main()
