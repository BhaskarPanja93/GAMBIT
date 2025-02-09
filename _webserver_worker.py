from gevent import monkey

monkey.patch_all()

from time import time, sleep
from sys import argv
from typing import Any
from flask import request, redirect, make_response
from jinja2 import Template
from argon2 import PasswordHasher
from threading import Thread

from OtherClasses.Quiz import Quiz
from OtherClasses.PrivateData import PrivateData
from OtherClasses.Matchmaker import Matchmaker, Match
from OtherClasses.FileNames import FileNames
from OtherClasses.Database import Database
from OtherClasses.CachedElements import CachedElements
from OtherClasses.CoreValues import CoreValues
from OtherClasses.DivIDs import DivID
from OtherClasses.Pages import Pages
from OtherClasses.Player import Player
from OtherClasses.Party import Party
from OtherClasses.Routes import Routes
from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.CommonFunctions import connectDB, WSGIRunner

from customisedLogs import CustomisedLogs
from internal.dynamicWebsite import DynamicWebsite



##############################################################################################################################
# NAVBAR


def renderBaseNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.BaseNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.BaseNavbar)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.BaseNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar1, UpdateMethods.update)


def removeBaseNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.BaseNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.BaseNavbar)
        viewerObj.updateHTML("", DivID.navbar1, UpdateMethods.update)


def renderLobbyNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.LobbyNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.LobbyNavbar)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar2, UpdateMethods.update)


def removeLobbyNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.LobbyNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.LobbyNavbar)
        viewerObj.updateHTML("", DivID.navbar2, UpdateMethods.update)



def renderQuizNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.QuizNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.QuizNavbar)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.QuizNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar2, UpdateMethods.update)


def removeQuizNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.QuizNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.QuizNavbar)
        viewerObj.updateHTML("", DivID.navbar2, UpdateMethods.update)


##############################################################################################################################
# GHOST ELEMENT


def renderGhost3D(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.Ghost3d):
        viewerObj.privateData.renderElement(FileNames.HTML.Ghost3d)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Ghost3d)).render(baseURI=viewerObj.privateData.baseURI), DivID.ghost3d, UpdateMethods.update)


##############################################################################################################################
# AUTH PAGES


def __renderAuthStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() not in [Pages.AUTH, Pages.PRE_AUTH, Pages.POST_AUTH]:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
        renderGhost3D(viewerObj)


def renderAuthPre(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    renderBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    hideSocials(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.PRE_AUTH:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPre)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.PRE_AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.PRE_AUTH))


def renderAuthForms(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    renderBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    hideSocials(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.AUTH:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthForms)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.AUTH))
        sendLoginForm(viewerObj)
        sendRegisterForm(viewerObj)


def renderAuthPost(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    renderBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    showSocials(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.POST_AUTH:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPost)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.POST_AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.POST_AUTH))


##############################################################################################################################
# CHAT ELEMENTS


def renderChatStructure(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.ChatFull):
        viewerObj.privateData.renderElement(FileNames.HTML.ChatFull)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.ChatFull)).render(baseURI=viewerObj.privateData.baseURI), DivID.chatBox, UpdateMethods.update)


##############################################################################################################################
# MUSIC TRAY


def renderMusicTray(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.MusicTray)).render(baseURI=viewerObj.privateData.baseURI), DivID.musicTrayHolder, UpdateMethods.update)


##############################################################################################################################
# FRIEND ELEMENTS


def showSocials(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.SocialsStructure):
        viewerObj.privateData.renderElement(FileNames.HTML.SocialsStructure)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.SocialsStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.socialStructure, UpdateMethods.update)
    viewerObj.sendCustomMessage(CustomMessages.toggleSocials(True))
    # friendList = SQLconn.execute(f"""SELECT
    # CASE
    #     WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
    #     WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
    # END AS result
    # FROM {Database.FRIEND.TABLE_NAME};""", [viewerObj.privateData.userID, viewerObj.privateData.userID])
    others = []
    for _ in range(15):
        #sleep(1)
        other = Player(None, str(_))
        others.append(other)
        viewerObj.sendCustomMessage(CustomMessages.friendAdded(other.displayUserName(), other.displayPFP(), other.displayState()))

    # for other in others:
    #     sleep(1)
    #     viewerObj.updateHTML("", other.connectionID, UpdateMethods.remove)
    #     viewerObj.sendCustomMessage()
def hideSocials(viewerObj: DynamicWebsite.Viewer):
    viewerObj.sendCustomMessage(CustomMessages.toggleSocials(False))


##############################################################################################################################
# LOBBY PAGES


def __renderLobbyStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() != Pages.LOBBY:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyFeatures)).render(baseURI=viewerObj.privateData.baseURI), DivID.lobbyFeatures, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.LOBBY)


def renderLobby(viewerObj: DynamicWebsite.Viewer):
    __renderLobbyStructure(viewerObj)
    renderBaseNavbar(viewerObj)
    renderLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    showSocials(viewerObj)
    viewerObj.privateData.newPage(Pages.LOBBY)
    if viewerObj.privateData.party is None:
        viewerObj.privateData.party = createParty(viewerObj.privateData.player)



##############################################################################################################################
# QUIZ PAGES


def __renderQuizStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() != Pages.QUIZ:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.QuizFull)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.LOBBY)


def renderQuiz(viewerObj: DynamicWebsite.Viewer):
    __renderQuizStructure(viewerObj)
    removeBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    renderQuizNavbar(viewerObj)
    hideSocials(viewerObj)
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.QuizQuestion)).render(baseURI=viewerObj.privateData.baseURI), DivID.quizContent, UpdateMethods.update)


##############################################################################################################################
# NOTES PAGES


def renderNotesFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.NotesFullPage)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)


def renderNotes(viewerObj: DynamicWebsite.Viewer):
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.POST_AUTH))


##############################################################################################################################
# NAVBAR


def renderBaseNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.BaseNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.BaseNavbar)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.BaseNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar1, UpdateMethods.update)


def removeBaseNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.BaseNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.BaseNavbar)
        viewerObj.updateHTML("", DivID.navbar1, UpdateMethods.update)


def renderLobbyNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.LobbyNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.LobbyNavbar)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar2, UpdateMethods.update)


def removeLobbyNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.LobbyNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.LobbyNavbar)
        viewerObj.updateHTML("", DivID.navbar2, UpdateMethods.update)



def renderQuizNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.QuizNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.QuizNavbar)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.QuizNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar2, UpdateMethods.update)


def removeQuizNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.QuizNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.QuizNavbar)
        viewerObj.updateHTML("", DivID.navbar2, UpdateMethods.update)



##############################################################################################################################
# CONTEXTUAL


def renderPreAuthUniversal(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.PreAuthUniversal):
        viewerObj.privateData.renderScript(FileNames.JS.PreAuthUniversal)
        viewerObj.updateHTML(f"<script id='{FileNames.JS.PreAuthUniversal}'>" + cachedHTMLElements.fetchStaticJS(FileNames.JS.PreAuthUniversal) + "</script>", DivID.scripts, UpdateMethods.append)
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.Trail):
        viewerObj.privateData.renderScript(FileNames.JS.Trail)
        viewerObj.updateHTML(f"<script id='{FileNames.JS.Trail}'>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Trail)+"</script>", DivID.scripts, UpdateMethods.append)
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.UniversalContainer)).render(baseURI=viewerObj.privateData.baseURI), DivID.root, UpdateMethods.update)


##############################################################################################################################
# DECIDE FIRST PAGE


def renderFirstPage(viewerObj: DynamicWebsite.Viewer, isAuthenticated: bool):
    renderPreAuthUniversal(viewerObj)
    renderMusicTray(viewerObj)
    if isAuthenticated:
        if viewerObj.privateData.player is None:
            viewerObj.privateData.player = Player(viewerObj, viewerObj.privateData.userName)
        renderChatStructure(viewerObj)
        if viewerObj.privateData.expectedPostAuthPage == Pages.LOBBY: renderLobby(viewerObj)
        elif viewerObj.privateData.expectedPostAuthPage == Pages.QUIZ: renderQuiz(viewerObj)
        #elif viewerObj.privateData.expectedPostAuthPage == Pages.marketPlace: renderMarketPlace(viewerObj)
        else: renderAuthPost(viewerObj)
    else:
        renderAuthPre(viewerObj)


##############################################################################################################################
# USER ACTIONS


def performActionPostSecurity(viewerObj: DynamicWebsite.Viewer, form: dict, isSecure:bool):
    if "PURPOSE" not in form: return
    purpose = form.pop("PURPOSE")
    if viewerObj.privateData.currentPage() not in [Pages.PRE_AUTH, Pages.AUTH]:
        if purpose == "LOGOUT":
            logoutDevice(viewerObj)
            return viewerObj.sendCustomMessage(CustomMessages.refreshBrowser())
    if viewerObj.privateData.currentPage() == Pages.AUTH:
        if purpose == "LOGIN" and isSecure:
            resetFormErrors(viewerObj)
            identifier = form.get("identifier").strip()
            password = form.get("password").strip()
            if not identifier:
                sendLoginCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.loginIdentifierError, "Invalid Username/Email")
            if not password:
                sendLoginCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.loginIdentifierError, "Invalid Password")

            accepted, reason = manualLogin(viewerObj, identifier, password)
            if accepted:
                return renderFirstPage(viewerObj, accepted)
            else:
                sendLoginCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.loginIdentifierError, reason)
        elif purpose == "REGISTER" and isSecure:
            resetFormErrors(viewerObj)
            username = form.get("user-name").strip()
            password = form.get("password").strip()
            confirmPassword = form.get("confirm-password").strip()
            email = form.get("email").strip()
            name = form.get("person-name").strip()
            if not username:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerUsernameError, "Invalid Username")
            if not password:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerPasswordError, "Invalid Password")
            if password != confirmPassword:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerPasswordError, "Passwords Do Not Match")
            if not email:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerEmailError, "Invalid Email")
            if not name:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerNameError, "Invalid Name")

            accepted, reason = createUser(viewerObj, username, password, name, email)
            if accepted:
                return renderFirstPage(viewerObj, accepted)
            else:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerGeneralError, reason)
    elif viewerObj.privateData.currentPage() == Pages.PRE_AUTH:
        if purpose == "RENDER_AUTH_FORMS":
            return renderAuthForms(viewerObj)
    elif viewerObj.privateData.currentPage() == Pages.LOBBY:
        if purpose == "PARTY_CODE":
            return viewerObj.privateData.party.generatePartyCode()
        if purpose == "PARTY_CODE_INPUT":
            newParty = partyCodes.get(form.get("CODE"))
            if newParty is not None:
                oldParty = viewerObj.privateData.party
                if oldParty.partyID != newParty.partyID:
                    viewerObj.privateData.party = newParty
                    if oldParty: oldParty.removePlayer(viewerObj.privateData.player, True)
                    return newParty.addPlayer(viewerObj.privateData.player)
        if purpose == "START_QUEUE":
            return matchmaker.addToQueue(viewerObj.privateData.party)
        if purpose == "STOP_QUEUE":
            return matchmaker.removeFromQueue(viewerObj.privateData.party)
    elif viewerObj.privateData.currentPage() in [Pages.LOBBY, Pages.NOTES]:
        return renderAuthPost(viewerObj)
    return rejectForm(viewerObj, form, "Unknown Purpose")


def rejectForm(viewerObj: DynamicWebsite.Viewer, divToTarget, reason):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.FormErrorElement)).render(errorText=reason), divToTarget, UpdateMethods.update)
    print("FORM REJECTED")


def formSubmitCallback(viewerObj: DynamicWebsite.Viewer, form: dict):
    print("Form received: ", viewerObj.viewerID, form, type(form))
    performActionPostSecurity(viewerObj, form, True)


def customWSMessageCallback(viewerObj: DynamicWebsite.Viewer, message: Any):
    print("WS received: ", viewerObj.viewerID, message, type(message))
    performActionPostSecurity(viewerObj, message, False)


def visitorLeftCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Left: ", viewerObj.viewerID)
    if viewerObj.privateData.party is not None:
        viewerObj.privateData.party.removePlayer(viewerObj.privateData.player, False)


def newVisitorCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Joined: ", viewerObj.viewerID)
    setPrivateDetails(viewerObj)
    accepted, reason = autoLogin(viewerObj)
    renderFirstPage(viewerObj, accepted)


def firstPageCreator():
    return make_response(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.FirstPage)).render(title="GAMBIT", baseURI=request.path))


##############################################################################################################################
# AUTHENTICATION


def resetFormErrors(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML("", DivID.loginIdentifierError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerGeneralError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerNameError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerEmailError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerUsernameError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerPasswordError, UpdateMethods.update)


def sendLoginCSRF(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(viewerObj.purposeManager.createCSRF("LOGIN"), DivID.loginCSRF, UpdateMethods.update)


def sendRegisterCSRF(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(viewerObj.purposeManager.createCSRF("REGISTER"), DivID.registerCSRF, UpdateMethods.update)


def sendLoginForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Login)).render(baseURI=viewerObj.privateData.baseURI), DivID.loginForm, UpdateMethods.update)
    sendLoginCSRF(viewerObj)


def sendRegisterForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Register)).render(baseURI=viewerObj.privateData.baseURI), DivID.registerForm, UpdateMethods.update)
    sendRegisterCSRF(viewerObj)


def checkPasswordStrength(password:str):
    return len(password) >= 8 and password.isalnum()


def logoutDevice(viewerObj: DynamicWebsite.Viewer):
    SQLconn.execute(f"DELETE FROM {Database.USER_DEVICES.TABLE_NAME} WHERE {Database.USER_DEVICES.VIEWER_ID}=? LIMIT 1", [viewerObj.viewerID])


def createDevice(viewerObj: DynamicWebsite.Viewer):
    logoutDevice(viewerObj)
    SQLconn.execute(f"INSERT INTO {Database.USER_DEVICES.TABLE_NAME} VALUES (?, ?, ?)", [viewerObj.viewerID, viewerObj.privateData.userName,  viewerObj.privateData.activeSince])


def setPrivateDetails(viewerObj: DynamicWebsite.Viewer):
    viewerObj.privateData = PrivateData()
    viewerObj.privateData.baseURI = request.path.split("?")[0]


def createUser(viewerObj: DynamicWebsite.Viewer, username:str, password:str, personName:str, email:str):
    if SQLconn.execute(f"SELECT {Database.USER_AUTH.USERNAME} from {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.USERNAME}=? LIMIT 1", [username]): return False, "Username already registered"
    if SQLconn.execute(f"SELECT {Database.USER_AUTH.EMAIL} from {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.EMAIL}=? LIMIT 1", [email]): return False, "Email already registered"
    SQLconn.execute(f"INSERT INTO {Database.USER_AUTH.TABLE_NAME} VALUES (?, ?, ?)", [username, email, passwordHasher.hash(password)])
    SQLconn.execute(f"INSERT INTO {Database.USER_INFO.TABLE_NAME} VALUES (?, ?, ?)", [username, personName, viewerObj.privateData.activeSince])
    viewerObj.privateData.userName = username
    createDevice(viewerObj)
    return True, "User registered"


def manualLogin(viewerObj: DynamicWebsite.Viewer, identifier:str, password:str):
    savedCredentials = SQLconn.execute(f"SELECT {Database.USER_AUTH.USERNAME}, {Database.USER_AUTH.PW_HASH} FROM {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.USERNAME}=? OR {Database.USER_AUTH.EMAIL}=? LIMIT 1", [identifier, identifier])
    if savedCredentials:
        savedCredentials = savedCredentials[0]
        username = savedCredentials[Database.USER_AUTH.USERNAME]
        pwHash = savedCredentials[Database.USER_AUTH.PW_HASH]
        try:
            if passwordHasher.verify(pwHash.decode(), password):
                viewerObj.privateData.userName = username
                createDevice(viewerObj)
                return True, "Manual Logged In"
        except:
            pass
    return False, "Invalid Credentials"


def autoLogin(viewerObj: DynamicWebsite.Viewer):
    savedDevice = SQLconn.execute(f"SELECT {Database.USER_DEVICES.USERNAME} FROM {Database.USER_DEVICES.TABLE_NAME} WHERE {Database.USER_DEVICES.VIEWER_ID}=? LIMIT 1", [viewerObj.viewerID])
    if savedDevice:
        savedDevice = savedDevice[0]
        viewerObj.privateData.userName = savedDevice[Database.USER_DEVICES.USERNAME].decode()
        return True, "Auto Logged In"
    return False, "Unknown Device"



##############################################################################################################################
# PARTY


def closeParty(party: Party):
    print(f"CLOSING PARTY {party.partyID}")
    if party.partyID in partyIDs: del partyIDs[party.partyID]
    if party.partyCode in partyCodes: del partyCodes[party.partyCode]
    matchmaker.removeFromQueue(party)


def onPartyCodeGenerated(party: Party):
    partyCodes[party.partyCode] = party


def createParty(player):
    party = Party()
    partyIDs[party.partyID] = party
    party.onPartyCodeCreated = onPartyCodeGenerated
    party.onPartyClosed = closeParty
    party.onSelfLeave = renderLobby
    if player:
        if player.viewer: renderLobbyNavbar(player.viewer)
        party.addPlayer(player)
    return party


##############################################################################################################################
# QUIZ

def onMatchFound(match: Match):
    quiz = Quiz(match)




##############################################################################################################################
# TEST

def testMatchmaking():
    sleep(2)
    for _ in range(1):
        party = createParty(Player(None, str(_)))
        matchmaker.addToQueue(party)
        #sleep(0.5)



##############################################################################################################################
# VARIABLES


serverStartTime = time()
fernetKey = argv[1]
webPort = int(argv[2])
cdPort = int(argv[3])
partyIDs:dict[str, Party] = {}
partyCodes:dict[str, Party] = {}


passwordHasher = PasswordHasher()
UpdateMethods = DynamicWebsite.UpdateMethods
cachedHTMLElements = CachedElements()
matchmaker = Matchmaker(onMatchFound)
logger = CustomisedLogs()
SQLconn = connectDB(logger)
dynamicWebsiteApp = DynamicWebsite(firstPageCreator, newVisitorCallback, visitorLeftCallback, formSubmitCallback, customWSMessageCallback, fernetKey, CoreValues.appName, Routes.webHomePage)
baseApp, WSSock = dynamicWebsiteApp.start()



@baseApp.get("/debug")
def _debug():
    final = ""
    final += "<br><br>Parties<br>"
    for partyID in partyIDs:
        final += "<br>&emsp;"+partyID
        final+="<br>&emsp;&emsp;Players"
        for player in partyIDs[partyID].players:
            final += "<br>&emsp;&emsp;"+player.userName
    final += "<br><br>Party Codes<br>"
    for partyCode in partyCodes:
        final += "<br>&emsp;"+partyCode+"&emsp;&emsp;"+partyCodes[partyCode].partyID
    return final


@baseApp.before_request
def _modHeadersBeforeRequest():
    """
    Before any request goes to any route, it passes through this function.
    Applies user remote address correctly (received from proxy)
    :return:
    """
    if request.remote_addr == "127.0.0.1":
        if request.environ.get("HTTP_X_FORWARDED_FOR") is not None:
            address = request.environ.get("HTTP_X_FORWARDED_FOR")
        else: address = "LOCALHOST"
        request.remote_addr = address
    if request.environ.get("HTTP_X_FORWARDED_PATH") is not None:
        request.path = request.environ.get("HTTP_X_FORWARDED_PATH")
    else:
        request.path = ""
    if request.environ.get("HTTP_X_FORWARDED_PROTO") is not None:
        request.scheme = request.environ.get("HTTP_X_FORWARDED_PROTO")


@baseApp.errorhandler(Exception)
def handle_404(error):
    return redirect("http://"+request.environ["HTTP_HOST"].replace(str(webPort), str(cdPort))+request.environ["PATH_INFO"]+"?"+request.environ["QUERY_STRING"])




#Thread(target=testMatchmaking).start()


WSGIRunner(baseApp, webPort, Routes.webHomePage, logger)