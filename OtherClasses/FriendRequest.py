from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.Interactions import Interactions
from OtherClasses.Player import Player


class FriendRequest:
    def __init__(self, sender:Player, receiver:Player):
        self.sender = sender
        self.receiver = receiver
        self.ID = f"FR-{sender.userName}"
        self.active = True
    def sendToReceiver(self):
        if self.receiver.viewer and self.active: self.receiver.viewer.sendCustomMessage(CustomMessages.newSocialInteraction(self.sender.userName, self.ID, Interactions.FRIEND_REQUEST))
    def destroy(self):
        if self.receiver.viewer and self.active:
            self.receiver.viewer.sendCustomMessage(CustomMessages.deleteInteraction(self.ID))
            self.active = False
