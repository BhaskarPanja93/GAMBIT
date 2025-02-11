from random import randrange

from jinja2 import Template
from randomisedString import RandomisedString

from OtherClasses.CachedElements import CachedElements
from OtherClasses.FileNames import FileNames


class Player:
    def __init__(self, viewerObj, playerName, cachedElements:CachedElements):
        self.party = None
        self.cachedElements = cachedElements
        self.viewer = viewerObj
        self.PFP = "https://i.pinimg.com/originals/e4/3d/2d/e43d2dea1d8793fcf016d2a634bdf761.png"
        self.userName = (playerName if playerName else "BOT-"+RandomisedString().AlphaNumeric(5, 5))
        self.state = "status-" + RandomisedString().AlphaNumeric(5, 5)
        self.level = 5
        self.rank = "https://static.wixstatic.com/media/cb04e9_db781b062c6d4d02b1d5dbaf314ad2ef~mv2.png/v1/fill/w_256,h_256,al_c,q_85,enc_auto/cb04e9_db781b062c6d4d02b1d5dbaf314ad2ef~mv2.png"
        self.MMR = randrange(1, 1000)
        self.optionsSelected = {}
        self.score = 0
        self.correct = 0
        self.incorrect = 0
        self.healthImpact = 0

    def displayPFP(self):
        return self.PFP
    def displayUserName(self):
        return self.userName
    def displayState(self):
        return self.state
    def displayLevel(self):
        return self.level
    def displayRank(self):
        return self.rank
    def displayAsTeam(self, hasCrown:bool=False):
        return Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizPlayer)).render(crownHide="hidden" if not hasCrown else "", username=self.displayUserName(), score=self.score, PFP=self.displayPFP())
    def displayAsOpponent(self, hasCrown:bool=False):
        return Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizPlayer)).render(crownHide="hidden" if not hasCrown else "", username=self.displayUserName(), score=self.score, PFP=self.displayPFP())
    def __gt__(self, other):
        return self.score > other.score
    def __lt__(self, other):
        return self.score < other.score