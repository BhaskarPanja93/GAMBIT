from gevent import monkey

from internal.Enums import Routes

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from flask import Flask

from internal.SecretEnums import ServerSecrets

connectionApp = Flask("Connection")


@connectionApp.get(Routes.connCheck.value)
def _checkConn():
    return ""

@connectionApp.get(Routes.connCreate.value)
def _createConn():
    return ""

@connectionApp.get(Routes.connChange.value)
def _changeConn():
    return ""

@connectionApp.get(Routes.connDestroy.value)
def _destroyConn():
    return ""


print(f"CONN: http://127.0.0.1:{ServerSecrets.connectionPort.value}")
WSGIServer(('0.0.0.0', ServerSecrets.connectionPort.value,), connectionApp, log=None).serve_forever()