import unittest
from UserEntity import Bank


class TestInit(unittest.TestCase):
    """
    Tests for Bank __init__
    """

    def test_init(self):
        test_bank = Bank()
        self.assertIsInstance(test_bank, Bank)
        self.assertEqual(Bank.__str__(), "The Bank")


if __name__ == '__main__':
    unittest.main()
