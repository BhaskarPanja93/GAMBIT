from random import shuffle

from randomisedString import RandomisedString
from time import time

class Option:
    def __init__(self, realIndex, text, isCorrect):
        self.optionID = RandomisedString().AlphaNumeric(2,4)
        self.realIndex = realIndex
        self.text = text
        self.isCorrect = isCorrect


class Question:
    def __init__(self, questionID:str, text:str, rawOptions:list, correct:list[int]):
        self.generatedAt = time()
        self.questionID = questionID
        self.text = text
        self.options:list[Option] = []
        self.maxOptions = 4
        shuffle(correct)
        option = rawOptions.pop(correct[0])
        self.options.append(Option(correct, option, True))
        for index in range(len(rawOptions)): self.options.append(Option(index, rawOptions[index], index in correct))
        while len(self.options) > self.maxOptions:
            shuffle(self.options)
            if not self.options[-1].isCorrect:
                self.options.pop()
    def fetchOption(self, optionID:str):
        for option in self.options:
            if option.optionID == optionID:
                return option