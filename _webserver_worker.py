from gevent import monkey

monkey.patch_all()

from OtherClasses.Matchmaker import Matchmaker
from time import time
from sys import argv
from typing import Any
from flask import request, redirect, make_response
from jinja2 import Template
from argon2 import PasswordHasher

from OtherClasses.PrivateData import PrivateData
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
# GHOST ELEMENT


def renderGhost3D(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.Ghost3d):
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Ghost3d)).render(baseURI=viewerObj.privateData.baseURI), DivID.ghost3d, UpdateMethods.update)


##############################################################################################################################
# AUTH PAGES


def __renderAuthStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() not in [Pages.AUTH, Pages.PRE_AUTH, Pages.POST_AUTH]:
        # if not viewerObj.privateData.isScriptRendered(FileNames.JS.Auth):
        #     viewerObj.updateHTML(f"<script id='{FileNames.JS.Auth}'>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Auth)+"</script>", DivID.scripts, UpdateMethods.append)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
        renderGhost3D(viewerObj)


def renderAuthPre(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.PRE_AUTH:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPre)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.PRE_AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.PRE_AUTH))


def renderAuthForms(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.AUTH:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthForms)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.AUTH))
        sendLoginForm(viewerObj)
        sendRegisterForm(viewerObj)


def renderAuthPost(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.POST_AUTH:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPost)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.POST_AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.POST_AUTH))


##############################################################################################################################
# FRIEND ELEMENTS


def renderFriends(viewerObj: DynamicWebsite.Viewer):
    # if not viewerObj.privateData.isScriptRendered(FileNames.JS.Friends):
    #     viewerObj.updateHTML(f"<script id='{FileNames.JS.Friends}'>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Friends)+"</script>", DivID.scripts, UpdateMethods.append)
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.FriendsStructure):
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.FriendsStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.friendsStructure, UpdateMethods.update)

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


##############################################################################################################################
# LOBBY PAGES


def __renderLobbyStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() != Pages.LOBBY:
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyFeatures)).render(baseURI=viewerObj.privateData.baseURI), DivID.lobbyFeatures, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.LOBBY)


def renderLobby(viewerObj: DynamicWebsite.Viewer):
    __renderLobbyStructure(viewerObj)
    viewerObj.privateData.newPage(Pages.LOBBY)
    if viewerObj.privateData.party is None:
        viewerObj.privateData.party = createParty(viewerObj.privateData.player)


def renderPartyJoined(viewerObj: DynamicWebsite.Viewer):
    pass


def renderPartyLeft(viewerObj: DynamicWebsite.Viewer):
    pass


def kickedFromParty(viewerObj: DynamicWebsite.Viewer):
    pass


##############################################################################################################################
# NOTES PAGES


def renderNotesFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.NotesFullPage)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)


def renderNotes(viewerObj: DynamicWebsite.Viewer):
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.POST_AUTH))



##############################################################################################################################
# CHAT ELEMENT


def renderChatStructure(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.ChatFull):
        # viewerObj.updateHTML(f"<script id='{FileNames.JS.Chat}'>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Chat)+"</script>", DivID.scripts, UpdateMethods.append)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.ChatFull)).render(baseURI=viewerObj.privateData.baseURI), DivID.chatBox, UpdateMethods.update)


##############################################################################################################################
# MUSIC TRAY


def renderMusicTray(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.MusicTray)).render(baseURI=viewerObj.privateData.baseURI), DivID.musicTrayHolder, UpdateMethods.update)


##############################################################################################################################
# NAVBAR


def renderRegularNavbar(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.RegularNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar, UpdateMethods.update)


def renderLobbyNavbar(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar, UpdateMethods.update)


##############################################################################################################################
# CONTEXTUAL


def renderPreAuthUniversal(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.PreAuthUniversal):
        viewerObj.updateHTML(f"<script id='{FileNames.JS.PreAuthUniversal}'>" + cachedHTMLElements.fetchStaticJS(FileNames.JS.PreAuthUniversal) + "</script>", DivID.scripts, UpdateMethods.append)
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.Trail):
        viewerObj.updateHTML(f"<script id='{FileNames.JS.Trail}'>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Trail)+"</script>", DivID.scripts, UpdateMethods.append)
    # if not viewerObj.privateData.isScriptRendered(FileNames.JS.Music):
    #     viewerObj.updateHTML(f"<script id='{FileNames.JS.Music}'>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Music)+"</script>", DivID.scripts, UpdateMethods.append)
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.UniversalContainer)).render(baseURI=viewerObj.privateData.baseURI), DivID.root, UpdateMethods.update)


def renderPostAuthUniversal(viewerObj: DynamicWebsite.Viewer):
    # if not viewerObj.privateData.isScriptRendered(FileNames.JS.Lobby):
    #     viewerObj.updateHTML(f"<script id='{FileNames.JS.Lobby}'>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Lobby)+"</script>", DivID.scripts, UpdateMethods.append)
    pass

##############################################################################################################################
# DECIDE FIRST PAGE


def renderFirstPage(viewerObj: DynamicWebsite.Viewer, isAuthenticated: bool):
    renderPreAuthUniversal(viewerObj)
    renderRegularNavbar(viewerObj)
    renderMusicTray(viewerObj)
    if isAuthenticated:
        if viewerObj.privateData.player is None:
            viewerObj.privateData.player = Player(viewerObj, viewerObj.privateData.userName)
        renderPostAuthUniversal(viewerObj)
        renderFriends(viewerObj)
        renderChatStructure(viewerObj)
        if viewerObj.privateData.expectedPostAuthPage == Pages.LOBBY: renderLobby(viewerObj)
        #elif viewerObj.privateData.expectedPostAuthPage == Pages.marketPlace: renderMarketPlace(viewerObj)
        else: renderAuthPost(viewerObj)
    else:
        renderAuthPre(viewerObj)


##############################################################################################################################
# USER ACTIONS


def performActionPostSecurity(viewerObj: DynamicWebsite.Viewer, form: dict, isSecure:bool):
    if "PURPOSE" not in form: return rejectForm(form, "Lacks Purpose")
    purpose = form.pop("PURPOSE")
    if viewerObj.privateData.currentPage() not in [Pages.PRE_AUTH, Pages.AUTH]:
        if purpose == "LOGOUT":
            logoutDevice(viewerObj)
            return viewerObj.sendCustomMessage(CustomMessages.refreshBrowser())
    if viewerObj.privateData.currentPage() == Pages.AUTH:
        if purpose == "LOGIN" and isSecure:
            identifier = form.get("identifier")
            password = form.get("password")
            if not identifier: return rejectForm(form, "Invalid Username/Email")
            if not password: return rejectForm(form, "Invalid Password")
            accepted, reason = manualLogin(viewerObj, identifier, password)
            if accepted: return renderFirstPage(viewerObj, accepted)
            else:
                rejectForm(form, reason)
                return sendLoginForm(viewerObj)
        elif purpose == "REGISTER" and isSecure:
            username = form.get("user-name")
            password = form.get("password")
            confirmPassword = form.get("confirm-password")
            email = form.get("email")
            name = form.get("person-name")
            if not username: return rejectForm(form, "Invalid Username")
            if not password: return rejectForm(form, "Invalid Password")
            if password != confirmPassword: return rejectForm(form, "Passwords Do Not Match")
            if not email: return rejectForm(form, "Invalid Email")
            if not name: return rejectForm(form, "Invalid Name")
            accepted, reason = createUser(viewerObj, username, password, name, email)
            if accepted: return renderFirstPage(viewerObj, True)
            else:
                rejectForm(form, reason)
                return sendRegisterForm(viewerObj)
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
            #viewerObj.privateData.party.startTimer()
            return matchmaker.addToQueue(viewerObj.privateData.party)
        if purpose == "STOP_QUEUE":
            return matchmaker.removeFromQueue(viewerObj.privateData.party)
    return rejectForm(form, "Unknown Purpose")


def rejectForm(form: dict, reason):
    print("FORM REJECTED", reason)


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


def sendLoginForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Login)).render(CSRF=viewerObj.purposeManager.createCSRF("LOGIN"), baseURI=viewerObj.privateData.baseURI), DivID.loginForm, UpdateMethods.update)


def sendRegisterForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Register)).render(CSRF=viewerObj.purposeManager.createCSRF("REGISTER"), baseURI=viewerObj.privateData.baseURI), DivID.registerForm, UpdateMethods.update)


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
        if passwordHasher.verify(pwHash.decode(), password):
            viewerObj.privateData.userName = username
            createDevice(viewerObj)
        return True, "Manual Logged In"
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


def onPartyCodeGenerated(party: Party):
    partyCodes[party.partyCode] = party
    print(f"NEW PARTY CODE {party.partyID} {party.partyCode}", sep='\n')


def createParty(player):
    party = Party()
    partyIDs[party.partyID] = party
    party.onPartyCodeCreated = onPartyCodeGenerated
    party.onPartyClosed = closeParty
    party.onSelfLeave = renderLobby
    if player:
        if player.viewer: renderLobbyNavbar(player.viewer)
        party.addPlayer(player)
    print(f"NEW PARTY {party.partyID}")
    return party


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
matchmaker = Matchmaker()
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


WSGIRunner(baseApp, webPort, Routes.webHomePage, logger)