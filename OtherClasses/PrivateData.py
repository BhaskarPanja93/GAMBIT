from datetime import datetime

from OtherClasses.Pages import Pages

class PrivateData:
    def __init__(self):
        self.activeSince = datetime.now()
        self.expectedPostAuthPage = Pages.lobby
        self.userID = ""
        self.currentPage = ""
        self.player = None
        self.party = None
        self.friendsRendered = False
