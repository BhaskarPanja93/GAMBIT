from threading import Thread
from time import sleep

from OtherClasses.Party import Party


class Matchmaker:
    def __init__(self):
        self.inQueue = {}
        self.active = False

    def addToQueue(self, party: Party):
        self.inQueue[party.partyID] = party
        if not self.active:
            Thread(target=self.__startLooking).start()
    def removeFromQueue(self, party: Party):
        self.inQueue.pop(party.partyID)
    def __startLooking(self):
        self.active = True
        while len(self.inQueue) > 0:
            sleep(2)
            partiesToLookFor = list(self.inQueue)
            partiesToLookAgainst = list(self.inQueue)
            for partyID_SearchingFor in partiesToLookFor:
                for partyID_SearchingAgainst in partiesToLookAgainst:
                    if partyID_SearchingAgainst == partyID_SearchingFor or partyID_SearchingAgainst not in self.inQueue or partiesToLookFor not in self.inQueue: continue

        self.active = False