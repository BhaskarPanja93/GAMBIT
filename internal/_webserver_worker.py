from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from dynamicWebsite import *

from internal.SecretEnums import *
from internal.Enums import *


def sendRegister(viewerObj: BaseViewer):
    registerHTML = f"""
        <form id="songForm" onsubmit="return submit_ws(this)" autocomplete="off">
            {viewerObj.addCSRF(FormPurposes.register.value)}
            <label for="songName">Register:</label><br>
            <input type="text" id="songName" name="songName"><br><br>
            <button type="submit">Register</button>
        </form>"""
    viewerObj.queueTurboAction(registerHTML, "register", viewerObj.turboApp.methods.update)

def sendLogin(viewerObj: BaseViewer):
    registerHTML = f"""
        <form id="songForm" onsubmit="return submit_ws(this)" autocomplete="off">
            {viewerObj.addCSRF(FormPurposes.login.value)}
            <label for="songName">Login:</label><br>
            <input type="text" id="songName" name="songName"><br><br>
            <button type="submit">Login</button>
        </form>"""
    viewerObj.queueTurboAction(registerHTML, "login", viewerObj.turboApp.methods.update)


def newVisitorCallback(viewerObj: BaseViewer):
    initial = "<div id=\"register\"></div><div id=\"login\"></div>"
    viewerObj.queueTurboAction(initial, "mainDiv", viewerObj.turboApp.methods.update)
    sendRegister(viewerObj)
    sendLogin(viewerObj)


def formSubmitCallback(viewerObj: BaseViewer, form: dict):
    if form is not None:
        purpose = form.pop("PURPOSE")

        if purpose == FormPurposes.register.value:
            print(form)

        elif purpose == FormPurposes.login.value:
            print(form)

    else:
        print("Disconnected: ", viewerObj.viewerID)


extraHeads = ""

baseApp, turboApp = createApps(formSubmitCallback, newVisitorCallback, WebsiteRelated.appName.value, Routes.homePageRoute.value, Routes.WSRoute.value, ServerSecrets.fernetKey.value, extraHeads, "Study Well", False)

print(f"http://127.0.0.1:{ServerSecrets.portToUse.value}{Routes.homePageRoute.value}")
WSGIServer(('0.0.0.0', ServerSecrets.portToUse.value,), baseApp, log=None).serve_forever()


