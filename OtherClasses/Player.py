from randomisedString import RandomisedString

class Player:
    def __init__(self, viewerObj = None):
        self.viewer = viewerObj
        self.PFP = "https://i.pinimg.com/originals/e4/3d/2d/e43d2dea1d8793fcf016d2a634bdf761.png"
        self.userName = "username-"+RandomisedString().AlphaNumeric(5, 5)
        self.state = "status-" + RandomisedString().AlphaNumeric(5, 5)
        self.level = 5
        self.rank = "https://static.wixstatic.com/media/cb04e9_db781b062c6d4d02b1d5dbaf314ad2ef~mv2.png/v1/fill/w_256,h_256,al_c,q_85,enc_auto/cb04e9_db781b062c6d4d02b1d5dbaf314ad2ef~mv2.png"


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