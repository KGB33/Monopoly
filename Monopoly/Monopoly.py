from UserEntity import Player
from Tiles import Board
from InputValidation import get_positive_non_zero_int_input
"""
Temp main to demonstrat / play with player class
"""


def __main__():
    Board.read_in_board()
    print(Board.__str__())
    number_of_players = get_positive_non_zero_int_input("\nHow many Players? ")
    player_list = []
    for i in range(0, number_of_players):
        name = str(input("\nWhat is the next player's name?"))
        player_list += [Player(name)]
    for turn_number in range(0, 1):
        for player in player_list:
            print("\n\n\n" + player.name + "'s Turn!"
                  + "\n==============================")
            keep_rolling = True
            num_doubles = 0
            while keep_rolling:
                num_doubles = player.roll_dice(num_doubles=num_doubles)
                print("\nLanded On: " + Board.spaces[player.position].name
                      + "\n\tTile number: " + str(player.position))
                Board.spaces[player.position].landed_on(player)
                if num_doubles == 0:
                    keep_rolling = False



__main__()
