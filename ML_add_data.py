import secrets
from math import exp
from threading import Thread
from time import sleep

from pooledMySQL import PooledMySQL

MySQLPool = PooledMySQL("gambit", "SimplePassword@69", "gambit", "bhindi1.ddns.net")
MySQLPool.execute("truncate ml_train")

class Person:
    def __init__(self, personID):
        self.personID = personID
        self.placementQuestionsCompleted:int = 0
        self.hiddenMMR = secrets.choice(range(1, 1000)) / 1000
        self.goodMood = secrets.choice(range(1, 100))

class Question:
    def __init__(self, questionID):
        self.questionID = questionID
        self.correctOption = secrets.choice(range(1, 5))
        self.toughness = secrets.choice(range(1, 100)) / 100

class Answer:
    def __init__(self, person: Person, question: Question):
        self.person = person
        self.question = question
        self.timeTaken = max(0, min(30, (int(15 * (1 - person.hiddenMMR) + 15 * question.toughness))))
        person.goodMood += secrets.choice(range(-1, 2))*secrets.randbelow(100000) / 100000
        self.optionSelected = secrets.choice(range(1, 5)) if (secrets.randbelow(1000000) / 1000000) > (self.success_probability()) else question.correctOption

    def success_probability(self):
        mood_factor = self.person.goodMood / 100
        hiddenMMR_factor = self.person.hiddenMMR
        difficulty_factor = self.question.toughness
        return exp(-difficulty_factor) * (hiddenMMR_factor * 0.7 + mood_factor * 0.3)

people: dict[int, Person] = {personID: Person(personID) for personID in range(1, 500)}
questions: dict[int, Question] = {questionID: Question(questionID) for questionID in range(1, 500)}

records = []
peopleKeys = list(people)
maxPlacements = 10
while peopleKeys:
    personID = secrets.choice(peopleKeys)
    person = people[personID]
    questionKeys = list(questions.keys())
    while questionKeys:
        isPlacementQuiz = int(person.placementQuestionsCompleted < maxPlacements)
        placement_question_modifier = maxPlacements - person.placementQuestionsCompleted
        if isPlacementQuiz:
            person.placementQuestionsCompleted += 1
            placement_question_modifier *= 4

        questionID = secrets.choice(questionKeys)
        question = questions[questionID]
        answer = Answer(person, question)
        isCorrect = 1 if answer.optionSelected == question.correctOption else 0

        if isCorrect:
            difficulty_modifier = question.toughness
            hiddenMMR_modifier = 1 - person.hiddenMMR
            time_modifier = (30 - answer.timeTaken) / 30
            correct_modifier = 1
        else:
            difficulty_modifier = 1 - question.toughness
            hiddenMMR_modifier = person.hiddenMMR
            time_modifier = (30 - answer.timeTaken) / 30
            correct_modifier = - 1

        MMROffset = (placement_question_modifier + 1) * time_modifier * hiddenMMR_modifier * difficulty_modifier * correct_modifier / 100

        #print(f"{isCorrect=}\ntimeTaken={answer.timeTaken}\nhiddenMMR={person.hiddenMMR * 1000}\ntoughness={question.toughness * 100}%\n{MMROffset*1000=}\nplacements={person.placementQuestionsCompleted}/{maxPlacements}")

        person.hiddenMMR = max(0, min(1, person.hiddenMMR + MMROffset))

        visibleMMR = int(person.hiddenMMR * 1000)

        values = [
            personID,
            person.placementQuestionsCompleted,
            answer.timeTaken,
            questionID,
            answer.optionSelected,
            question.correctOption,
            int(person.hiddenMMR * 1000),
            int(question.toughness * 100),
            MMROffset,
        ]
        #input()
        print(values)
        Thread(target=MySQLPool.execute, args=("INSERT INTO ml_train VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", values,)).start()
        #MySQLPool.execute("INSERT INTO ml_train VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
        #input()
        sleep(0.001)
