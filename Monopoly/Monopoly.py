from UserEntity import Player
from Board import Board
"""
Temp main to demonstrat / play with player class
"""

def __main__():
    number_of_players = int(input("How many Players?"))
    player_list = []
    for i in range(0,number_of_players):
        name = str(input("What is the next player's name?"))
        player_list += [Player(name)]
    for turn_number in range(0,4):
        for i in range(0, number_of_players):
            player_list[i].roll_dice()
            print("\nPlayer: " + player_list[i].name + " is On " + Board.spaces[player_list[i].position])
       

__main__()