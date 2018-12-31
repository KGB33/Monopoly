from abc import ABC, abstractmethod
from UserEntity import Player, Bank, FreeParking
from InputValidation import get_yes_or_no_input
from random import randint
from Exceptions import TilesClassNotFoundError


class Location(ABC):
    """
    Abstract Parent Class for all locations on the board

    Attributes:
        :location: (int)
            position, (0 - 39), on the monopoly board

        :name: (String)
            Name of the location

        :price: (int)
            purchase cost of the tile

        :owner: (UserEntity Object)
            Current Owner of the tile

        :is_mortgaged: (Boolean)
            mortgage state of the tile
    """

    @abstractmethod
    def __init__(self, location, name, price):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile

        :param price: (int)
            purchase cost of the tile
        """
        self.location = location
        self.name = name
        self.price = price
        self.owner = Bank
        self.is_mortgaged = False
        super().__init__()

    def landed_on(self, player):
        """
        Calls the proper function depending on
        who landed on the property and who owns the property

        :param player: (Player Object)
            The player that landed on the tile

        """
        if self.owner == Bank:
            self.owned_by_bank(player)
        elif self.owner != player:
            self.owned_by_player(player)

    def owned_by_bank(self, player):
        """
        Gives the player the option to purchase the tile,
        if the tile is purchased, transfers money,
        updates owner, and sets is_mortgaged to False

        :param player: (Player Object)
            Player that landed on the tile
        """
        buy_or_pass = self.ask_buy_or_pass()
        if buy_or_pass:  # buy
            player.money = player.money - self.price
            self.owner = player
            player.owned_properites.update({self.location: self})
            self.is_mortgaged = False
            self.price = self.price * 2

    def owned_by_player(self, player):
        """
        Charges player rent, transfers rent between owner and player

        :param player: (Player Object)
            Player that landed on tile
        """
        self.owner.exchange_money(player, self.rent[self.number_of_houses])

    def ask_buy_or_pass(self):
        """
        Asks the player if they would like to purchase the
        property, displays the Name and price

        :return: (Boolean)
            True if the player would like to buy
            False if the player would not like to buy
        """
        buy_or_pass = get_yes_or_no_input(
                            "Would you like to buy " + self.name +
                            " for $" + str(self.price) + "? y/n")
        return buy_or_pass

    def mortgage(self):
        """
        Sets is_mortgaged to True,
        Gives owner mortgage value (1/2 price),
        Sets price to 1/2 price,
        Sets owner to Bank,
        """
        self.is_mortgaged = True
        self.price = self.price / 2
        Bank.exchange_money(self.owner, self.price)
        self.owner = Bank

    def unmortgage(self, player):
        """
        Sets is_mortgaged to False,
        Sets price to full price
        Sets owner to player
        Charges Player unmortgage price

        :param player: (Player Object)
            Player that is unmortgageing the tile
        """
        self.is_mortgaged = False
        self.price = self.price * 2
        self.owner = player
        self.owner.exchange_money(self.owner, self.price * -.75)

    def format_owner(self):
        """
        Formats current owner information for __str__()

        :return: (String)
            Easy to read owner information
        """
        if isinstance(self.owner, Bank):
            owned_by = "Owner: {0}, Current Rent {1}" \
                .format(self.owner, self.format_current_rent())
        else:
            owned_by = "Owner: {0}, Price: {1}, Morgaged: {2}" \
                .format(self.owner, self.price, self.is_mortgaged)
        return owned_by

    def __str__(self):
        """
        :return: (String)
            Easy to read tile description
        """
        output = "{0} {1}" \
                 "\n\t{2}".format(self.location, self.name, self.format_owner())
        return output


class Property(Location):
    """
    Defines all the Properties on the board
    Does not include railroads or utilities

    Attributes:

        ---- From Location Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location

            :price: (int)
                purchase cost of the tile

            :owner: (UserEntity Object)
                Current Owner of the tile

            :is_mortgaged: (Boolean)
                mortgage state of the tile

        ---- New in Property Class ----
            :color: (String)
                Color of the property

            :rent: (1x6 array-like)
                Rent tiers for the property

            :number_of_houses: (int)
                Number of houses on the property, 0 - 5
                Zero is No houses
                Five is a hotel

            :cost_per_house: (int)
                Price of one house
    """

    def __init__(self, location, name, property_data):
        """
        :param location: (Int)
            position on the board, int from 0 to 39

        :param property_data: (1x9 array-like)
            list with various data formatted as follows
            ["Color", Price, rent, rent_1_house, ..., rent_hotel]
        """
        self.color = property_data[0]
        self.rent = property_data[2:]
        self.number_of_houses = 0
        self.cost_per_house = self.set_cost_per_house(location)
        super().__init__(location, name, int(property_data[1]))

    @staticmethod
    def set_cost_per_house(location):
        """
        Determines the price for one house based on the location

        :param location: (int)
            location on the board

        :return: (int)
            cost for one house
        """
        if location > 30:
            return 200
        elif location > 20:
            return 150
        elif location > 10:
            return 100
        else:
            return 50

    def __str__(self):
        """
        :return: (String)
            Easy to read tile description
        """
        rent_tiers = ''
        for tier in self.rent:
            rent_tiers += str(tier) + ', '
        owned_by = self.format_owner()
        output = "{0} {1} {2}" \
                 "\n\t{3}" \
                 "\n\tCost Per House: {4}, Number Of Houses: {5}" \
                 "\n\tRent Tiers {6}"\
            .format(self.location, self.name, self.color, owned_by,
                    self.cost_per_house, self.number_of_houses, rent_tiers)
        return output

    def format_current_rent(self):
        """
        Formats Current rent for __str__

        :return: (String)
            Current Rent
        """
        return str(self.rent[self.number_of_houses])


class Utility(Location):
    """
    Defines all utilities
    i.e. Electric Company and Water Works

    Attributes:

        ---- From Location Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location

            :price: (int)
                purchase cost of the tile

            :owner: (UserEntity Object)
                Current Owner of the tile

            :is_mortgaged: (Boolean)
                mortgage state of the tile
    """

    def __init__(self, location, name, price=150):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile

        :param price: (Optional, int, default=150)
            purchase cost of the tile
        """
        super().__init__(location, name, price)

    def owned_by_player(self, player):
        """
        Charges player rent, transfers rent between owner and player

        :param player: (Player Object)
            Player that landed on tile
        """
        num_utils_owned = 0
        multiplier = {1: 4, 2: 10}
        roll = randint(1, 6)
        for key in self.owner.owned_properites:
            if isinstance(self.owner.owned_properites[key], Utility):
                num_utils_owned += 1
        self.owner.exchange_money(player, roll * multiplier[num_utils_owned])


class Railroad(Location):
    """
    Defines all 4 railroads

    Attributes:

        ---- From Location Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location

            :price: (int)
                purchase cost of the tile

            :owner: (UserEntity Object)
                Current Owner of the tile

            :is_mortgaged: (Boolean)
                mortgage state of the tile
    """

    def __init__(self, location, name, price=200):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile

        :param price: (Optional, int, default=200)
            purchase cost of the tile
        """
        super().__init__(location, name, price)

    def owned_by_player(self, player):
        """
        Charges player rent, transfers rent between owner and player

        :param player: (Player Object)
            Player that landed on tile
        """
        num_railroads_owned = 0
        cost = {1: 50, 2: 100, 3: 150, 4: 200}
        for key in self.owner.owned_properites:
            if isinstance(self.owner.owned_properites[key], Railroad):
                num_railroads_owned += 1
        self.owner.exchange_money(player, cost[num_railroads_owned])


class Effect(ABC):
    """
    Parent class for all squares where an effect is
    applied. Including Chance, Community Chest, Income tax, etc.

    Attributes:

        :location: (int)
            position, (0 - 39), on the monopoly board

        :name: (String)
            Name of the location
    """

    @abstractmethod
    def __init__(self, location, name):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile
        """
        self.location = location
        self.name = name

    @abstractmethod
    def landed_on(self, player):
        pass


class Card(Effect):
    """
    Parent Class for Chance and Community Chest Cards

    Attributes:
        ---- From Effect Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location

        ---- New In Card Class ----
            :active_player: (Player Object)
                Player that the card will be affecting
    """

    def __init__(self, location, name):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile
        """
        self.active_player = None
        super().__init__(location, name)

    def landed_on(self, player):
        """
        Sets Active player to player, then calls draw_card()

        :param player: (Player Object)
            Player that landed on card tile

        :return:
            calls draw_card
        """
        self.active_player = player
        return self.draw_card()

    def draw_card(self):
        pass

    # -------------Card effects --------------

    def advance_to_tile(self, tile_num):
        """
        Moves player to specified tile and calls that tile's landed_on method

        :param tile_num: (int)
            Tile the active player will be moved to
        """
        # Checks if player will pass go
        if self.active_player.position >= tile_num:
            self.active_player.money += 200
        self.active_player.position = tile_num
        print("You've been moved to :", Board.spaces[tile_num],
              "\n\tTile Number:", tile_num)
        return Board.spaces[self.active_player.position].landed_on(self.active_player)

    def advance_to_next(self, class_type):
        """
        Advances active player to the next tile of specified class type

        :param class_type: (Object)
            class of tile to advance to
            examples: Railroad, Utility, Card
        """
        location_to_check = self.active_player.position + 1
        passed_go = False
        while not isinstance(
                Board.spaces[location_to_check], class_type):
            location_to_check += 1
            if location_to_check > 39:
                location_to_check = location_to_check % 40
                passed_go = True
        self.active_player.position = location_to_check
        if passed_go:
            self.active_player.money += 200
        print("You've advanced to the next ", str(class_type),
              "\n\tTile Number: ", self.active_player.position)
        return Board.spaces[self.active_player.position].landed_on(self.active_player)

    def gain_money(self, amount):
        """
        Give player money

        :param amount: (int)
            Amount of money to give active player
        """
        print("You've gained $", amount)
        self.active_player.money += amount

    def lose_money(self, amount):
        """
        Takes player's money

        :param amount: (int)
            amount of money to take from active player
        """
        print("You've lost $", amount)
        Board.spaces[20].exchange_money(self.active_player, amount)

    def get_out_of_jail_free(self):
        """
        Gives player a get out of jail free card
        """
        print("You got a get out of jail free card",
              "\n\t you now have ", self.active_player.get_out_of_jail_cards)
        self.active_player.get_out_of_jail_cards += 1

    def go_back(self, num_tiles):
        """
        Moves player back specified number of spaces and calls that tiles landed_on method.

        :param num_tiles: (int)
            Number of tiles to be moved back
        """
        self.active_player.position -= num_tiles
        print("You've been sent back ", num_tiles, "tiles.",
              "\nYou're now on tile number: ", self.active_player.position)
        return Board.spaces[self.active_player.position].landed_on()

    def go_to_jail(self):
        """
        Sends the player to jail, player does not pass go and does not collect $200
        """
        print("Oh No! you've been sent to jail!!")
        self.active_player.position = 'jail'

    def house_repairs(self):
        """
        Charges player house repairs
        """
        owed_money = 0
        for key in Board.spaces:
            try:
                if Board.spaces[key].owner == self.active_player:
                    hold = Board.spaces[key].number_of_houses
                    owed_money += 25 * hold
            except AttributeError:
                # Corner Tiles have no attribute owner, skipped
                pass
        print("House repairs are expensive!")
        if owed_money == 0:
            print("Lucky for you, you have no houses")
        else:
            print("You paid: $", owed_money)
        Board.spaces[20].exchange_money(self.active_player, owed_money)

    def pay_all_other_players(self, amount):
        """
        Active player pays all other players specified amount

        :param amount: (int)
            amount to pay other players
        """
        # TODO: implement pay all other players
        print("Lucky for {} I don't know how to make you pay everyone else... yet".format(self.active_player))

    def get_money_from_all_other_players(self, amount):
        """
        Active player gets money from all other players

        :param amount: (int)
            amount gotten from other players
        """
        amount = amount * -1
        self.pay_all_other_players(amount)

    def __str__(self):
        """
        :return: (String)
            Easy to read tile description
        """
        output = "{0} {1}".format(self.location, self.name)
        return output
          

class Chance(Card):
    """
    All Chance Cards

    Attributes:
        ---- From Card Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location

            :active_player: (Player Object)
                Player that the card will be affecting
    """

    def __init__(self, location, name):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile
        """
        super().__init__(location, name)

    def draw_card(self):
        """
        Chooses a random random card and calls the appropriate method
        """
        key = randint(0, 16)
        if key == 0:
            return self.advance_to_tile(0)
        elif key == 1:
            return self.advance_to_tile(24)
        elif key == 2:
            return self.advance_to_tile(11)
        elif key == 3:
            return self.advance_to_next(Utility)
        elif key == 4:
            return self.advance_to_next(Railroad)
        elif key == 5:
            return self.advance_to_next(Railroad)
        elif key == 6:
            return self.gain_money(50)
        elif key == 7:
            self.get_out_of_jail_free()
        elif key == 8:
            return self.go_back(3)
        elif key == 9:
            return self.go_to_jail()
        elif key == 10:
            return self.house_repairs()
        elif key == 11:
            return self.lose_money(15)
        elif key == 12:
            return self.advance_to_tile(5)
        elif key == 13:
            return self.advance_to_tile(39)
        elif key == 14:
            return self.pay_all_other_players(50)
        elif key == 15:
            return self.gain_money(150)
        elif key == 16:
            return self.gain_money(100)
        else:
            return print("Bad Chance Card Draw")
    

class CommunityChest(Card):
    """
    All Community Chest Cards

    Attributes:
        ---- From Card Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location

            :active_player: (Player Object)
                Player that the card will be affecting
    """

    def __init__(self, location, name):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile
        """
        super().__init__(location, name)

    def draw_card(self):
        """
        Chooses a random random card and calls the appropriate method
        """
        key = randint(0, 16)
        if key == 0:
            return self.advance_to_tile(0)
        elif key == 1:
            return self.gain_money(200)
        elif key == 2:
            return self.lose_money(50)
        elif key == 3:
            return self.gain_money(50)
        elif key == 4:
            return self.get_out_of_jail_free()
        elif key == 5:
            return self.go_to_jail()
        elif key == 6:
            return self.get_money_from_all_other_players(50)
        elif key == 7:
            return self.gain_money(100)
        elif key == 8:
            return self.gain_money(20)
        elif key == 9:
            return self.get_money_from_all_other_players(10)
        elif key == 10:
            return self.gain_money(100)
        elif key == 11:
            return self.lose_money(50)
        elif key == 12:
            return self.lose_money(150)
        elif key == 13:
            return self.gain_money(25)
        elif key == 14:
            return self.house_repairs()
        elif key == 15:
            return self.gain_money(10)
        elif key == 16:
            return self.gain_money(100)
        else:
            print("bad CC draw")


class Board(object):
    """
    The Monopoly Board

    Attributes:
        :spaces: (Dict)
            A dictionary where the key is the location of a tile and the content is the property

    """
    spaces = {}

    @classmethod
    def default_board(cls):
        """
        Builds a default board for testing
        """
        cls.spaces = {}
        streets = {x: Property(x, "Name", ["Color", 150, 5, 10, 20, 40, 80, 160])
                   for x in range(0, 40)}
        railroads = {x: Railroad(x, "Name") for x in [5, 15, 25, 35]}
        utilities = {x: Utility(x, "Name") for x in [12, 28]}
        chances = {x: Chance(x, "Chance Card") for x in [7, 22, 36]}
        community_chest = {x: CommunityChest(x, "Community Chest Card")
                           for x in [2, 17, 33]}
        free_parking = {20: FreeParking()}
        cls.spaces.update(streets)
        cls.spaces.update(railroads)
        cls.spaces.update(utilities)
        cls.spaces.update(chances)
        cls.spaces.update(community_chest)
        cls.spaces.update(free_parking)

    @classmethod
    def read_in_board(cls):
        """
        read in a board from file. Each line in the file should be formatted as follows:

        Square# ClassType class data
        """
        loop_value = True
        while loop_value:
            try:
                if get_yes_or_no_input('Would You Like To Use The Standard Board?'):
                    file_name = 'StandardBoard'
                else:
                    file_name = input("Please enter the file Name: ")
                with open('boards/' + file_name) as file:
                    for line in file:
                        if not line.startswith('#'):
                            data = line.split()
                            new_tile = TileFactory.create_tile(data)
                            cls.spaces.update(new_tile)
                            loop_value = False
            except FileNotFoundError:
                if file_name == "Q":
                    quit()
                print("File Not found, please try again.\n\tOr Enter Q to quit\n")

    @classmethod
    def __str__(cls):
        """
        :return: (String)
            Formatted __str__ method for all objects in spaces
        """
        output = ''
        for key in cls.spaces:
            output = output + "\n" + cls.spaces[key].__str__()
        return output


# construct the default board for testing
Board.default_board()


class TileFactory:
    """
    Creates all possible different tiles, used with read_in_board in Board
    """

    @staticmethod
    def create_tile(data):
        """
        Creates a tile based on the data provided

        :param data:
            Data read in from a file

        :return:
            A tile to be added to the board
        """
        while True:
            try:
                if data is not None:
                    position = int(data[0])
                    class_type = data[1]
                    name = data[2]
                    try:
                        data = [int(x) for x in data[3:]]
                    except ValueError:
                        last_part_data = [int(x) for x in data[4:]]
                        data = [data[3], ] + last_part_data
                if class_type == "Property":
                    return {position: Property(position, name, data)}
                elif class_type == "Utility":
                    return {position: Utility(position, name)}
                elif class_type == "Railroad":
                    return {position: Railroad(position, name)}
                elif class_type == "Chance":
                    return {position: Chance(position, name)}
                elif class_type == "CommunityChest":
                    return {position: CommunityChest(position, name)}
                elif class_type == "SetTax":
                    return {position: SetTax(position, name, data[0])}
                elif class_type == "PercentTax":
                    return {position: PercentTax(position, name, data[0])}
                elif class_type == "FreeParking":
                    return {position: FreeParking(position)}
                elif class_type == "Go":
                    return {0: Go()}
                elif class_type == 'JustVisiting':
                    return {10: JustVisiting()}
                elif class_type == 'GoToJail':
                    return {30: GoToJail()}
                elif class_type == 'jail':
                    return {'jail': Jail()}
                else:
                    raise TilesClassNotFoundError
            except TilesClassNotFoundError:
                print("\n\nError!!\n\tClass Type: ", data[1], " Not Found!")
                break
            except IndexError:
                data = None


class SetTax(Effect):
    """
    Charges player a set tax amount, is not dependant on the player's wealth

    Attributes:
        ---- From Effect Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location

        ---- New in SetTax Class ----
            :amount:
                Amount to tax the player
    """

    def __init__(self, location, name, amount):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile

        :param amount: (int)
            amount to tax the player
        """
        self.amount = int(amount)
        super().__init__(location, name)

    def landed_on(self, player):
        """
        Takes amount from player and adds it to Free Parking

        :param player: (Player Object)
            Player that landed on tile
        """
        Board.spaces[20].exchange_money(player, self.amount)

    def __str__(self):
        """
        :return: (String)
            Easy to read tile description
        """
        output = "{0} {1}" \
                 "\n\tTax Amount: ${2}"\
            .format(self.location, self.name, self.amount)
        return output


class PercentTax(Effect):
    """
        Charges player a set tax amount, is not dependant on the player's wealth

        Attributes:
            ---- From Effect Class ----
                :location: (int)
                    position, (0 - 39), on the monopoly board

                :name: (String)
                    Name of the location

            ---- New in PercentTax Class ----
                :percent:
                    percent to tax the player
        """

    def __init__(self, location, name, percent):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile

        :param percent: (float or String)
            percent to tax the player
        """
        self.percent = float(percent)
        super().__init__(location, name)

    def landed_on(self, player):
        """
        Charges player percent of their total wealth and gives it to free parking

        :param player: (Player Object)
            Player that landed on Percent Tax
        """
        Board.spaces[20].exchange_money(player, player.money * self.percent)

    def __str__(self):
        """
        :return: (String)
            Easy to read tile description
        """
        output = "{0} {1}" \
                 "\n\tTax percent: {2}%"\
            .format(self.location, self.name, self.percent)


class CornerTile(ABC):
    """
    Parent Class For Each of the corner tiles
    Excluding Free Parking.

    Attributes:
        :location: (int)
            position, (0 - 39), on the monopoly board

        :name: (String)
            Name of the location

    """

    @abstractmethod
    def __init__(self, location, name):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (String)
            Name of the Tile
        """
        self.location = location
        self.name = name

    @abstractmethod
    def landed_on(self, player):
        pass

    def __str__(self):
        """
        :return: (String)
            Description of the tile
        """
        output = "{0} {1}".format(self.location, self.name)
        return output


class Go(CornerTile):
    """
    Models GO Tile

    Attributes:
        ---- From CornerTile Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location
    """

    def __init__(self, location=0, name='GO'):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (Optional, String, default=GO)
            Name of the Tile
        """
        super().__init__(location, name)

    def landed_on(self, player):
        print("Landed on Go!")


class JustVisiting(CornerTile):
    """
    Models Just Visiting (jail) tile

    Attributes:
        ---- From CornerTile Class ----
            :location: (int)
                position, (0 - 39), on the monopoly board

            :name: (String)
                Name of the location
    """

    def __init__(self, location=10, name="JustVisiting"):
        """
        :param location: (int)
            Location, (0 - 39) on the monopoly board

        :param name: (Optional, String, default=JustVisiting)
            Name of the Tile
        """
        super().__init__(location, name)

    def landed_on(self, player):
        # TODO: find a way to print out what players are in jail
        print("Just Visiting Jail")


class GoToJail(CornerTile):
    """
    Class that sends people to jail
    """

    def __init__(self, location=30, name='Go To Jail'):
        super().__init__(location, name)

    def landed_on(self, player):
        player.position = 'jail'
        print("Go To Jail!!!")


class Jail(CornerTile):

    def __init__(self, location='jail', name='jail'):
        super().__init__(location, name)

    def landed_on(self, player):
        pass

    def __str__(self):
        return "This is the jail"

