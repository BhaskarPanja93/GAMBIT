from gevent.monkey import patch_all; patch_all()

from time import time
from sys import argv
from flask import Flask, request, send_from_directory, Response

from OtherClasses.CDFileTypes import CDFileType
from OtherClasses.Folders import Folders
from OtherClasses.Routes import Routes
from OtherClasses.CoreValues import CoreValues
from OtherClasses.MusicCollection import MusicCollection
from OtherClasses.CommonFunctions import WSGIRunner
from customisedLogs import CustomisedLogs
from flask_cors import CORS


serverStartTime = time()
fernetKey = argv[1]
webPort = int(argv[2])
cdPort = int(argv[3])
cdApp = Flask(CoreValues.cdName)
musicCollection = MusicCollection()
allowed_origins = [
    "*"
]

CORS(cdApp, resources={r"/*": {"origins": allowed_origins}})
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
    categoryStream = musicCollection.activeStreams.get(category)
    if categoryStream is None: return "Invalid stream category"
    def soundBytesGenerator():
        first = True
        while True:
            if first:
                first = False
                yield b"".join(categoryStream.allChunks)
            with categoryStream.condition:
                categoryStream.condition.wait()
                yield categoryStream.allChunks[-1]
    return Response(soundBytesGenerator(), mimetype="audio/mpeg'")


@cdApp.get(f"{Routes.allMusicCategories}")
def _allMusicCategories():
    return list(musicCollection.activeStreams)



@cdApp.errorhandler(Exception)
def handle_404(error):
    return "Doesnt Exist in CD", 404


logger = CustomisedLogs()
WSGIRunner(cdApp, cdPort, "", logger)