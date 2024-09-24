from gevent import monkey

monkey.patch_all()


from gevent.pywsgi import WSGIServer
from flask import Flask, request, send_from_directory


from Enums import *


CDNApp = Flask("CDN")


@CDNApp.get(Routes.cdnMemoryContent.value)
def _memContent():
    return ""


@CDNApp.get(Routes.cdnLiveContent.value)
def _liveContent():
    return ""


@CDNApp.get(Routes.cdnFileContent.value)
def _fileContent():
    fileType = request.args.get("type").strip()
    fileName = request.args.get("name").strip()
    if fileType == CDNFileType.font.value:
         return send_from_directory(folderLocation+"/static/font", fileName, as_attachment=True)
    elif fileType == CDNFileType.image.value:
        return send_from_directory(folderLocation + "/static/image", fileName, as_attachment=True)
    elif fileType == CDNFileType.video.value:
        return send_from_directory(folderLocation + "/static/video", fileName, as_attachment=True)
    elif fileType == CDNFileType.html.value:
        return send_from_directory(folderLocation + "/static/html", fileName, as_attachment=True)
    elif fileType == CDNFileType.css.value:
        return send_from_directory(folderLocation + "/static/css", fileName, as_attachment=True)
    elif fileType == CDNFileType.js.value:
        return send_from_directory(folderLocation + "/static/js", fileName, as_attachment=True)


print(f"CDN: http://127.0.0.1:{ServerSecrets.cdnPort.value}")
WSGIServer(('0.0.0.0', ServerSecrets.cdnPort.value,), CDNApp, log=None).serve_forever()