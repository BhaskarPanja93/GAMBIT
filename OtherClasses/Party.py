from randomisedString import RandomisedString

from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.Player import Player


class Party:
    def __init__(self):
        self.partyID = RandomisedString().AlphaNumeric(5, 10)
        self.players:dict[int, Player|None] = {0:None, 1:None, 2:None}
    def notifyPlayerJoined(self, newPlayerIndex:int, newPlayer:Player):
        for toSendIndex in self.players:
            playerAtIndex = self.players[toSendIndex]
            if playerAtIndex is None: continue
            if newPlayer.viewer is not None:
                newPlayer.viewer.sendCustomMessage(CustomMessages.addedPartyMember(toSendIndex, playerAtIndex.displayPFP(), playerAtIndex.displayUserName(), playerAtIndex.displayLevel(), playerAtIndex.displayRank()))
            if toSendIndex != newPlayerIndex and playerAtIndex.viewer is not None:
                playerAtIndex.viewer.sendCustomMessage(CustomMessages.addedPartyMember(newPlayerIndex, newPlayer.displayPFP(), newPlayer.displayUserName(), newPlayer.displayLevel(), newPlayer.displayRank()))
    def notifyPlayerLeft(self, index:int, player:Player):
        pass
    def addPlayer(self, player:Player):
        for playerIndex in self.players:
            if self.players[playerIndex] is None:
                self.players[playerIndex] = player
                self.notifyPlayerJoined(playerIndex, player)
                return playerIndex
    def removePlayer(self, player:Player):
        pass