from gevent import monkey

from internal.Enums import Routes

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from flask import Flask

from internal.SecretEnums import ServerSecrets

CDNApp = Flask("CDN")

@CDNApp.get(Routes.cdnMemoryContent.value)
def _memContent():
    return ""


@CDNApp.get(Routes.cdnFileContent.value)
def _fileContent():
    return ""


print(f"CDN: http://127.0.0.1:{ServerSecrets.webPort.value}")
WSGIServer(('0.0.0.0', ServerSecrets.webPort.value,), CDNApp, log=None).serve_forever()