import unittest
from InputValidation import get_yes_or_no_input, get_positive_non_zero_int_input
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


class TestGetPositiveNonZeroIntInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['3'])
    def test_correct_responce_first_time(self, input):
        self.assertEqual(get_positive_non_zero_int_input('prompt'), 3)

    @patch('builtins.input', side_effect=['-90', '0', 'abc', '-asd123', '-123abc', '-32', 3])
    def test_incorrect_responces(self, input):
        self.assertEqual(get_positive_non_zero_int_input('prompt'), 3)


if __name__ == '__main__':
    unittest.main()
