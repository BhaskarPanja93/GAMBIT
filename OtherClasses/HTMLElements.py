from OtherClasses.Folders import Folders
from OtherClasses.FileNames import FileNames

class HTMLElements:
    def __init__(self):
        self.knownHTMLElements:dict[str, str] = {}


    def fetchStatic(self, itemName: str) -> str:
        if itemName not in self.knownHTMLElements:
            self.knownHTMLElements[itemName] = open(f"{Folders.html}{itemName}", "r").read()
        return self.knownHTMLElements.get(itemName)


    def createAuthForm(self, registerCSRF: str, loginCSRF: str):
        return (self.fetchStatic(FileNames.HTML.AuthForm)
                .replace("REPLACE_REGISTER_CSRF", registerCSRF)
                .replace("REPLACE_LOGIN_CSRF", loginCSRF))

