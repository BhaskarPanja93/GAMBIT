from randomisedString import RandomisedString

from OtherClasses.Player import Player


class Friend:
    def __init__(self, P1:Player, P2:Player):
        self.connectionID = "connection-"+RandomisedString().AlphaNumeric(5, 5)
        self.P1 = P1
        self.P2 = P2