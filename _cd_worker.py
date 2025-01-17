from gevent.monkey import patch_all

patch_all()

from time import time, sleep
from sys import argv
from flask import Flask, request, send_from_directory, Response

from OtherClasses.CDFileTypes import CDFileType
from OtherClasses.Folders import Folders
from OtherClasses.Routes import Routes
from OtherClasses.CoreValues import CoreValues
from OtherClasses.MusicCollection import MusicCollection
from OtherClasses.CommonFunctions import WSGIRunner
from customisedLogs import CustomisedLogs


serverStartTime = time()
fernetKey = argv[1]
webPort = int(argv[2])
cdPort = int(argv[3])
cdApp = Flask(CoreValues.cdName)
musicCollection = MusicCollection()


@cdApp.get(Routes.cdFileContent)
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


@cdApp.get(Routes.favicon)
def _favicon():
    return send_from_directory(Folders.image, "favicon.png", as_attachment=True)


@cdApp.get(f"{Routes.liveMusic}/<category>")
def _liveMusicFeed(category):
    def soundBytesGenerator(category):
        first_run = True
        timeToWait=0
        while True:
            categoryStream = musicCollection.getStream(category)
            if categoryStream is None: return "Invalid stream category"
            if timeToWait: sleep(timeToWait)
            if first_run:
                data = categoryStream.header
                first_run = False
            else:
                data = categoryStream.getCurrentChunk()
                timeToWait = categoryStream.chunkTime
            yield data
    return Response(soundBytesGenerator(category))


@cdApp.errorhandler(Exception)
def handle_404(error):
   return "ITEM_NOT_FOUND", 404

logger = CustomisedLogs()
WSGIRunner(cdApp, cdPort, "", logger)