from OtherClasses.Party import Party
from OtherClasses.Player import Player


class PartyInvite:
    def __init__(self, interactionID, party:Party, sender:Player, receiver:Player):
        self.interactionID = interactionID
        self.party = party
        self.sender = sender
        self.receiver = receiver