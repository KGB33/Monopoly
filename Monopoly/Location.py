from abc import ABC, abstractmethod


class Location(ABC):
    """
    Abstract Parent Class for all locations on the board
    """

    def __init__(self, location_in):
        self.location = location_in
        super().__init__()

    @abstractmethod
    def landed_on(self, player):
        pass
