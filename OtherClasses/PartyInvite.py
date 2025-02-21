from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.Interactions import Interactions
from OtherClasses.Party import Party
from OtherClasses.Player import Player


class PartyInvite:
    def __init__(self, party:Party, whoseParty:Player, sender:Player, receiver:Player):
        self.party = party
        self.whoseParty = whoseParty
        self.sender = sender
        self.receiver = receiver
        self.type = Interactions.PARTY_INVITE if self.sender.userName==self.whoseParty.userName else Interactions.PARTY_JOIN_REQUEST
        self.ID = f"{sender.userName}-{'' if self.sender.userName==self.whoseParty.userName else ''}-{self.type}"
        self.active = True
    def sendToReceiver(self):
        if self.receiver.viewer and self.active: self.receiver.viewer.sendCustomMessage(CustomMessages.newSocialInteraction(self.sender.userName, self.ID, self.type))
    def destroy(self):
        if self.receiver.viewer and self.active:
            self.receiver.viewer.sendCustomMessage(CustomMessages.deleteInteraction(self.ID))
            self.active = False
