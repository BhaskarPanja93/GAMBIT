from gevent import monkey

from internal.Enums import Routes

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from flask import Flask, request, send_from_directory

from Enums import *

CDNApp = Flask("CDN")

@CDNApp.get(Routes.cdnMemoryContent.value)
def _memContent():
    return ""


@CDNApp.get(Routes.cdnFileContent.value)
def _fileContent():
    fileType = request.args.get("type").strip()
    fileName = request.args.get("name").strip()
    if fileType == CDNFileType.font.value:
         return send_from_directory(folderLocation+"/static/font", fileName, as_attachment=True)


print(f"CDN: http://127.0.0.1:{ServerSecrets.webPort.value}")
WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), CDNApp, log=None).serve_forever()