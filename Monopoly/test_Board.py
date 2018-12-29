import unittest
from unittest.mock import patch
from Tiles import Board


class TestReadInBoard(unittest.TestCase):

    @patch('Tiles.get_yes_or_no_input', return_value=True)
    def test_Standard_Board(self, input):
        Board.read_in_board()
        print(Board.spaces)
        self.assertEqual(41, len(Board.spaces)) # 41 due to jail/just visiting
        Board.default_board()


class TestDefaultBoard(unittest.TestCase):

    def test_default_board(self):
        self.assertEqual(len(Board.spaces), 40)


if __name__ == '__main__':
    unittest.main()
