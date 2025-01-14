from gevent import monkey
monkey.patch_all()


from typing import Any
from sys import argv
from time import sleep
from flask import request, send_from_directory
from gevent.pywsgi import WSGIServer


from OtherClasses.Pages import *
from OtherClasses.HTMLElements import *
from OtherClasses.DivIDs import *
from OtherClasses.Routes import *
from OtherClasses.CDNFileTypes import *
from OtherClasses.CoreValues import *
from OtherClasses.Folders import *
from OtherClasses.FileNames import *


from customisedLogs import CustomisedLogs
from dynamicWebsite import DynamicWebsite


webFernetKey = argv[1]
webPort = int(argv[2])
UpdateMethods = DynamicWebsite.UpdateMethods
cachedHTMLElements = HTMLElements()


def renderAuthFullPage(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData is None or viewerObj.privateData.get("currentPage") not in [Pages.auth, Pages.preAuth, Pages.postAuth]:
        viewerObj.updateHTML(cachedHTMLElements.fetchStatic(FileNames.HTML.AuthFullPage), DivID.root, UpdateMethods.update)


def renderAuthPre(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.fetchStatic(FileNames.HTML.AuthPre), DivID.auth, UpdateMethods.update)
    viewerObj.privateData["currentPage"] = Pages.preAuth


def renderAuthForm(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.createAuthForm(viewerObj.purposeManager.createCSRF("REGISTER"), viewerObj.purposeManager.createCSRF("LOGIN")), DivID.auth, UpdateMethods.update)
    viewerObj.privateData["currentPage"] = Pages.preAuth


def renderAuthPost(viewerObj: DynamicWebsite.Viewer):
    renderAuthFullPage(viewerObj)
    viewerObj.updateHTML(cachedHTMLElements.fetchStatic(FileNames.HTML.AuthPost), DivID.auth, UpdateMethods.update)
    viewerObj.privateData["currentPage"] = Pages.preAuth


def renderNotesFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(cachedHTMLElements.fetchStatic(FileNames.HTML.AuthFullPage), DivID.root, UpdateMethods.update)


def renderNotes(viewerObj: DynamicWebsite.Viewer):
    pass


def formSubmitCallback(viewerObj: DynamicWebsite.Viewer, form: dict):
    print("Form received: ", viewerObj.viewerID, form)


def customWSMessageCallback(viewerObj: DynamicWebsite.Viewer, message: Any):
    print("WS received: ", viewerObj.viewerID, message)


def visitorLeftCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Left: ", viewerObj.viewerID)


def newVisitorCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Joined: ", viewerObj.viewerID)
    viewerObj.privateData = {}
    renderAuthPre(viewerObj)
    sleep(2)
    renderAuthForm(viewerObj)
    sleep(2)
    renderAuthPost(viewerObj)
    sleep(2)
    renderNotes(viewerObj)


logger = CustomisedLogs()
#SQLconn = connectDB(logger)


extraHeads = f"""
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="{Routes.cdnFileContent}?type={CDNFileType.js}&name={FileNames.JS.Trail}"></script>
<link rel="stylesheet" href="{Routes.cdnFileContent}?type={CDNFileType.css}&name={FileNames.CSS.auth}">
<link rel="stylesheet" href="{Routes.cdnFileContent}?type={CDNFileType.css}&name={FileNames.CSS.form}">
<script src="https://cdn.tailwindcss.com"></script>
"""


bodyBase = f"""
<body style="background-color: #000000;"> 
    <audio id="{DivID.music}" preload="none"> <source src="" type="audio/x-wav;codec=pcm"> </audio>
    <div id="{DivID.root}"></div>
    <div id="{DivID.scripts}"></div>
</body>
"""


#musicCollection = MusicCollection()
dynamicWebsiteApp = DynamicWebsite(newVisitorCallback, visitorLeftCallback, formSubmitCallback, customWSMessageCallback, webFernetKey,
                                   CoreValues.appName,  Routes.webHomePage, extraHeads, bodyBase, CoreValues.title)
baseApp, WSSock = dynamicWebsiteApp.start()


@baseApp.get(Routes.cdnFileContent)
def _fileContent():
    fileType = request.args.get("type", "").strip()
    fileName = request.args.get("name", "").strip()
    if fileType == CDNFileType.text:
         return send_from_directory(Folders.static+CDNFileType.text, fileName, as_attachment=True)
    elif fileType == CDNFileType.font:
         return send_from_directory(Folders.font, fileName, as_attachment=True)
    elif fileType == CDNFileType.image:
        return send_from_directory(Folders.image, fileName, as_attachment=True)
    elif fileType == CDNFileType.video:
        return send_from_directory(Folders.video, fileName, as_attachment=True)
    elif fileType == CDNFileType.html:
        return send_from_directory(Folders.html, fileName, as_attachment=True)
    elif fileType == CDNFileType.css:
        return send_from_directory(Folders.css, fileName, as_attachment=True)
    elif fileType == CDNFileType.js:
        return send_from_directory(Folders.js, fileName, as_attachment=True)
    return ""


@baseApp.get("/favicon.ico")
def _favicon():
    return send_from_directory(Folders.image, "favicon.png", as_attachment=True)


try:
    open(r"C:\cert\privkey1.pem", "r").close()
    print(f"https://127.0.0.1:{webPort}{Routes.webHomePage}")
    WSGIServer(('0.0.0.0', webPort,), baseApp, keyfile=r'C:\cert\privkey1.pem', certfile=r'C:\cert\fullchain1.pem').serve_forever()
except:
    print(f"http://127.0.0.1:{webPort}{Routes.webHomePage}")
    WSGIServer(('0.0.0.0', webPort,), baseApp).serve_forever()

