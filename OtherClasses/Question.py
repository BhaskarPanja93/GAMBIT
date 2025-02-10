from randomisedString import RandomisedString


class Option:
    def __init__(self, realIndex, text):
        self.realIndex = realIndex
        self.text = text
        self.modifiedIndices = RandomisedString().AlphaNumeric(2,4)


class Question:
    def __init__(self, text:str, rawOptions:list[str], correct:list[int]):
        self.text = text
        self.rawOptions = rawOptions
        self.correct = correct
        self.modifiedOptions:list[Option] = []
        for optionIndex in range(len(self.rawOptions)): self.modifiedOptions.append(Option(optionIndex, self.rawOptions[optionIndex]))
