from random import choice
from random import randrange

from randomisedString import RandomisedString

from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.Interactions import Interactions
from OtherClasses.PlayerStatus import PlayerStatus
from OtherClasses.Question import Question
from internal.dynamicWebsite import DynamicWebsite


class Player:
    def __init__(self, viewerObj:DynamicWebsite.Viewer|None=None, username:str|None=None):
        self.OFFLINE_PFP = "https://i.pinimg.com/736x/9f/64/75/9f6475a845d14fb7647e2fdfd1407976.jpg"
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
        self.rankImages = [
            "https://static.wikia.nocookie.net/valorant/images/7/79/Iron_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/a/ae/Bronze_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/d/d7/Silver_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/2/27/Gold_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/1/1b/Platinum_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/0/01/Diamond_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/5/53/Ascendant_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/0/0b/Immortal_3_Rank.png",
            "https://static.wikia.nocookie.net/valorant/images/1/1a/Radiant_Rank.png"

        ]
        self.botUsernames = [
            "BennyBot",
            "LexiBot",
            "MiloBot",
            "OllieBot",
            "ZaraBot",
            "TobyBot",
            "LumiBot",
            "EddieBot",
            "FinnBot",
            "RoryBot",
            "LanaBot",
            "NiaBot",
            "JunoBot",
            "TheoBot",
            "IvyBot",
            "KaiBot",
            "TessaBot",
            "ZekeBot",
            "MaxiBot",
            "PennyBot",
            "NovaBot",
            "RemyBot",
            "FelixBot",
            "SamiBot",
            "ArloBot",
            "LucaBot",
            "EllaBot",
            "JoeyBot",
            "NicoBot",
            "TillyBot",
            "DaisyBot",
            "MacyBot",
            "HugoBot",
            "SunnyBot",
            "MiraBot",
            "OttoBot",
            "TrixiBot",
            "ViviBot",
            "RosieBot",
            "BasilBot",
            "LennyBot",
            "CleoBot",
            "EmmyBot",
            "NoahBot",
            "RubyBot",
            "GigiBot",
            "JessBot",
            "ZionBot",
            "MonaBot",
            "TobyBot"
        ]

        self.party = None
        self.viewer = viewerObj
        self.PFP = self.OFFLINE_PFP
        self.userName = viewerObj.privateData.userName if viewerObj is not None else username if username else choice(self.botUsernames)
        self.state = PlayerStatus.OFFLINE
        self.level = 1
        self.currentXP = 0
        self.levelXP = 0
        self.hiddenMMR = 0
        self.rank = ""

        self.quizQuestions:dict[str, Question] = {}
        self.score = 0
        self.correct = 0
        self.incorrect = 0
        self.unattempted = 0
        self.healthImpact = 0

        self.friends = []
        self.incomingFriendRequests = {}
        self.outgoingFriendRequests = {}

        self.incomingPartyJoinRequests = {}
        self.outgoingPartyJoinRequests = {}

        self.incomingPartyInvites = {}
        self.outgoingPartyInvites = {}

    def setXP(self, xp):
        xp_list = [
        100, 280, 520, 800, 1120, 1470, 1850, 2260, 2700, 3160,
        3650, 4160, 4690, 5240, 5810, 6400, 7010, 7640, 8280, 8940,
        9620, 10320, 11030, 11760, 12500, 13260, 14030, 14820, 15620, 16430,
        17260, 18100, 18960, 19820, 20710, 21600, 22510, 23420, 24360, 25300,
        26250, 27220, 28200, 29190, 30190, 31200, 32220, 33260, 34300, 35360,
        36420, 37500, 38580, 39680, 40790, 41910, 43030, 44170, 45320, 46480,
        47640, 48820, 50000, 51200, 52400, 53620, 54840, 56070, 57320, 58570,
        59820, 61090, 62370, 63660, 64950, 66260, 67570, 68890, 70220, 71550,
        72900, 74250, 75620, 76990, 78370, 79750, 81150, 82550, 83960, 85380,
        86810, 88240, 89680, 91140, 92590, 94060, 95530, 97020, 98500, 100000
        ]
        total_xp = 0
        for level, xp_needed in enumerate(xp_list, start=1):
            if xp < total_xp + xp_needed:
                self.level = level
                self.currentXP = xp - total_xp
                self.levelXP = xp_needed
                return
            total_xp += xp_needed
        self.level = len(xp_list)
        self.currentXP = xp - total_xp
        self.levelXP = xp_list[-1]
    def setVisibleMMR(self, visibleMMR):
        MMRList = [100, 280, 520, 800, 1120, 1470, 1850, 2260, 2700]
        total_MMR = 0
        for rankIndex, mmr_needed in enumerate(MMRList, start=1):
            if visibleMMR < total_MMR + mmr_needed:
                self.rank = self.rankImages[rankIndex-1]
                return
            total_MMR += mmr_needed
        self.rank = self.rankImages[-1]
    def setStatus(self, status):
        self.state = status
    def getStatus(self):
        return self.state
    def setPFP(self):
        self.PFP = choice(self.PFP_LIST)
    def removePFP(self):
        self.PFP = self.OFFLINE_PFP
    def displayPFP(self):
        return self.PFP
    def displayUserName(self):
        return self.userName
    def displayState(self):
        return self.state
    def displayLevel(self):
        return f"Level {self.level}"
    def displayRank(self):
        return self.rank
    def __gt__(self, other):
        return self.score > other.score
    def __lt__(self, other):
        return self.score < other.score


class SocialInteraction:
    def __init__(self, interactionType:Interactions, sender:Player, receiver:Player, party=None):
        self.sender = sender
        self.receiver = receiver
        self.interactionType = interactionType
        self.ID = f"{sender.userName}-{self.interactionType}"
        self.party = party
        self.active = True
    def sendToReceiver(self):
        if self.receiver.viewer and self.active: self.receiver.viewer.sendCustomMessage(CustomMessages.newSocialInteraction(self.sender.userName, self.ID, self.interactionType))
    def destroy(self):
        if self.receiver.viewer and self.active:
            self.receiver.viewer.sendCustomMessage(CustomMessages.deleteInteraction(self.ID))
            self.active = False
