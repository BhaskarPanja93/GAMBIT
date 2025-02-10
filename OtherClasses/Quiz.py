from random import shuffle
from time import time, sleep

from jinja2 import Template
from pooledMySQL import PooledMySQL
from randomisedString import RandomisedString

from OtherClasses.CachedElements import CachedElements
from OtherClasses.DivIDs import DivID
from OtherClasses.FileNames import FileNames
from OtherClasses.Matchmaker import Match
from OtherClasses.Player import Player
from OtherClasses.Question import Question
from internal.dynamicWebsite import DynamicWebsite


class Quiz:
    def __init__(self, match: Match, onQuizEnd, cachedElements: CachedElements, SQLconn:PooledMySQL):
        self.quizID = RandomisedString().AlphaNumeric(30,30)
        self.createdAt = time()
        self.endAt = None
        self.match = match
        self.onQuizEnd = onQuizEnd
        self.questionHistory:list[Question] = []
        self.allowAnswersFrom:list[Player] = []
        self.SQLconn = SQLconn
        self.crowns:list[Player] = []
        self.cachedElements = cachedElements
        self.timePerQuestion = 5

    def start(self):
        lastAllowed = self.allowAnswersFrom
        self.allowAnswersFrom = []
        for player in list(self.match.teamA.allPlayers())+list(self.match.teamB.allPlayers()):
            if player in lastAllowed or len(lastAllowed)==0:
                self.allowAnswersFrom.append(player)
        self.sortPlayersByScore()
        self.updateNavbar()
        self.prepareQuestion()

    def prepareQuestion(self):
        question = Question(RandomisedString().AlphaNumeric(10,10), "1+1=",[1,2,3,4,5,6,7,8], [1])
        self.questionHistory.append(question)
        self.showPreQuestion()

    def updateNavbar(self):
        def renderPlayer(player, toSend):
            isAlly = player.party.team==toSend.party.team
            if isAlly: toSend.viewer.updateHTML(player.displayAsTeam(player in self.crowns), f"team-player-{index}", DynamicWebsite.UpdateMethods.update)
            else: toSend.viewer.updateHTML(player.displayAsOpponent(player in self.crowns), f"opponent-player-{index}", DynamicWebsite.UpdateMethods.update)
        teamAHealth = max(0,min(100,int(self.match.teamA.health)))
        teamBHealth = max(0,min(100,int(self.match.teamB.health)))
        for toSend in list(self.match.teamA.allPlayers())+list(self.match.teamB.allPlayers()):
            if toSend.viewer is not None:
                if self.match.teamB == toSend.party.team:
                    toSend.viewer.updateHTML(f"""{teamBHealth}""", f"team-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-red-500 h-full" style="width: {teamBHealth}%;"></div>""", f"team-health-bar", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""{teamAHealth}""", f"opponent-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-red-500 h-full" style="width: {teamAHealth}%;"></div>""", f"opponent-health-bar", DynamicWebsite.UpdateMethods.update)
                else:
                    toSend.viewer.updateHTML(f"""{teamBHealth}""", f"opponent-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-red-500 h-full" style="width: {teamBHealth}%;"></div>""", f"opponent-health-bar", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""{teamAHealth}""", f"team-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-red-500 h-full" style="width: {teamAHealth}%;"></div>""", f"team-health-bar", DynamicWebsite.UpdateMethods.update)
                for index in range(3):
                    if len(list(self.match.teamA.allPlayers()))>=index:
                        player = list(self.match.teamA.allPlayers())[index]
                        renderPlayer(player, toSend)
                    if len(list(self.match.teamB.allPlayers()))>=index:
                        player = list(self.match.teamB.allPlayers())[index]
                        renderPlayer(player, toSend)

    def showPreQuestion(self):
        self.showQuestion()

    def showQuestion(self):
        for party in self.match.teamA.parties+self.match.teamB.parties:
            for player in party.players:
                if player.viewer is not None:
                    question = self.questionHistory[-1]
                    shuffle(question.options)
                    temp = Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizQuestion))
                    player.viewer.updateHTML(temp.render(baseURI=player.viewer.privateData.baseURI, question=question, option=question.options), DivID.quizContent, DynamicWebsite.UpdateMethods.update)
        self.countDown()

    def countDown(self):
        for _ in range(self.timePerQuestion, -1, -1):
            for toSend in list(self.match.teamA.allPlayers())+list(self.match.teamB.allPlayers()):
                if toSend.viewer: toSend.viewer.updateHTML(str(_), DivID.quizTimer, DynamicWebsite.UpdateMethods.update)
            sleep(1)
        self.endQuestion()

    def endQuestion(self):
        question = self.questionHistory[-1]
        for player in self.allowAnswersFrom:
            optionData = player.optionsSelected.get(question.questionID)
            if optionData:
                optionSelected = question.fetchOption(optionData.get("OPTION_ID"))
                timeTaken = optionData.get("TIME", question.generatedAt+5) - question.generatedAt
                player.optionsSelected[question.questionID] = optionSelected
                if optionSelected.isCorrect:
                    player.score += 10 * (self.timePerQuestion - timeTaken)
                    player.party.team.health += 1.5 * (self.timePerQuestion - timeTaken)
                else:
                    player.score -= 5 * timeTaken
                    player.party.team.health -= len(self.questionHistory) * 1.5 * timeTaken
            else:
                player.score -= 5
                player.party.team.health -= len(self.questionHistory) * 1.5
        if self.match.teamA.health<=0 or self.match.teamB.health<=0: self.end()
        else: self.start()

    def sortPlayersByScore(self):
        highestScore = 0
        for player in list(self.match.teamA.allPlayers())+list(self.match.teamB.allPlayers()):
            if player.score > highestScore:
                highestScore = player.score
                self.crowns = [player]
            elif player.score == highestScore:
                self.crowns.append(player)

    def showEndPage(self):
        pass

    def end(self):
        self.endAt = time()
        self.showEndPage()

    def saveToDB(self):
        pass

