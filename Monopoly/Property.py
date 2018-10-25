import Location


class Property(Location):
    """
    Defines all the Properties on the board
    Does not include railroads or utilities
    """

    def __init__(self, location_in, property_data_in):
        """
        location: position on the board, int from 0 to 39
        property_data_in: list with vairous data formated as follows
        ["Name", "Color", Price, rent, rent_1_house, ..., rent_hotel]
        """
        self.name = property_data_in[0]
        self.color = property_data_in[1]
        self.price = property_data_in[2]
        self.rent = property_data_in[3:]
        self.number_of_houses = 0
        self.owner = bank
        self.is_morgaged =False
        super().__init__(location_in)

    def landed_on(self, player):
        """
        Returns the proper function depending on
        who landed on the property and who owns the property
        """
        if self.owner == bank: 
            return owned_by_bank(self, player)
        elif self.owner != player:
            return owned_by_player(self, player)

    def owned_by_bank(self, player):
        buy_or_pass
        if buy_or_pass: #buy
            player.money = player.money - self.cost
            self.owner = player
            player.owned_properties += {self.location : self.name}

    def ask_buy_or_pass(self, is_morgaged):
        """
        asks the player if they would like to purchuse the
        property, and displays the Name and price
        """
        if self.is_morgaged:
            buy_or_pass = str(input("Would you like to buy " + self.name +
                                    "for $" + self.price +
                                    "? (half off due to morgage) y/n"))
            while buy_or_pass != 'y' or buy_or_pass != 'n':
                print("That option is invalid!\n")
                buy_or_pass = str(input("Would you like to buy " + self.name +
                                        "for $" + self.price +
                                        "? (half off due to morgage) y/n"))
        else:
            buy_or_pass = str(input("Would you like to buy " + self.name +
                                    "for $" + true_cost + "? y/n"))
            while buy_or_pass != 'y' or buy_or_pass != 'n':
                print("That option is invalid!\n")
                buy_or_pass = str(input("Would you like to buy " + self.name +
                                        "for $" + true_cost + "? y/n"))
        if buy_or_pass == 'y':
            return True
        else:
            return False
