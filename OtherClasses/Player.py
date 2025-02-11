from random import randrange

from random import choice
from jinja2 import Template
from randomisedString import RandomisedString

from OtherClasses.CachedElements import CachedElements
from OtherClasses.FileNames import FileNames


class Player:
    def __init__(self, viewerObj, playerName, cachedElements:CachedElements):
        self.PFP_LIST = [
        "https://i.pinimg.com/564x/05/0b/4b/050b4b5204d7b8f92bea7da09a819a3e.jpg",
        "https://i.pinimg.com/236x/ed/1d/92/ed1d9261080d42ef548d6dfe44df5c03.jpg",
        "https://i.pinimg.com/236x/a5/ac/32/a5ac32de26502b9b34acdd8681b53e63.jpg",
        "https://i.pinimg.com/236x/8a/61/46/8a614641b53bc8dc0d1ee02326a38956.jpg",
        "https://pbs.twimg.com/media/FP6DoSeXEAAAIqG.png",
        "https://i.pinimg.com/564x/18/0e/65/180e6574a9aa0e4c7c23a252db4184dc.jpg",
        "https://i.pinimg.com/236x/9a/32/1b/9a321b907189f15a91469ca730421459.jpg",
        "https://i.pinimg.com/564x/bf/2e/22/bf2e225612d2d2160f49df825e179864.jpg",
        "https://i.pinimg.com/564x/05/93/c2/0593c22a578bf58e4bf01a4a063a3587.jpg",
        "https://i.pinimg.com/236x/a2/c6/ef/a2c6efe54eba3be3ebefbda068725c68.jpg",
        "https://i.pinimg.com/236x/20/69/04/2069047e6b5be475b93a3a1fe37a2e54.jpg",
        "https://i.pinimg.com/550x/40/e9/dc/40e9dcec8ad71caeb53de023a5241754.jpg",
        "https://i.pinimg.com/564x/2f/b9/f7/2fb9f7a42f940e2300323da45af47e84.jpg",
        "https://i.pinimg.com/236x/1b/70/19/1b7019c55fc0eb78a712b9bc043f7738.jpg",
        "https://i.pinimg.com/564x/67/7b/85/677b85e0c6c2ad8735c613368b7b6e66.jpg",
        "https://i.pinimg.com/170x/dc/c8/55/dcc855cbfcc5ae9bc9e7bfdaee27a3dc.jpg",
        "https://i.pinimg.com/236x/29/14/2d/29142dac5d5f2343ce00a9d8f773f910.jpg",
        "https://i.pinimg.com/originals/e4/3d/2d/e43d2dea1d8793fcf016d2a634bdf761.png",
        "https://pbs.twimg.com/media/FP6Dpk2XEAgco1F.png",
        "https://i.pinimg.com/originals/14/98/90/14989073ad9b9c8efddd8dcaff076db5.png",
        "https://i.pinimg.com/236x/b4/6a/98/b46a989d1dfaa3bb5354d63867a58bd3.jpg",
        ]
        self.party = None
        self.cachedElements = cachedElements
        self.viewer = viewerObj
        self.PFP = choice(self.PFP_LIST)
        self.userName = (playerName if playerName else "BOT-"+RandomisedString().AlphaNumeric(5, 5))
        self.state = "ONLINE"
        self.level = 0
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
        return Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizPlayer)).render(crownHide="hidden" if not hasCrown else "", username=self.displayUserName(), score=int(self.score), PFP=self.displayPFP())
    def displayAsOpponent(self, hasCrown:bool=False):
        return Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizPlayer)).render(crownHide="hidden" if not hasCrown else "", username=self.displayUserName(), score=int(self.score), PFP=self.displayPFP())
    def __gt__(self, other):
        return self.score > other.score
    def __lt__(self, other):
        return self.score < other.score