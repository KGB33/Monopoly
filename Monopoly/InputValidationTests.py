import unittest
from InputValidation import *
from unittest.mock import patch


class TestGetYesOrNo(unittest.TestCase):
    """
    Tests input validation when asking for a yes or no responce
    """

    @patch('builtins.input', return_value='y')
    def test_get_yes_or_no_yes_responce(self, input):
        self.assertTrue(get_yes_or_no_input('prompt'))

    @patch('builtins.input', return_value='n')
    def test_get_yes_or_no_no_responce(self, input):
            self.assertFalse(get_yes_or_no_input('prompt'))

    @patch('builtins.input', side_effect=['a', 'b', 'c', 'y'])
    def test_get_yes_or_no_three_invalids(self, input):
        self.assertTrue(get_yes_or_no_input('prompt'))

if __name__ == '__main__':
    unittest.main()
