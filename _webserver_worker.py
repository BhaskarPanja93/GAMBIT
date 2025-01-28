from gevent import monkey

monkey.patch_all()

from time import time, sleep
from sys import argv
from typing import Any
from flask import request, redirect
from jinja2 import Template
from werkzeug.sansio.utils import get_current_url
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
from OtherClasses.Friend import Friend
from OtherClasses.Routes import Routes
from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.CommonFunctions import connectDB, WSGIRunner

from customisedLogs import CustomisedLogs
from internal.dynamicWebsite import DynamicWebsite


##############################################################################################################################
# GHOST ELEMENT


def renderGhost3D(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.Ghost3d):
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Ghost3d), DivID.ghost3d, UpdateMethods.update)


##############################################################################################################################
# AUTH PAGES


def __renderAuthStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() not in [Pages.AUTH, Pages.PRE_AUTH, Pages.POST_AUTH]:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthStructure), DivID.changingPage, UpdateMethods.update)
        if not viewerObj.privateData.isScriptRendered(FileNames.JS.Auth):
            viewerObj.updateHTML("<script>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Auth)+"</script>", DivID.scripts, UpdateMethods.append)
        sleep(0.1)
        renderGhost3D(viewerObj)


def renderAuthPre(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.PRE_AUTH:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPre), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.PRE_AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.PRE_AUTH))


def renderAuthForms(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.AUTH:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthForms), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.AUTH))
        sendLoginForm(viewerObj)
        sendRegisterForm(viewerObj)


def renderAuthPost(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.POST_AUTH:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPost), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.POST_AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.POST_AUTH))


##############################################################################################################################
# FRIEND ELEMENTS


def renderFriends(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.FriendsStructure):
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.FriendsStructure), DivID.friendsStructure, UpdateMethods.update)
        #sleep(0.1)
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.Friends):
        viewerObj.updateHTML("<script>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Friends)+"</script>", DivID.scripts, UpdateMethods.append)

    # friendList = SQLconn.execute(f"""SELECT
    # CASE
    #     WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
    #     WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
    # END AS result
    # FROM {Database.FRIEND.TABLE_NAME};""", [viewerObj.privateData.userID, viewerObj.privateData.userID])
    others = []
    for _ in range(5):
        #sleep(1)
        other = Player()
        friend = Friend(viewerObj.privateData.player, other)
        others.append(friend)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.FriendElement)).render(connectionID=friend.connectionID, PFP=other.displayPFP(), userName=other.displayUserName(), state=other.displayState()), DivID.onlineFriends, UpdateMethods.append)
    # for other in others:
    #     sleep(1)
    #     viewerObj.updateHTML("", other.connectionID, UpdateMethods.remove)
    #     viewerObj.sendCustomMessage()


##############################################################################################################################
# LOBBY PAGES


def __renderLobbyStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() != Pages.LOBBY:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyStructure), DivID.changingPage, UpdateMethods.update)
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyFeatures), DivID.lobbyFeatures, UpdateMethods.update)
        sleep(0.1)


def renderLobby(viewerObj: DynamicWebsite.Viewer):
    __renderLobbyStructure(viewerObj)
    viewerObj.privateData.newPage(Pages.LOBBY)
    if viewerObj.privateData.party is None:
        viewerObj.privateData.party = createParty()
        viewerObj.privateData.party.addPlayer(viewerObj.privateData.player)
        viewerObj.privateData.party.addPlayer(Player())
        viewerObj.privateData.party.addPlayer(Player())


def renderPartyJoined(viewerObj: DynamicWebsite.Viewer):
    pass


def renderPartyLeft(viewerObj: DynamicWebsite.Viewer):
    pass


def kickedFromParty(viewerObj: DynamicWebsite.Viewer):
    pass


##############################################################################################################################
# NOTES PAGES


def renderNotesFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.NotesFullPage), DivID.changingPage, UpdateMethods.update)


def renderNotes(viewerObj: DynamicWebsite.Viewer):
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.POST_AUTH))



##############################################################################################################################
# CHAT ELEMENT


def renderChatStructure(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.ChatFull):
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.ChatFull), DivID.chatBox, UpdateMethods.update)


##############################################################################################################################
# MUSIC TRAY


def renderMusicTray(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.MusicTray), DivID.musicTrayHolder, UpdateMethods.update)


##############################################################################################################################
# NAVBAR


def renderNavbar(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Navbar), DivID.navbar, UpdateMethods.update)


def renderLogoutButton(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.LogoutButton):
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LogoutButton), DivID.logoutButton, UpdateMethods.update)


##############################################################################################################################
# CONTEXTUAL


def renderPreAuthUniversal(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.UniversalContainer), DivID.root, UpdateMethods.update)
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.PreAuthUniversal):
        viewerObj.updateHTML("<script>" + cachedHTMLElements.fetchStaticJS(FileNames.JS.PreAuthUniversal) + "</script>", DivID.scripts, UpdateMethods.append)
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.Trail):
        viewerObj.updateHTML("<script>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Trail)+"</script>", DivID.scripts, UpdateMethods.append)
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.Music):
        viewerObj.updateHTML("<script>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Music)+"</script>", DivID.scripts, UpdateMethods.append)
    #sleep(0.1)



def renderPostAuthUniversal(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.Lobby):
        viewerObj.updateHTML("<script>"+cachedHTMLElements.fetchStaticJS(FileNames.JS.Lobby)+"</script>", DivID.scripts, UpdateMethods.append)


##############################################################################################################################
# DECIDE FIRST PAGE


def renderFirstPage(viewerObj: DynamicWebsite.Viewer, isAuthenticated: bool):
    renderPreAuthUniversal(viewerObj)
    renderNavbar(viewerObj)
    renderMusicTray(viewerObj)
    if isAuthenticated:
        renderPostAuthUniversal(viewerObj)
        renderLogoutButton(viewerObj)
        renderChatStructure(viewerObj)
        renderFriends(viewerObj)
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
    if viewerObj.privateData.currentPage() == Pages.AUTH:
        if purpose == "LOGIN" and isSecure:
            identifier = form.get("identifier")
            password = form.get("password")
            if not identifier: return rejectForm(form, "Invalid Username/Email")
            if not password: return rejectForm(form, "Invalid Password")
            accepted, reason = manualLogin(viewerObj, identifier, password)
            if accepted: return renderFirstPage(viewerObj, True)
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
            if viewerObj.privateData.party is not None:
                return viewerObj.privateData.party.generatePartyCode()
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


def newVisitorCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Joined: ", viewerObj.viewerID)
    setPrivateDetails(viewerObj)
    accepted, reason = autoLogin(viewerObj)
    renderFirstPage(viewerObj, accepted)


##############################################################################################################################
# AUTHENTICATION


def sendLoginForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Login)).render(CSRF=viewerObj.purposeManager.createCSRF("LOGIN")), DivID.loginForm, UpdateMethods.update)


def sendRegisterForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Register)).render(CSRF=viewerObj.purposeManager.createCSRF("REGISTER")), DivID.registerForm, UpdateMethods.update)


def checkPasswordStrength(password:str):
    return len(password) >= 8 and password.isalnum()


def logoutDevice(viewerObj: DynamicWebsite.Viewer):
    SQLconn.execute(f"DELETE FROM {Database.USER_DEVICES.TABLE_NAME} WHERE {Database.USER_DEVICES.VIEWER_ID}=?", [viewerObj.viewerID])


def loginDevice(viewerObj: DynamicWebsite.Viewer):
    logoutDevice(viewerObj)
    SQLconn.execute(f"INSERT INTO {Database.USER_DEVICES.TABLE_NAME} VALUES (?, ?, ?)", [viewerObj.viewerID, viewerObj.privateData.userID,  viewerObj.privateData.activeSince])


def setPrivateDetails(viewerObj: DynamicWebsite.Viewer):
    viewerObj.privateData = PrivateData()
    viewerObj.privateData.player = Player(viewerObj)


def createUser(viewerObj: DynamicWebsite.Viewer, username:str, password:str, personName:str, email:str):
    userID = dynamicWebsiteApp.stringGenerator.AlphaNumeric(30, 30)
    if SQLconn.execute(f"SELECT {Database.USER_AUTH.USER_ID} from {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.USERNAME}=? LIMIT 1", [username]): return False, "Username already registered"
    if SQLconn.execute(f"SELECT {Database.USER_AUTH.USER_ID} from {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.EMAIL}=? LIMIT 1", [email]): return False, "Email already registered"
    SQLconn.execute(f"INSERT INTO {Database.USER_AUTH.TABLE_NAME} VALUES (?, ?, ?, ?)", [userID, username, email, passwordHasher.hash(password)])
    SQLconn.execute(f"INSERT INTO {Database.USER_INFO.TABLE_NAME} VALUES (?, ?, ?)", [userID, personName, viewerObj.privateData.activeSince])
    viewerObj.privateData.userID = userID
    loginDevice(viewerObj)
    print("User registered")
    return True, "User registered"


def manualLogin(viewerObj: DynamicWebsite.Viewer, identifier:str, password:str):
    savedCredentials = SQLconn.execute(f"SELECT {Database.USER_AUTH.USER_ID}, {Database.USER_AUTH.PW_HASH} FROM {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.USERNAME}=? OR {Database.USER_AUTH.EMAIL}=? LIMIT 1", [identifier, identifier])
    if savedCredentials:
        savedCredentials = savedCredentials[0]
        userID = savedCredentials[Database.USER_AUTH.USER_ID]
        pwHash = savedCredentials[Database.USER_AUTH.PW_HASH]
        if passwordHasher.verify(pwHash.decode(), password):
            viewerObj.privateData.userID = userID
            loginDevice(viewerObj)
            print("Manual Logged In")
        return True, "Manual Logged In"
    return False, "Invalid Credentials"


def autoLogin(viewerObj: DynamicWebsite.Viewer):
    savedDevice = SQLconn.execute(f"SELECT {Database.USER_DEVICES.USER_ID} FROM {Database.USER_DEVICES.TABLE_NAME} WHERE {Database.USER_DEVICES.VIEWER_ID}=? LIMIT 1", [viewerObj.viewerID])
    if savedDevice:
        savedDevice = savedDevice[0]
        viewerObj.privateData.userID = savedDevice[Database.USER_DEVICES.USER_ID]
        print("Auto Logged In")
        return True, "Auto Logged In"
    return False, "Unknown Device"



##############################################################################################################################
# PARTY


def closeParty(party: Party):
    if party.partyID in partyIDs: del partyIDs[party.partyID]
    if party.partyCode in partyCodes: del partyCodes[party.partyCode]
    print("NEW",partyCodes, partyIDs, sep='\n')


def onPartyCodeGenerated(party: Party):
    partyCodes[party.partyCode] = party
    print("PARTYCODE",partyCodes, partyIDs, sep='\n')


def createParty():
    party = Party()
    partyIDs[party.partyID] = party
    party.onPartyCodeCreated = onPartyCodeGenerated
    party.onPartyClosed = closeParty
    print("NEW",partyCodes, partyIDs, sep='\n')
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
logger = CustomisedLogs()
SQLconn = connectDB(logger)
dynamicWebsiteApp = DynamicWebsite(newVisitorCallback, visitorLeftCallback, formSubmitCallback, customWSMessageCallback, fernetKey, CoreValues.appName, Routes.webHomePage, cachedHTMLElements.fetchStaticHTML(FileNames.HTML.ExtraHead), cachedHTMLElements.fetchStaticHTML(FileNames.HTML.BodyBase), CoreValues.title)
baseApp, WSSock = dynamicWebsiteApp.start()


@baseApp.errorhandler(Exception)
def handle_404(error):
    if ':' in request.host:
        host, port = request.host.split(':')
        port = int(port)
    else:
        host = request.host
        if request.scheme == 'https': port = 443
        else: port = 80
    return redirect(get_current_url(request.scheme, f"{host}:{port+1}", request.root_path, request.path, request.query_string))

WSGIRunner(baseApp, webPort, Routes.webHomePage, logger)