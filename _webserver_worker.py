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


def renderAuthFullPage(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage not in [Pages.auth, Pages.preAuth, Pages.postAuth]:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthFullPage), DivID.basePage, UpdateMethods.update)
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Ghost3d), DivID.ghost3d, UpdateMethods.update)


def renderAuthPre(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPre), DivID.auth, UpdateMethods.update)
    viewerObj.privateData.currentPage = Pages.preAuth
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.preAuth))


def renderAuth(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthForm), DivID.auth, UpdateMethods.update)
    viewerObj.privateData.currentPage = Pages.auth
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.auth))
    sendLoginForm(viewerObj)
    sendRegisterForm(viewerObj)


def renderAuthPost(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPost), DivID.auth, UpdateMethods.update)
    viewerObj.privateData.currentPage = Pages.postAuth
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.postAuth))


def renderLobbyFullPage(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage not in [Pages.lobby]:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyFull), DivID.basePage, UpdateMethods.update)
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.LobbyFeatures), DivID.lobbyFeatures, UpdateMethods.update)


def renderLobby(viewerObj: DynamicWebsite.Viewer):
    renderLobbyFullPage(viewerObj)
    if viewerObj.privateData.party is None:
        viewerObj.privateData.party = Party()
        viewerObj.privateData.party.addPlayer(viewerObj.privateData.player)
        viewerObj.privateData.party.addPlayer(Player())
        viewerObj.privateData.party.addPlayer(Player())


def renderPartyJoined(viewerObj: DynamicWebsite.Viewer):
    pass


def renderPartyLeft(viewerObj: DynamicWebsite.Viewer):
    pass


def kickedFromParty(viewerObj: DynamicWebsite.Viewer):
    pass


def renderFriendFull(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage not in [None, Pages.auth, Pages.preAuth] and not viewerObj.privateData.friendsRendered:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.FriendsFull), DivID.friendsFull, UpdateMethods.update)
        viewerObj.privateData.friendsRendered = True


def renderFriends(viewerObj: DynamicWebsite.Viewer):
    renderFriendFull(viewerObj)
    # friendList = SQLconn.execute(f"""SELECT
    # CASE
    #     WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
    #     WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
    # END AS result
    # FROM {Database.FRIEND.TABLE_NAME};""", [viewerObj.privateData.userID, viewerObj.privateData.userID])
    others = []
    for _ in range(5):
        other = Player()
        friend = Friend(viewerObj.privateData.player, other)
        others.append(friend)
        viewerObj.updateHTML(Template(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.FriendElement)).render(connectionID=friend.connectionID, PFP=other.displayPFP(), userName=other.displayUserName(), state=other.displayState()), DivID.onlineFriends, UpdateMethods.append)
    #for other in others:
        #sleep(1)
        #viewerObj.updateHTML("", other.connectionID, UpdateMethods.remove)
        #viewerObj.sendCustomMessage()


def renderNotesFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.NotesFullPage), DivID.basePage, UpdateMethods.update)


def renderNotes(viewerObj: DynamicWebsite.Viewer):
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.postAuth))


def renderUniversal(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.UniversalContainer), DivID.root, UpdateMethods.update)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Navbar), DivID.navbar, UpdateMethods.update)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.MusicTray), DivID.musicTrayHolder, UpdateMethods.update)
    sleep(1)
    viewerObj.updateHTML(f'<script>{cachedHTMLElements.fetchStaticJS(FileNames.JS.Universal)}</script>', DivID.scripts, UpdateMethods.append)
    renderFriends(viewerObj)


def renderFirstPage(viewerObj: DynamicWebsite.Viewer):
    print(viewerObj.privateData.expectedPostAuthPage, viewerObj.privateData.expectedPostAuthPage==Pages.lobby)
    if viewerObj.privateData.expectedPostAuthPage == Pages.lobby: renderLobby(viewerObj)
    #elif viewerObj.privateData.expectedPostAuthPage == Pages.marketPlace: renderMarketPlace(viewerObj)
    else: renderAuthPost(viewerObj)


def rejectForm(form: dict, reason):
    print("FORM REJECTED", reason)


def formSubmitCallback(viewerObj: DynamicWebsite.Viewer, form: dict):
    print("Form received: ", viewerObj.viewerID, form)
    if "PURPOSE" not in form: return rejectForm(form, "Lacks Purpose")
    purpose = form.pop("PURPOSE")
    if viewerObj.privateData.currentPage == Pages.auth:
        if purpose == "LOGIN":
            identifier = form.get("identifier")
            password = form.get("password")
            if not identifier: return rejectForm(form, "Invalid Username/Email")
            if not password: return rejectForm(form, "Invalid Password")
            accepted, reason = manualLogin(viewerObj, identifier, password)
            if accepted: return renderFirstPage(viewerObj)
            else:
                rejectForm(form, reason)
                return sendLoginForm(viewerObj)
        elif purpose == "REGISTER":
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
            if accepted: return renderFirstPage(viewerObj)
            else:
                rejectForm(form, reason)
                return sendRegisterForm(viewerObj)
    return rejectForm(form, "Unknown Purpose")


def customWSMessageCallback(viewerObj: DynamicWebsite.Viewer, message: Any):
    print("WS received: ", viewerObj.viewerID, message)


def visitorLeftCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Left: ", viewerObj.viewerID)


def newVisitorCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Joined: ", viewerObj.viewerID)
    setPrivateDetails(viewerObj)
    renderUniversal(viewerObj)
    renderLobby(viewerObj)
    # accepted, reason = autoLogin(viewerObj)
    # if accepted: renderFirstPage(viewerObj)
    # else: renderAuthPre(viewerObj)


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


serverStartTime = time()
fernetKey = argv[1]
webPort = int(argv[2])
cdPort = int(argv[3])


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