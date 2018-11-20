import unittest
from unittest.mock import patch
from Tiles import Board


class TestReadInBoard(unittest.TestCase):

    @patch(Tiles.input, return_value="StandardBoard.txt")
    def test_Standard_Board(self, input):
        Board.read_in_board()
        print(Board.spaces)
        self.assertEqual("Some Spaces", Board.spaces)


if __name__ == '__main__':
    unittest.main()
