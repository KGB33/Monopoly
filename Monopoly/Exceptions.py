class PlayerInJailError(Exception):
    """
    raised when the player is in jail
    """
    pass


class PlayerOutOfMoneyError(Exception):
    """
    Raised when the player is out of Money
    """
    pass


class TilesClassNotFoundError(Exception):
    """
    Raised when the data read into the Tiles Factory
    cannot determine a class type to create
    """
