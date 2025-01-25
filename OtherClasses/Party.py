from jinja2 import Template
from randomisedString import RandomisedString

from OtherClasses.Player import Player


class Party:
    def __init__(self):
        self.partyID = RandomisedString().AlphaNumeric(5, 10)
        self.players:dict[int, Player|None] = {0:None, 1:None, 2:None}
    def notifyPlayerJoined(self, index:int, player:Player):
        for index in self.players:
            toSendTo = self.players[index]
            if toSendTo.viewer is not None:
                if player.userName == toSendTo.userName:
                    toSendTo.viewer.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyMember)).render(PFP=party.players[0].displayPFP(), username=party.players[0].displayUserName(), level=party.players[0].displayLevel(), rank=party.players[0].displayRank()), DivID.lobbyPlayerSuffix, UpdateMethods.update)

    def notifyPlayerLeft(self, index:int, player:Player):
        pass
    def addPlayer(self, player:Player):
        for playerIndex in self.players:
            if self.players[playerIndex] is None:
                self.players[playerIndex] = player
                self.notifyPlayerJoined(playerIndex, player)
                return playerIndex
    def removePlayer(self, player:Player):
        for playerIndex in self.players:
            if self.players[playerIndex] is not None and self.players[playerIndex].userName == player.userName:
                self.players.pop(playerIndex)
                newParty = Party()
                newParty.addPlayer(player)
                self.notifyPlayerLeft(playerIndex, player)
                return playerIndex