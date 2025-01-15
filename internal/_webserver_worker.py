from gevent import monkey


monkey.patch_all()

from typing import Any
from sys import argv
from gevent.pywsgi import WSGIServer
from flask import request, send_from_directory, Response

from OtherClasses.Pages import *
from OtherClasses.CachedElements import *
from OtherClasses.DivIDs import *
from OtherClasses.Routes import *
from OtherClasses.CDFileTypes import *
from OtherClasses.CoreValues import *
from OtherClasses.FileNames import *
from OtherClasses.MusicCollection import *


from customisedLogs import CustomisedLogs
from dynamicWebsite import DynamicWebsite


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
    viewerObj.updateHTML(cachedHTMLElements.fetchStaticHTML(FileNames.HTML.AuthFullPage), DivID.root, UpdateMethods.update)


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


    #renderAuthPre(viewerObj)
    #sleep(2)
    renderAuthForm(viewerObj)
    #sleep(2)
    #renderAuthPost(viewerObj)
    #sleep(2)
    #renderNotes(viewerObj)


logger = CustomisedLogs()
#SQLconn = connectDB(logger)


extraHeads = f"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="{Routes.cdFileContent}?type={CDFileType.css}&name={FileNames.CSS.auth}">
<link rel="stylesheet" href="{Routes.cdFileContent}?type={CDFileType.css}&name={FileNames.CSS.form}">
<script src="https://cdn.tailwindcss.com"></script>
"""


bodyBase = f"""
<body style="background-color: #000000;"> 
    <audio id="music-player" preload="none"> <source src="" type="audio/x-wav;codec=pcm"> </audio>
    <div id="{DivID.scripts}" style="display:none"></div>
    <div id="{DivID.root}"></div>
</body>
"""


dynamicWebsiteApp = DynamicWebsite(newVisitorCallback, visitorLeftCallback, formSubmitCallback, customWSMessageCallback, fernetKey, CoreValues.appName, Routes.webHomePage, extraHeads, bodyBase, CoreValues.title)
baseApp, WSSock = dynamicWebsiteApp.start()












musicCollection = MusicCollection()

@baseApp.get(Routes.cdFileContent)
def _fileContent():
    fileType = request.args.get("type", "").strip()
    fileName = request.args.get("name", "").strip()
    if fileType == CDFileType.text:
        return send_from_directory(Folders.text, fileName, as_attachment=True), 200
    elif fileType == CDFileType.font:
        return send_from_directory(Folders.font, fileName, as_attachment=True), 200
    elif fileType == CDFileType.image:
        return send_from_directory(Folders.image, fileName, as_attachment=True), 200
    elif fileType == CDFileType.video:
        return send_from_directory(Folders.video, fileName, as_attachment=True), 200
    elif fileType == CDFileType.html:
        return send_from_directory(Folders.html, fileName, as_attachment=True), 200
    elif fileType == CDFileType.css:
        return send_from_directory(Folders.css, fileName, as_attachment=True), 200
    elif fileType == CDFileType.js:
        return send_from_directory(Folders.js, fileName, as_attachment=True), 200
    return "", 404


@baseApp.get(Routes.favicon)
def _favicon():
    return send_from_directory(Folders.image, "favicon.png", as_attachment=True)


@baseApp.get(f"{Routes.liveMusic}/<category>")
def _liveMusicFeed(category):
    def soundBytesGenerator(category):
        first_run = True
        timeToWait=0
        while True:
            categoryStream = musicCollection.getStream(category)
            if categoryStream is None:
                return "Invalid stream category"
            if timeToWait: sleep(timeToWait)
            if first_run:
                data = categoryStream.header
                first_run = False
            else:
                data = categoryStream.getCurrentChunk()
                timeToWait = categoryStream.chunkTime
            yield data
    return Response(soundBytesGenerator(category))




@baseApp.after_request
def _setCacheTimeHeader(response):
    response.headers['Cache-Control'] = 'public, max-age=36000'
    response.headers['ETag'] = str(serverStartTime)
    return response












try:
    1/0
    open(r"C:\cert\privkey1.pem", "r").close()
    print(f"https://127.0.0.1:{webPort}{Routes.webHomePage}")
    WSGIServer(('0.0.0.0', webPort,), baseApp, keyfile=r'C:\cert\privkey1.pem', certfile=r'C:\cert\fullchain1.pem').serve_forever()
except:
    print(f"http://127.0.0.1:{webPort}{Routes.webHomePage}")
    WSGIServer(('0.0.0.0', webPort,), baseApp).serve_forever()

