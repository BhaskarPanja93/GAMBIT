from datetime import datetime

from OtherClasses.Pages import Pages


class PrivateData:
    def __init__(self):
        self.activeSince = datetime.now()
        self.expectedPostAuthPage = Pages.LOBBY
        self.baseURI = ""
        self.userName = ""
        self.player = None
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
            return False
        else:
            return True

    def renderScript(self, name):
        self.renderedScripts.add(name)

    def removeScript(self, name):
        self.renderedScripts.remove(name)
    def renderElement(self, name):
        self.renderedElements.add(name)

    def removeElement(self, name):
        self.renderedElements.remove(name)

    def newPage(self, name):
        self.pagesHistory.append(name)

    def currentPage(self):
        return self.pagesHistory[-1] if len(self.pagesHistory) else None