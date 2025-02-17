from __future__ import annotations
from random import shuffle, randrange

from randomisedString import RandomisedString
from time import time


class Option:
    def __init__(self, realIndex, text, isCorrect):
        self.optionID = RandomisedString().AlphaNumeric(2,4)
        self.realIndex = realIndex
        self.text = text
        self.isCorrect = isCorrect


class Question:
    def __init__(self, questionNumber:int|None, questionID:str|None, text:str|None, optionList:list|None, correctIndices:list[int]|None):
        self.questionNumber = questionNumber
        self.questionID = questionID
        self.text = text
        self.optionList = optionList
        self.correctIndices = correctIndices
        self.options:list[Option] = []
        self.maxOptions = 4
        self.selectedOption: Option | None = None
        self.maxTime = 8
        self.startTime = time()
        self.timeTaken = randrange(self.maxTime-3, self.maxTime+3)

    def prepare(self):
        shuffle(self.correctIndices)
        optionText = self.optionList.pop(self.correctIndices[0])
        self.correctIndices.remove(0)
        self.options.append(Option(self.correctIndices, optionText, True))
        for index in range(len(self.optionList)): self.options.append(Option(index, self.optionList[index], index in self.correctIndices))
        while len(self.options) > self.maxOptions:
            shuffle(self.options)
            if not self.options[-1].isCorrect:
                self.options.pop()

    def fetchOption(self, optionID:str):
        for option in self.options:
            if option.optionID == optionID:
                return option

    def replicate(self):
        new = Question(None, None, None, None, None)
        new.questionNumber = self.questionNumber
        new.questionID = self.questionID
        new.text = self.text
        new.options = [_ for _ in self.options]
        new.maxOptions = self.maxOptions
        new.selectedOption = self.selectedOption
        new.maxTime = self.maxTime
        new.startTime = self.startTime
        new.timeTaken = randrange(self.maxTime-3, self.maxTime+3)
        return new
