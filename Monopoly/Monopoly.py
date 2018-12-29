from UserEntity import Player
from Tiles import Board
from InputValidation import get_positive_non_zero_int_input
from Exceptions import PlayerOutOfMoneyError
"""
Temp main to demonstrate / play with player class
"""


def main():
    Board.read_in_board()
    print(Board.__str__())
    number_of_players = get_positive_non_zero_int_input("\nHow many Players? ")
    player_list = []
    for i in range(0, number_of_players):
        name = str(input("\nWhat is the next player's name?"))
        player_list += [Player(name)]
    while player_list:  # In Python empty lists are False
        for player in player_list:
            try:
                if player.money <= 0:
                    raise PlayerOutOfMoneyError
                print("\n\n\n" + player.name + "'s Turn!"
                      + "\n==============================\n"
                      + player.__str__()
                      + "\n==============================\n")
                choice = player.turn_options()
                keep_rolling = True
                num_doubles = 0
                while keep_rolling:
                    num_doubles = player.roll_dice(num_doubles=num_doubles)
                    print("\nLanded On:\n" + Board.spaces[player.position].__str__())
                    Board.spaces[player.position].landed_on(player)
                    if num_doubles == 0:
                        keep_rolling = False
            except PlayerOutOfMoneyError:
                player_list.remove(player)


if __name__ == '__main__':
    main()
