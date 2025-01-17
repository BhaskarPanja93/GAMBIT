from gevent import monkey

monkey.patch_all()

from time import time
from sys import argv
from typing import Any
from flask import request, redirect
from werkzeug.sansio.utils import get_current_url

from OtherClasses.FileNames import FileNames
from OtherClasses.Database import Database
from OtherClasses.CachedElements import CachedElements
from OtherClasses.CoreValues import CoreValues
from OtherClasses.DivIDs import DivID
from OtherClasses.Pages import Pages
from OtherClasses.Routes import Routes
from OtherClasses.CommonFunctions import connectDB, WSGIRunner

from customisedLogs import CustomisedLogs
from internal.dynamicWebsite import DynamicWebsite


serverStartTime = time()
fernetKey = argv[1]
webPort = int(argv[2])
cdPort = int(argv[3])
UpdateMethods = DynamicWebsite.UpdateMethods
cachedHTMLElements = CachedElements()


def renderAuthFullPage(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData is None or viewerObj.privateData.get("currentPage") not in [Pages.auth, Pages.preAuth, Pages.postAuth]:
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthFullPage), DivID.basePage, UpdateMethods.update)
        viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Ghost3d), DivID.ghost3d, UpdateMethods.update)


def renderAuthPre(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPre), DivID.auth, UpdateMethods.update)
    viewerObj.privateData["currentPage"] = Pages.preAuth


def renderAuthForm(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.createAuthForm(viewerObj.purposeManager.createCSRF("REGISTER"), viewerObj.purposeManager.createCSRF("LOGIN")), DivID.auth, UpdateMethods.update)
    viewerObj.privateData["currentPage"] = Pages.auth


def renderAuthPost(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthPost), DivID.auth, UpdateMethods.update)
    viewerObj.privateData["currentPage"] = Pages.postAuth


def renderNotesFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.NotesFullPage), DivID.basePage, UpdateMethods.update)


def renderNotes(viewerObj: DynamicWebsite.Viewer):
    pass


def renderMusicTray(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.MusicTray), DivID.musicTray, UpdateMethods.update)
    viewerObj.updateHTML(f'<script>{cachedHTMLElements.fetchStaticJS(FileNames.JS.Music)}</script>', DivID.scripts, UpdateMethods.append)


def renderUniversal(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.UniversalContainer), DivID.root, UpdateMethods.update)
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.Navbar), DivID.navbar, UpdateMethods.update)
    viewerObj.updateHTML(f'<script>{cachedHTMLElements.fetchStaticJS(FileNames.JS.Trail)}</script>', DivID.scripts, UpdateMethods.append)


def formSubmitCallback(viewerObj: DynamicWebsite.Viewer, form: dict):
    print("Form received: ", viewerObj.viewerID, form)


def customWSMessageCallback(viewerObj: DynamicWebsite.Viewer, message: Any):
    print("WS received: ", viewerObj.viewerID, message)


def visitorLeftCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Left: ", viewerObj.viewerID)


def newVisitorCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Joined: ", viewerObj.viewerID)
    viewerObj.privateData = {}
    renderUniversal(viewerObj)
    renderMusicTray(viewerObj)
    knownUserID = SQLconn.execute(f"SELECT {Database.USER_DEVICES.USER_ID} FROM {Database.USER_DEVICES.SELF} WHERE {Database.USER_DEVICES.VIEWER_ID}=? LIMIT 1", [viewerObj.viewerID])
    if knownUserID:
        knownUserID = knownUserID[0]
        viewerObj.privateData["UserID"] = knownUserID.get(Database.USER_DEVICES.VIEWER_ID)
    print(knownUserID)
    if knownUserID: renderAuthPost(viewerObj)
    else: renderAuthPre(viewerObj)


logger = CustomisedLogs()
SQLconn = connectDB(logger)
dynamicWebsiteApp = DynamicWebsite(newVisitorCallback, visitorLeftCallback, formSubmitCallback, customWSMessageCallback, fernetKey, CoreValues.appName, Routes.webHomePage, cachedHTMLElements.fetchStaticHTML(FileNames.HTML.ExtraHead), cachedHTMLElements.fetchStaticHTML(FileNames.HTML.BodyBase), CoreValues.title)
baseApp, WSSock = dynamicWebsiteApp.start()

@baseApp.get("/ip")
def get_ip():
    return request.remote_addr


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
