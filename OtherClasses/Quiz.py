from json import loads
from random import shuffle, choice
from time import time, sleep

from jinja2 import Template
from pooledMySQL import PooledMySQL
from randomisedString import RandomisedString

from OtherClasses.CachedElements import CachedElements
from OtherClasses.Database import Database
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
        self.questionHistory:dict[str, Question] = {}
        self.currentQuestionID = None
        self.allowAnswersFrom = []
        self.SQLconn = SQLconn
        self.crowns:list[Player] = []
        self.cachedElements = cachedElements
        self.match.quiz = self

    def updateVisuals(self):
        self.sortPlayersByScore()
        self.updateNavbar()

    def start(self):
        lastAllowedPlayers = self.allowAnswersFrom
        self.allowAnswersFrom = []
        for player in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
            if player in lastAllowedPlayers or len(lastAllowedPlayers)==0:
                self.allowAnswersFrom.append(player)
        if self.allowAnswersFrom:
            if not self.questionHistory: self.updateVisuals()
            self.prepareQuestion()

    def prepareQuestion(self):
        QRaw = self.SQLconn.execute(f"SELECT * FROM {Database.QUESTION.TABLE_NAME} ORDER BY RAND() LIMIT 1")[0]
        QRaw[Database.QUESTION.QUESTION_ID] = QRaw[Database.QUESTION.QUESTION_ID].decode()
        if QRaw[Database.QUESTION.QUESTION_ID] in self.questionHistory: return self.prepareQuestion()
        question = Question(len(self.questionHistory)+1, QRaw[Database.QUESTION.QUESTION_ID], QRaw[Database.QUESTION.TEXT], loads(QRaw[Database.QUESTION.OPTIONS]), loads(QRaw[Database.QUESTION.CORRECT]))
        question.prepare()
        self.questionHistory[question.questionID] = question
        self.currentQuestionID = question.questionID
        for player in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
            player.quizQuestions[question.questionID] = question.replicate()
            shuffle(player.quizQuestions[question.questionID].options)
        self.showPreQuestion()

    def updateNavbar(self):
        def renderPlayer(player, toSend):
            isAlly = player.party.team==toSend.party.team
            if isAlly: toSend.viewer.updateHTML(player.displayAsTeam(player in self.crowns), f"team-player-{index}", DynamicWebsite.UpdateMethods.update)
            else: toSend.viewer.updateHTML(player.displayAsOpponent(player in self.crowns), f"opponent-player-{index}", DynamicWebsite.UpdateMethods.update)
        teamAHealth = round(self.match.teamA.health, 2)
        teamBHealth = round(self.match.teamB.health, 2)
        for toSend in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
            if toSend.viewer is not None:
                if self.match.teamB == toSend.party.team:
                    toSend.viewer.updateHTML(f"""{teamBHealth}%""", f"team-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-green-500 h-full" style="width: {teamBHealth}%;"></div>""", f"team-health-bar", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""{teamAHealth}%""", f"opponent-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-red-500 h-full" style="width: {teamAHealth}%;"></div>""", f"opponent-health-bar", DynamicWebsite.UpdateMethods.update)
                else:
                    toSend.viewer.updateHTML(f"""{teamBHealth}%""", f"opponent-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-red-500 h-full" style="width: {teamBHealth}%;"></div>""", f"opponent-health-bar", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""{teamAHealth}%""", f"team-health", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML(f"""<div class="bg-green-500 h-full" style="width: {teamAHealth}%;"></div>""", f"team-health-bar", DynamicWebsite.UpdateMethods.update)
                for index in range(3):
                    toSend.viewer.updateHTML("", f"team-player-{index}", DynamicWebsite.UpdateMethods.update)
                    toSend.viewer.updateHTML("", f"opponent-player-{index}", DynamicWebsite.UpdateMethods.update)
                    try: renderPlayer(self.match.teamA.allPlayers()[index], toSend)
                    except: pass
                    try: renderPlayer(self.match.teamB.allPlayers()[index], toSend)
                    except: pass

    def showPreQuestion(self):
        self.showQuestion()

    def showPostQuestion(self, lastQuestionID):
        if self.questionHistory:
            for player in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
                if player.viewer is not None:
                    questionInstance = player.quizQuestions[lastQuestionID]
                    for index in range(4):
                        temp = Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizOption))
                        if questionInstance.selectedOption is not None and questionInstance.selectedOption.optionID == questionInstance.options[index].optionID: isSelected = True
                        else: isSelected = False
                        player.viewer.updateHTML(temp.render(baseURI=player.viewer.privateData.baseURI, index=index, option=questionInstance.options[index], showAnswer=True, isSelected=isSelected), f"{DivID.quizOption}{index}", DynamicWebsite.UpdateMethods.replace)
            sleep(2)

    def showQuestion(self):
        for player in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
            if player.viewer is not None:
                temp = Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizQuestion))
                player.viewer.updateHTML(temp.render(baseURI=player.viewer.privateData.baseURI, question=player.quizQuestions[self.currentQuestionID]), DivID.quizContent, DynamicWebsite.UpdateMethods.update)
        sleep(1)
        for player in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
            if player.viewer is not None:
                for index in range(4):
                    temp = Template(self.cachedElements.fetchStaticHTML(FileNames.HTML.QuizOption))
                    player.viewer.updateHTML(temp.render(baseURI=player.viewer.privateData.baseURI, index=index, option=player.quizQuestions[self.currentQuestionID].options[index], showAnswer=False, isSelected=False), f"{DivID.quizOption}{index}", DynamicWebsite.UpdateMethods.replace)
            player.quizQuestions[self.currentQuestionID].startTime = time()
        self.countDown()

    def countDown(self):
        for _ in range(self.questionHistory[self.currentQuestionID].maxTime, -1, -1):
            for toSend in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
                if toSend.viewer: toSend.viewer.updateHTML(str(_), DivID.quizTimer, DynamicWebsite.UpdateMethods.update)
            sleep(1)
        self.endQuestion()

    def endQuestion(self):
        lastQuestionID = self.currentQuestionID
        self.currentQuestionID = None
        for player in self.allowAnswersFrom:
            if player.viewer is None:
                player.quizQuestions[lastQuestionID].selectedOption = choice(player.quizQuestions[lastQuestionID].options)
                player.quizQuestions[lastQuestionID].timeTaken = time() - player.quizQuestions[lastQuestionID].startTime
            questionInstance:Question = player.quizQuestions.get(lastQuestionID)
            if questionInstance.selectedOption is None:
                scoreChange = -3
                healthImpact = -questionInstance.questionNumber * 2
                player.unattempted += 1
                player.score += scoreChange
                player.healthImpact += healthImpact
                player.party.team.health += healthImpact
            elif questionInstance.selectedOption.isCorrect:
                scoreChange = 5 * (questionInstance.maxTime - questionInstance.timeTaken)
                healthImpact = (questionInstance.maxTime - questionInstance.timeTaken) * len(self.questionHistory)
                player.correct += 1
                player.score += scoreChange
                player.healthImpact += healthImpact
                player.party.team.health += healthImpact
            else:
                scoreChange = -questionInstance.timeTaken
                healthImpact = -len(self.questionHistory) * questionInstance.timeTaken /2
                player.incorrect += 1
                player.score += scoreChange
                player.healthImpact += healthImpact
                player.party.team.health += healthImpact

        if self.questionHistory: self.updateVisuals()
        self.showPostQuestion(lastQuestionID)
        if 100<=self.match.teamA.health or self.match.teamA.health<=0 or 100<=self.match.teamB.health or self.match.teamB.health<=0: self.end()
        else: self.start()

    def sortPlayersByScore(self):
        highestScore = 0
        for player in self.match.teamA.allPlayers()+self.match.teamB.allPlayers():
            if player.score > highestScore:
                highestScore = player.score
                self.crowns = [player]
            elif player.score == highestScore:
                self.crowns.append(player)

    def end(self):
        if self.match.teamB.health > self.match.teamA.health: self.match.teamB.winner = True
        else: self.match.teamA.winner = True
        self.endAt = time()
        self.onQuizEnd(self)

    def saveToDB(self):
        pass

