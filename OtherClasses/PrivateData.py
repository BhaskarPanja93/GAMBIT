from datetime import datetime

from OtherClasses.Pages import Pages

class PrivateData:
    def __init__(self):
        self.activeSince = datetime.now()
        self.expectedPostAuthPage = Pages.LOBBY
        self.baseURI = ""
        self.userID = ""
        self.userName = ""
        self.player = None
        self.party = None
        self.pagesHistory = []
        self.renderedElements = set()
        self.renderedScripts = set()

    def isScriptRendered(self, name):
        if name not in self.renderedScripts:
            self.renderedScripts.add(name)
            return False
        else:
            return True

    def isElementRendered(self, name):
        if name not in self.renderedElements:
            self.renderedElements.add(name)
            return False
        else:
            return True

    def newPage(self, name):
        self.pagesHistory.append(name)

    def currentPage(self):
        return self.pagesHistory[-1] if len(self.pagesHistory) else None