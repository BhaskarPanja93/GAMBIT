from jinja2 import Template
from randomisedString import RandomisedString
from time import time, sleep

from OtherClasses.CachedElements import CachedElements
from OtherClasses.DivIDs import DivID
from OtherClasses.FileNames import FileNames
from OtherClasses.Matchmaker import Match
from OtherClasses.Pages import Pages
from OtherClasses.Player import Player
from internal.dynamicWebsite import DynamicWebsite


class Quiz:
    def __init__(self, match: Match, onQuizEnd, cachedElements: CachedElements):
        self.quizID = RandomisedString().AlphaNumeric(30,30)
        self.createdAt = time()
        self.endAt = None
        self.match = match
        self.onQuizEnd = onQuizEnd
        self.questionHistory = []
        self.cachedElements = cachedElements

    def start(self):
        pass

    def prepareQuestion(self):
        pass
    def showPlayers(self):
        for party in self.match.teamA.parties:
            for player in party.players:
                if player.viewer is not None:
                    player.viewer.updateHTML(Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizQuestion)).render(baseURI=player.viewer.privateData.baseURI), DivID.quizContent, DynamicWebsite.UpdateMethods.update)

        for party in self.match.teamB.parties:
            for player in party.players:
                if player.viewer is not None:
                    player.viewer.updateHTML(Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizQuestion)).render(baseURI=player.viewer.privateData.baseURI), DivID.quizContent, DynamicWebsite.UpdateMethods.update)

    def showPreQuestion(self):
        pass
    def showQuestion(self):
        pass
    def endQuestion(self):
        pass
    def showEndPage(self):
        pass
    def end(self):
        self.showEndPage()

