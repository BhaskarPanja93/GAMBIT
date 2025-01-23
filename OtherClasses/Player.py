from randomisedString import RandomisedString

class Player:
    def __init__(self):
        self.PFP = "https://i.pinimg.com/originals/e4/3d/2d/e43d2dea1d8793fcf016d2a634bdf761.png"
        self.userName = RandomisedString().AlphaNumeric(5, 10)
        self.status = "status-"+RandomisedString().AlphaNumeric(5, 5)

    def displayPFP(self):
        return self.PFP
    def displayUserName(self):
        return self.userName
    def displayStatus(self):
        return self.status