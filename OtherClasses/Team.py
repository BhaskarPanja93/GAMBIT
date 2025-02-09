from math import sqrt, exp
from threading import Thread
from time import time

from OtherClasses.Party import Party
from OtherClasses.Player import Player


class Team:
    def __init__(self, parties) -> None:
        self.parties:list[Party] = list(parties)
        self.count = 0
        self.sumMMR = 0
        self.minMMR = None
        self.maxMMR = 0
        self.oldestPartyCreatedAt = None
        self.averageMMR = 0
        self.generateDetails()

    def generateDetails(self):
        for party in self.parties:
            self.count += len(party.players)
            self.oldestPartyCreatedAt = time()-party.partyTimer if self.oldestPartyCreatedAt is None or self.oldestPartyCreatedAt>time()-party.partyTimer else self.oldestPartyCreatedAt
            for player in party.players:
                self.sumMMR += player.MMR
                self.minMMR = player.MMR if self.minMMR is None or self.minMMR>player.MMR else self.minMMR
                self.maxMMR = max(self.maxMMR, player.MMR)
        self.averageMMR = self.sumMMR / max(1, self.count)
        if self.oldestPartyCreatedAt is None:
            self.oldestPartyCreatedAt = time()
        if self.minMMR is None:
            self.minMMR = 0

    def isValid(self, allowEmpty:bool):
        return (self.count > 0 or allowEmpty) and (time()-self.oldestPartyCreatedAt > 4 or self.count==0) and (self.averageMMR - self.minMMR <= exp(sqrt(time()-self.oldestPartyCreatedAt))**2 or time()-self.oldestPartyCreatedAt > 10)

    def fillBots(self, finalMMR, totalPlayers):
        botsNeeded = totalPlayers-self.count
        if botsNeeded == 0 : return
        totalMMRNeeded = finalMMR*totalPlayers - self.sumMMR
        botMMR = totalMMRNeeded / botsNeeded
        botParty = Party()
        for _ in range(botsNeeded):
            botPlayer = Player(None, f"Bot")
            botPlayer.MMR = botMMR
            botParty.addPlayer(botPlayer)
        self.parties.append(botParty)
        self.generateDetails()
