from itertools import combinations
from math import exp, sqrt
from threading import Thread
from time import sleep, time

from OtherClasses.CachedElements import CachedElements
from OtherClasses.Party import Party
from OtherClasses.Team import Team


class Match:
    def __init__(self, teamA:Team, teamB:Team):
        self.oldestPartyCreatedAt = None
        self.MMRDiff = None
        self.teamA = teamA
        self.teamB = teamB
        self.totalPlayers = 0
        self.quiz = None
        self.generateDetails()

    def generateDetails(self):
        self.teamA.match = self
        self.teamB.match = self
        self.MMRDiff = abs(self.teamA.averageMMR-self.teamB.averageMMR)
        self.oldestPartyCreatedAt = min(self.teamA.oldestPartyCreatedAt, self.teamB.oldestPartyCreatedAt)
        for party in self.teamA.parties+self.teamB.parties:
            self.totalPlayers += len(party.players)

    def isValid(self):
        return self.MMRDiff <= exp(sqrt(time()-self.oldestPartyCreatedAt))**2 and (self.MMRDiff < 300 if self.teamB.parties else True)

class Matchmaker:
    def __init__(self, onMatch, cachedElements:CachedElements):
        self.inQueue:list[Party] = []
        self.onMatch = onMatch
        self.cachedElements = cachedElements
        Thread(target=self.__startLooking).start()

    def addToQueue(self, party: Party):
        if party not in self.inQueue: self.inQueue.append(party)

    def removeFromQueue(self, party: Party):
        if party in self.inQueue:
            self.inQueue.remove(party)

    def __startLooking(self):
        playersPerTeam = 3
        while True:
            if not self.inQueue:
                sleep(1)
                continue
            print("\nIn Queue:", len(self.inQueue))
            for party in self.inQueue:
                for player in party.players:
                    print("--- ", player.userName, player.MMR)
            smallestDiffMatch = None
            partiesInQueue = self.inQueue
            for team1Size in range(min(3, len(partiesInQueue)), 0, -1):
                for team1parties in combinations(partiesInQueue, team1Size):
                    remainingParties = [x for x in partiesInQueue if x not in team1parties]
                    for team2Size in range(min(3, len(remainingParties)), 0-1, -1):
                        for team2parties in combinations(remainingParties, team2Size):
                            team1 = Team(team1parties, self.cachedElements)
                            team2 = Team(team2parties, self.cachedElements)
                            if team1.isValid(False) and team2.isValid(True):
                                dummyMatch = Match(team1, team2)
                                if dummyMatch.isValid():
                                    if smallestDiffMatch is None or ((2*playersPerTeam) - dummyMatch.totalPlayers)*dummyMatch.MMRDiff<((2 * playersPerTeam) - smallestDiffMatch.totalPlayers)*smallestDiffMatch.MMRDiff:
                                        smallestDiffMatch = dummyMatch

            if smallestDiffMatch is None: sleep(1)
            else:
                teamA = smallestDiffMatch.teamA
                teamB = smallestDiffMatch.teamB
                teamB.fillBots(teamA.averageMMR, playersPerTeam)
                teamA.fillBots(teamB.averageMMR, playersPerTeam)
                teamA.opponentTeam = teamB
                teamB.opponentTeam = teamA
                match = Match(teamA, teamB)
                for party in teamA.parties:
                    party.matchStarted = True
                    party.readyPlayers = []
                    self.removeFromQueue(party)
                for party in teamB.parties:
                    party.matchStarted = True
                    party.readyPlayers = []
                    self.removeFromQueue(party)
                print("Matched")
                print(f"\tMMRDiff={match.MMRDiff}")
                print("\t\tTeamA")
                for party in match.teamA.parties:
                    print(f"\t\t\tParty waited for {party.partyTimer}")
                    for player in party.players:
                        print("\t\t\t\t", player.userName, player.MMR)
                print("\t\tTeamB")
                for party in match.teamB.parties:
                    print(f"\t\t\tParty waited for {party.partyTimer}")
                    for player in party.players:
                        print("\t\t\t\t", player.userName, player.MMR)
                self.onMatch(match)



