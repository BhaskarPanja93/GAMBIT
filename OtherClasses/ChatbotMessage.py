from datetime import datetime
from randomisedString import RandomisedString


class ChatbotMessageSenders:
    user = "user"
    assistant = "assistant"
    system = "system"
    tool = "tool"


class ChatbotMessage:
    def __init__(self, sender: ChatbotMessageSenders, message: str, isComplete:bool):
        self.id = RandomisedString().AlphaNumeric(5, 5)
        self.time = datetime.now()
        self.sender = sender
        self.message = message
        self.isComplete = isComplete
    def export(self):
        return {"role": self.sender, "content": self.message}
