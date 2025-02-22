from __future__ import annotations

from time import sleep

from randomisedString import RandomisedString

from OtherClasses.ChatMessageNodes import ChatMessageNodes
from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.DivIDs import DivID
from OtherClasses.Social import Player
from internal.dynamicWebsite import DynamicWebsite


class Party:
    def __init__(self, onPartyCodeCreated=None, onPartyClosed=None, onSelfLeave=None, cachedElements=None, matchmaker=None):
        self.partyID = RandomisedString().AlphaNumeric(10, 10)
        self.cachedElements = cachedElements
        self.matchMaker = matchmaker
        self.defaultPartyCode = "-----"
        self.partyCode = self.defaultPartyCode
        self.leaderIndex = None
        self.players:list[Player] = []
        self.maxPlayers = 3
        self.readyPlayers:list[Player] = []
        self.partyTimer = 0
        self.onPartyClosed =  onPartyClosed
        self.onPartyCodeCreated = onPartyCodeCreated
        self.onSelfLeave = onSelfLeave
        self.matchStarted = False
        self.team = None
    def __notifyOtherPlayersIndexDecrement(self, hollowIndex:int):
        for player in self.players:
            if player.viewer is None: continue
            player.viewer.sendCustomMessage(CustomMessages.decrementPartyMemberIndex(hollowIndex, len(self.players)))
    def __notifyPlayerPromotion(self, oldLeaderIndex:int, newLeaderIndex:int):
        for player in self.players:
            if player.viewer is not None:
                player.viewer.sendCustomMessage(CustomMessages.newLeader(oldLeaderIndex, newLeaderIndex))
    def __notifyOtherPlayersJoined(self, newPlayerIndex:int, newPlayer:Player):
        for playerIndex in range(len(self.players)):
            player = self.players[playerIndex]
            if playerIndex != newPlayerIndex:
                if player.viewer is None: continue
                player.viewer.sendCustomMessage(CustomMessages.addedPartyMember(newPlayerIndex, newPlayer))
    def __notifyOtherPlayersLeft(self, oldPlayerIndex:int):
        for player in self.players:
            if player.viewer is not None:
                player.viewer.sendCustomMessage(CustomMessages.removedPartyMember(oldPlayerIndex))
    def __notifySelfJoined(self, newPlayerIndex:int):
        newPlayer = self.players[newPlayerIndex]
        if newPlayer.viewer is not None:
            for playerIndex in range(len(self.players)):
                player = self.players[playerIndex]
                newPlayer.viewer.sendCustomMessage(CustomMessages.addedPartyMember(playerIndex, player))
    def __notifySelfLeft(self, oldPlayer:Player, notifySelfLeave:bool):
        if oldPlayer.viewer is not None and self.onSelfLeave is not None:
            if notifySelfLeave: self.onSelfLeave(oldPlayer.viewer)
    def playerReady(self, player:Player):
        if player not in self.readyPlayers:
            self.readyPlayers.append(player)
            self.updateReadyStat()
        self.checkAllPlayersReady()
    def playerUnready(self, player:Player):
        if player in self.readyPlayers:
            self.readyPlayers.remove(player)
            self.updateReadyStat()
        self.checkAllPlayersReady()
    def updateReadyStat(self):
        for player in self.players:
            if player.viewer: player.viewer.updateHTML(f"{'CANCEL' if player in self.readyPlayers else 'START'} <span class='text-sm ml-2'>[{len(self.readyPlayers)}/{len(self.players)}]</span>", DivID.startStopQueue, DynamicWebsite.UpdateMethods.update)
    def checkAllPlayersReady(self):
        self.partyTimer = 0
        if len(self.readyPlayers)==len(self.players):
            self.matchMaker.addToQueue(self)
            while len(self.readyPlayers)==len(self.players):
                for player in self.players:
                    if player.viewer is not None:
                        player.viewer.updateHTML(str(self.partyTimer), DivID.startStopQueue, DynamicWebsite.UpdateMethods.update)
                sleep(1)
                self.partyTimer += 1
            if not self.matchStarted:
                self.matchMaker.removeFromQueue(self)
    def addPlayer(self, newPlayer:Player):
        if len(self.players) < self.maxPlayers:
            newPlayer.party = self
            self.players.append(newPlayer)
            index = len(self.players) - 1
            self.__notifySelfJoined(index)
            self.sendPartyCode(newPlayer)
            self.__notifyOtherPlayersJoined(index, newPlayer)
            self.updateReadyStat()
            return index
    def removePlayer(self, oldPlayer:Player, notifySelfLeave:bool):
        for index in range(len(self.players)):
            if self.players[index].userName == oldPlayer.userName:
                if index == self.leaderIndex or self.leaderIndex is None: self.__transferLeader()
                self.__notifySelfLeft(oldPlayer, notifySelfLeave)
                self.__notifyOtherPlayersLeft(index)
                self.__notifyOtherPlayersIndexDecrement(index)
                self.players.pop(index)
                if len(self.players) == 0 and self.onPartyClosed is not None: self.onPartyClosed(self)
                else: self.playerUnready(oldPlayer)
                return index

    def sendPartyCode(self, player):
        if player.viewer is not None:
            player.viewer.updateHTML(self.partyCode, DivID.partyCodeShow, DynamicWebsite.UpdateMethods.update)
    def generatePartyCode(self):
        if self.partyCode == self.defaultPartyCode:
            self.partyCode = RandomisedString().AlphaNumeric(5, 5).lower()
            self.onPartyCodeCreated(self)
            for player in self.players:
                if player is not None:
                    self.sendPartyCode(player)
    def __transferLeader(self):
        if len(self.players):
            oldLeaderIndex = self.leaderIndex
            self.leaderIndex = 0
            self.__notifyPlayerPromotion(oldLeaderIndex, self.leaderIndex)
    def __isLeader(self, player:Player):
        return player.userName == self.players[self.leaderIndex].userName
    def kickPlayer(self, requestedBy:Player, playerIndex:int):
        if self.__isLeader(requestedBy):
            toKick = self.players[playerIndex]
            if toKick is not None:
                self.removePlayer(toKick, True)
    def receiveMessage(self, sender, text):
        for player in self.players:
            if player.viewer: player.viewer.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.PARTY, sender if sender!=player.userName else ChatMessageNodes.YOU, text))
    def __eq__(self, other):
        return self.partyID == other.partyID