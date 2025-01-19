from OtherClasses.Folders import Folders
from OtherClasses.FileNames import FileNames

class CachedElements:
    def __init__(self):
        self.knownHTMLElements:dict[str, dict[str, str]] = {}


    def fetchStaticHTML(self, itemName: str) -> str:
        if "HTML" not in self.knownHTMLElements: self.knownHTMLElements["HTML"] = {}
        if itemName not in self.knownHTMLElements["HTML"]:
            self.knownHTMLElements["HTML"][itemName] = open(Folders.html/itemName, "r").read()
        return self.knownHTMLElements["HTML"].get(itemName)

    def fetchStaticJS(self, itemName: str) -> str:
        if "JS" not in self.knownHTMLElements: self.knownHTMLElements["JS"] = {}
        if itemName not in self.knownHTMLElements["JS"]:
            self.knownHTMLElements["JS"][itemName] = open(Folders.js/itemName, "r").read()
        return self.knownHTMLElements["JS"].get(itemName)

    def fetchStaticCSS(self, itemName: str) -> str:
        if "CSS" not in self.knownHTMLElements: self.knownHTMLElements["CSS"] = {}
        if itemName not in self.knownHTMLElements["CSS"]:
            self.knownHTMLElements["CSS"][itemName] = open(Folders.css/itemName, "r").read()
        return self.knownHTMLElements["CSS"].get(itemName)


    def createAuthForm(self, registerCSRF: str, loginCSRF: str):
        return (self.fetchStaticHTML(FileNames.HTML.AuthForm)
                .replace("REPLACE_REGISTER_CSRF", registerCSRF)
                .replace("REPLACE_LOGIN_CSRF", loginCSRF))

