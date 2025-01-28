from __future__ import annotations
__version__ = "2.0.0beta1"
__packagename__ = "dynamicWebsite"


def updatePackage():
    from time import sleep
    from json import loads
    import http.client
    print(f"Checking updates for Package {__packagename__}")
    try:
        host = "pypi.org"
        conn = http.client.HTTPSConnection(host, 443)
        conn.request("GET", f"/pypi/{__packagename__}/json")
        data = loads(conn.getresponse().read())
        latest = data['info']['version']
        if latest != __version__:
            try:
                import subprocess
                from pip._internal.utils.entrypoints import (
                    get_best_invocation_for_this_pip,
                    get_best_invocation_for_this_python,
                )
                from pip._internal.utils.compat import WINDOWS
                if WINDOWS:
                    pip_cmd = f"{get_best_invocation_for_this_python()} -m pip"
                else:
                    pip_cmd = get_best_invocation_for_this_pip()
                subprocess.run(f"{pip_cmd} install {__packagename__} --upgrade")
                print(f"\nUpdated package {__packagename__} v{__version__} to v{latest}\nPlease restart the program for changes to take effect")
                sleep(3)
            except:
                print(f"\nFailed to update package {__packagename__} v{__version__} (Latest: v{latest})\nPlease consider using pip install {__packagename__} --upgrade")
                sleep(3)
        else:
            print(f"Package {__packagename__} already the latest version")
    except:
        print(f"Ignoring version check for {__packagename__} (Failed)")


class Imports:
    from flask import Flask, Request, Response, send_file, render_template_string, make_response, request
    from flask_sock import Sock, ConnectionClosed
    from json import dumps, loads
    from time import time, sleep
    from threading import Thread
    from cryptography.fernet import Fernet
    from urllib.parse import urlparse
    from bidict import bidict
    from typing import Any
    from base64 import urlsafe_b64decode, urlsafe_b64encode
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.hashes import SHA256
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from rateLimitedQueues import RateLimitedQueues
    from randomisedString import RandomisedString


class DynamicWebsite:


    class WS_DATA_TYPES:
        FILE_PART = "FP"
        FORM = "F"
        CUSTOM = "C"


    class VIEWER_STATES:
        CREATED = "CREATED"
        DEAD = "DEAD"
        INCOMPLETE = "INCOMPLETE"
        COMPLETE = "COMPLETE"
        DYING = "DYING"

    class WS_DATA_REASONS:
        class IN:
            VERIFY_CSRF = "CSRF-VERIFY"
            READY = "READY"
            CLIENT_KEY = "CLIENT-KEY"
        class OUT:
            TURBO = "TURBO"
            FUTURE_CSRF = "FUTURE-CSRF"
            CSRF_ACCEPTED = "CSRF-ACCEPTED"


    class WSPurposes:
        RESPONSIVE = "RESPONSIVE"
        LARGE = "LARGE"


    class UpdateMethods:
        """
        All allowed methods for updating content into divs
        """
        append = "append"
        prepend = "prepend"
        replace = "replace"
        update = "update"
        remove = "remove"
        after = "after"
        before = "before"


    class ERRORS:
        class InvalidHTML(Exception):
            pass


    class HTMLElements:
        giveMeTheFile = "GIVE_ME_THE_FILE"
        dynamicWebsiteFilename = "dynamicWebsite.js"
        hotWireFilename = "hotwire.js"
        replaceActionRoutePlaceholder = "REPLACE_ACTION_ROUTE"
        replaceExtraHeadsPlaceholder = "REPLACE_EXTRA_HEADS"
        replaceTitlePlaceholder = "REPLACE_TITLE"
        replaceBodyPlaceholder = "REPLACE_BODY"

        baseBody = """
        <body>
            <div id="root"></div>
        </body>"""

        baseHTML = f"""
            <html>
                <head>
                    <script type="text/javascript" src="{replaceActionRoutePlaceholder}?{giveMeTheFile}={hotWireFilename}"></script>
                    <script type="text/javascript" src="{replaceActionRoutePlaceholder}?{giveMeTheFile}={dynamicWebsiteFilename}"></script>
                    <title>{replaceTitlePlaceholder}</title>
                    {replaceExtraHeadsPlaceholder}
                </head>
                {replaceBodyPlaceholder}
            </html>
            """


    class CookieHolder:
        """
        Internal DataStructure to hold a visitor's uniquely identifying information and methods to convert to and from cookies
        """

        def __init__(self, instanceID: str = "", viewer: DynamicWebsite.Viewer | None = None):
            self.instanceID = instanceID
            self.viewer = viewer
            self.stage = 0

            self.remoteAddress = None
            self.userAgent = None
            self.viewerID = None
            self.hostURL = None

            self.language = None
            self.platform = None
            self.screenResolution = None
            self.colorDepth = None
            self.timezone = None
            self.plugins = None

            self.lastActivity = None
            self.currentActivity = None


        def readL1(self, requestObj: Imports.Request) -> DynamicWebsite.CookieHolder:
            """
            Read from a request context environ object into current cookie object and return itself
            :param requestObj: the request context to read from
            :return:
            """
            self.remoteAddress = requestObj.remote_addr
            self.userAgent = requestObj.user_agent.string
            parsedURL = Imports.urlparse(requestObj.host_url)
            self.hostURL = f"{parsedURL.hostname}{f':{parsedURL.port}' if parsedURL.port is not None else ''}"
            self.stage = 1
            return self


        def readL2(self, data: dict) -> DynamicWebsite.CookieHolder:
            """
            Read from a WebSocket's identity and return itself
            :param data: the WS data to read from
            :return:
            """
            self.language = data.get("L")
            self.platform = data.get("PF")
            self.screenResolution = data.get("S_R")
            self.colorDepth = data.get("C_D")
            self.timezone = data.get("T_Z")
            self.plugins = data.get("PL")
            self.instanceID = data.get("IN")
            self.stage = 2
            return self


        def export(self, stage:int) -> dict:
            if stage == 1:
                return (
                    {"H_U": self.hostURL,
                     "R_A": self.remoteAddress,
                     "U_A": self.userAgent,
                     "V_ID": self.viewerID,
                     "IN": self.instanceID
                     })
            elif stage == 2:
                return (
                    {"H_U": self.hostURL,
                     "R_A": self.remoteAddress,
                     "U_A": self.userAgent,
                     "V_ID": self.viewerID,
                     "L": self.language,
                     "PF": self.platform,
                     "S_R": self.screenResolution,
                     "C_D": self.colorDepth,
                     "T_Z": self.timezone,
                     "PL": self.plugins,
                     "L_A": self.lastActivity,
                     "C_A": self.currentActivity,
                     "S": self.stage,
                     "IN": self.instanceID,
                     })


        def readDict(self, inputDict: dict) -> DynamicWebsite.CookieHolder:
            """
            Read from a dictionary into current cookie object and return itself
            :param inputDict: the dictionary to read from
            :return:
            """
            self.remoteAddress = inputDict["R_A"]
            self.userAgent = inputDict["U_A"]
            self.viewerID = inputDict["V_ID"]
            self.hostURL = inputDict["H_U"]
            self.language = inputDict.get("L")
            self.platform = inputDict.get("PF")
            self.screenResolution = inputDict.get("S_R")
            self.colorDepth = inputDict.get("C_D")
            self.timezone = inputDict.get("T_Z")
            self.plugins = inputDict.get("PL")
            self.lastActivity = inputDict.get("L_A")
            self.currentActivity = inputDict.get("C_A")
            self.stage = inputDict.get("S")
            self.instanceID = inputDict.get("IN")
            return self


        def wrapResponse(self, response: Imports.Response, fernetKey: str) -> Imports.Response:
            """
            Attach required cookies and headers into argument response object of Response type and return it
            :param response: the response object to attach cookies and headers to
            :param fernetKey: the fernet string to encrypt the cookie with
            :return:
            """
            for stage in range(1, self.stage+1):
                response.set_cookie(f"DW-ID-L{stage}", Imports.Fernet(fernetKey).encrypt(Imports.dumps(self.export(stage)).encode()).decode(), expires=Imports.time() + 30 * 24 * 60 * 60, httponly=True)
            return response


        def decrypt(self, cookieStr: str, fernetKey) -> DynamicWebsite.CookieHolder:
            """
            Check if a request.cookie is valid and imports its values into self and return itself
            :param cookieStr: the cookie string received from request object
            :param fernetKey: the fernet string to decrypt the cookie with
            :return:
            """
            try:
                self.readDict(Imports.loads(Imports.Fernet(fernetKey).decrypt(cookieStr.encode())))
            except:
                pass
            return self


        def match(self, other: DynamicWebsite.CookieHolder, stage: int, withViewerID: bool=False, withInstanceID: bool=False) -> bool:
            # TODO: add fuzzy Imports.SequenceMatcher(None, str(self), str(other)).ratio() > 0.8
            if stage == 1:
                return (self.userAgent == other.userAgent and self.remoteAddress == other.remoteAddress and self.hostURL == other.hostURL
                        and (not withViewerID or self.viewerID == other.viewerID) and (not withInstanceID or self.instanceID == other.instanceID))
            elif stage == 2:
                return self.match(other, 1, withViewerID, withInstanceID) and (self.language == other.language and self.platform == other.platform and self.screenResolution == other.screenResolution
                                                                               and self.colorDepth == other.colorDepth and self.timezone == other.timezone and self.plugins == other.plugins)


    class FileHolder:
        """
        Internal Structure for receiving parts of Files uploaded by Visitor and storing when required by the server
        """
        def __init__(self, viewer: DynamicWebsite.Viewer, fileID):
            self.viewer = viewer
            self.isReady = False
            self.isCurrentlySaving = False
            self.startedSaving = False
            self.lastPartSaved = -1
            self.ID = fileID
            self.fileName = ""
            self.fileType = ""
            self.fileSize = 0
            self.maxPartIndex = 0
            self.lastPartReceivedAt = Imports.time()

            self.parts = {}


        def acceptNewData(self, fileData:dict):
            partIndex = fileData["C"]
            data = Imports.urlsafe_b64decode(self.viewer.dynamicWebsiteApp.fixB64Pads(fileData["D"]))
            self.lastPartReceivedAt = Imports.time()
            if partIndex == self.maxPartIndex:
                self.isReady = True
            if self.startedSaving:
                if partIndex == self.lastPartSaved + 1 and not self.isCurrentlySaving:
                    self._directSave(partIndex, data)
                    return
            self.parts[partIndex] = data


        def _directSave(self, partIndex, data):
            if data is not None or partIndex in self.parts:
                self.isCurrentlySaving = True
                self.lastPartSaved = partIndex
                with open(self.fileName, "ab") as f: f.write(data)
                self.isCurrentlySaving = False
                self._directSave(partIndex+1, None)


        def save(self, fileName: str|None = None):
            self.fileName = fileName or self.fileName
            if not self.startedSaving:
                open(self.fileName, "wb").close()
                self.startedSaving = True
            if not self.isCurrentlySaving:
                self._directSave(self.lastPartSaved+1, None)


    class PurposeManager:
        def __init__(self, viewer: DynamicWebsite.Viewer, stringGenerator: Imports.RandomisedString):
            self.viewer = viewer
            self.stringGenerator = stringGenerator
            self.activeCSRF: dict[str, list[str]] = {}
            self.knownPurposes:Imports.bidict = Imports.bidict()


        def encryptedPurpose(self, purpose: str):
            if purpose not in self.knownPurposes:
                encrypted = self.stringGenerator.AlphaNumeric(5, 5)
                self.knownPurposes[purpose] = encrypted
                self.activeCSRF[encrypted] = []
            return self.knownPurposes.get(purpose)


        def decryptedPurpose(self, purpose: str):
            return self.knownPurposes.inverse.get(purpose)


        def createCSRF(self, purpose: str, deleteAfter: int = -1):
            hiddenPurpose = self.encryptedPurpose(purpose)
            csrf = self.stringGenerator.AlphaNumeric(_min=10, _max=10)
            purposeString = f"{hiddenPurpose}.{csrf}"
            self.activeCSRF[hiddenPurpose].append(csrf)
            if deleteAfter > 0: Imports.Thread(target=self.deleteCSRF, args=(hiddenPurpose, csrf, deleteAfter)).start()
            return f"""<input type="hidden" name="PURPOSE_CSRF" value="{purposeString}">"""


        def deleteCSRF(self, hiddenPurpose: str, csrf: str, timeToWait: int):
            for countDown in range(timeToWait, 0, -1):
                if csrf not in self.activeCSRF[hiddenPurpose]:
                    return
            else:
                self.activeCSRF[hiddenPurpose].remove(csrf)


        def checkCSRFPurpose(self, purposeString: str):
            hiddenPurpose, csrf = purposeString.split(".")
            if csrf not in self.activeCSRF[hiddenPurpose]:
                return None
            else:
                self.activeCSRF[hiddenPurpose].remove(csrf)
                return self.decryptedPurpose(hiddenPurpose)


    class ServerKeyHolder:
        def __init__(self):
            self._privateKey = None
            self._publicKeyDER = None
            self._generatingKeys = False
            self._generateServerKeys()

        def pubB64(self):
            return Imports.urlsafe_b64encode(self._publicKeyDER).decode()

        def sharedKey(self, clientPubB64, salt, info):
            return Imports.HKDF(
                algorithm=Imports.SHA256(),
                length=32,
                salt=salt,
                info=info,
            ).derive(self._privateKey.exchange(Imports.ec.ECDH(), Imports.serialization.load_der_public_key(Imports.urlsafe_b64decode(clientPubB64))))


        def _generateServerKeys(self):
            if self._generatingKeys:
                while self._privateKey is None or self._publicKeyDER is None:
                    Imports.sleep(1)
                return
            self._generatingKeys = True
            self._privateKey = Imports.ec.generate_private_key(Imports.ec.SECP256R1())
            self._publicKeyDER = self._privateKey.public_key().public_bytes(
                encoding=Imports.serialization.Encoding.DER,
                format=Imports.serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            self._generatingKeys = False


    class WSHolder:
        def __init__(self, rawWS, salt: bytes, info: bytes):
            self.isActive = None
            self.rawWS = rawWS
            self.purpose = None
            self.queue = Imports.RateLimitedQueues()

            self.key = None
            self.salt = salt
            self.info = info


        def encrypt(self, message: str, iv: bytes):
            enc = Imports.Cipher(
                Imports.algorithms.AES(self.key),
                Imports.modes.GCM(iv),
                backend=Imports.default_backend(),
            ).encryptor()
            return {
                "eB64": Imports.urlsafe_b64encode(enc.update(message.encode()) + enc.finalize()).decode(),
                "ivB64": Imports.urlsafe_b64encode(iv).decode(),
                "tagB64": Imports.urlsafe_b64encode(enc.tag).decode(),
            }


        def decrypt(self, json:dict):
            dec = Imports.Cipher(
                Imports.algorithms.AES(self.key),
                Imports.modes.GCM(Imports.urlsafe_b64decode(DynamicWebsite.fixB64Pads(json["ivB64"])), Imports.urlsafe_b64decode(DynamicWebsite.fixB64Pads(json["tagB64"]))),
                backend=Imports.default_backend(),
            ).decryptor()
            return (dec.update(Imports.urlsafe_b64decode(DynamicWebsite.fixB64Pads(json["eB64"]))) + dec.finalize()).decode()


        def sendRaw(self, finalData):
            self.queue.queueAction(self.rawWS.send, False, 0, None, None, None, None, finalData)


    class Viewer:
        """
        Internal DataStructure to hold all information regarding individual visitor
        """
        def __init__(self, dynamicWebsiteApp: DynamicWebsite):
            self.arrivalCalled: bool = False
            self.currentState = DynamicWebsite.VIEWER_STATES.CREATED
            self.dynamicWebsiteApp = dynamicWebsiteApp
            self.purposeManager = DynamicWebsite.PurposeManager(self, self.dynamicWebsiteApp.stringGenerator)
            self.addCSRF = self.createCSRF = self.purposeManager.createCSRF
            self.formSubmitCallback = self.dynamicWebsiteApp.formSubmitCallback
            self.customMessageCallback = self.dynamicWebsiteApp.customMessageCallback
            self.pendingFiles:dict[str, DynamicWebsite.FileHolder] = {}
            self.currentWS:dict[str, DynamicWebsite.WSHolder|str|None] = {}
            self.futureWS:dict[str, str] = {}
            self.cookie: DynamicWebsite.CookieHolder|None = None
            self.viewerID:str|None = None
            self.privateData = None


        def sendTurbo(self, stream, highPriority: bool = True):
            WSObj = self.currentWS.get(DynamicWebsite.WSPurposes.RESPONSIVE) if highPriority and self.currentWS.get(DynamicWebsite.WSPurposes.RESPONSIVE) else self.currentWS.get(DynamicWebsite.WSPurposes.LARGE)
            if WSObj is None:
                Imports.sleep(1)
                return self.sendTurbo(stream, highPriority)
            try:
                if self.currentState != DynamicWebsite.VIEWER_STATES.DEAD:
                    toSend = Imports.dumps({"REASON":self.dynamicWebsiteApp.WS_DATA_REASONS.OUT.TURBO, "DATA": stream})
                    if WSObj.key is not None and WSObj.key != True:
                        if WSObj.key:
                            toSend = Imports.dumps(WSObj.encrypt(toSend, self.dynamicWebsiteApp.stringGenerator.AlphaNumeric(12,12).encode()))
                    WSObj.sendRaw(toSend)
            except (BrokenPipeError, Imports.ConnectionClosed):  # pragma: no cover
                print("Unable to send. Connection closed")


        def sendCustomMessage(self, data: Imports.Any, highPriority: bool = True):
            WSObj = self.currentWS.get(DynamicWebsite.WSPurposes.RESPONSIVE) if highPriority and self.currentWS.get(DynamicWebsite.WSPurposes.RESPONSIVE) else self.currentWS.get(DynamicWebsite.WSPurposes.LARGE)
            if WSObj is None:
                Imports.sleep(1)
                return self.sendCustomMessage(data)
            try:
                if self.currentState != DynamicWebsite.VIEWER_STATES.DEAD:
                    toSend = Imports.dumps({"T":self.dynamicWebsiteApp.WS_DATA_TYPES.CUSTOM, "DATA": data})
                    if WSObj.key is not None and WSObj.key != True:
                        if WSObj.key:
                            toSend = Imports.dumps(WSObj.encrypt(toSend, self.dynamicWebsiteApp.stringGenerator.AlphaNumeric(12,12).encode()))
                    WSObj.sendRaw(toSend)
            except (BrokenPipeError, Imports.ConnectionClosed):  # pragma: no cover
                print("Unable to send. Connection closed")


        def receive(self, data:dict):
            TYPE = data.pop("T")

            if TYPE == DynamicWebsite.WS_DATA_TYPES.CUSTOM:
                Imports.Thread(target=self.customMessageCallback, args=(self, data.get("D"),)).start()

            elif TYPE == DynamicWebsite.WS_DATA_TYPES.FORM:
                formData = data.get("D")
                purpose = self.purposeManager.checkCSRFPurpose(formData.pop("PURPOSE_CSRF"))
                if purpose is not None:
                    formData["PURPOSE"] = purpose
                    files = formData.pop("DW_FILES_IN_FORM")
                    for elementName in files:
                        formData[elementName] = []
                        for fileId in files[elementName]:
                            fileObj = self.dynamicWebsiteApp.createFile(self, fileId)
                            fileObj.fileName = files[elementName][fileId]["NAME"]
                            fileObj.fileSize = files[elementName][fileId]["SIZE"]
                            fileObj.fileType = files[elementName][fileId]["TYPE"]
                            fileObj.maxPartIndex = files[elementName][fileId]["MAXPART"]
                            formData[elementName].append(fileObj)
                    self.formSubmitCallback(self, formData)

            elif TYPE == DynamicWebsite.WS_DATA_TYPES.FILE_PART:
                fileID = data.pop("FID")
                if fileID in self.pendingFiles:
                    self.pendingFiles[fileID].acceptNewData(data)


        def updateHTML(self, htmlData: str, divID: str, method: str, nonBlockingWait: float = 0, removeAfter: float = 0, blockingWait: float = 0, newDivAttributes: dict|None = None, highPriority: bool = True) -> str|None:
            if type(htmlData) != str:
                try: htmlData = Imports.dumps(htmlData)
                except:
                    try: htmlData = str(htmlData)
                    except: raise DynamicWebsite.ERRORS.InvalidHTML

            if nonBlockingWait > 0:
                blockingWait = nonBlockingWait
                return Imports.Thread(target=self.updateHTML, args=(htmlData, divID, method, 0, removeAfter, blockingWait, newDivAttributes)).start()

            if blockingWait > 0:
                Imports.sleep(blockingWait)
                return self.updateHTML(htmlData, divID, method, 0, removeAfter, 0, newDivAttributes)
            #
            # if method == DynamicWebsite.UpdateMethods.newDiv:
            #     readDivID = divID
            #     divID = f"{readDivID}.{self.stringGenerator.AlphaNumeric(_min=5, _max=5)}"
            #     divAttributes = ""
            #     if newDivAttributes:
            #         for key in newDivAttributes:
            #             value = newDivAttributes[key]
            #             divAttributes+=f' {key}=\"{value}\"'
            #     self.updateHTML(f"""<div id='{divID}'{divAttributes}></div><div id='{readDivID}'></div>""", f'{readDivID}_create', DynamicWebsite.UpdateMethods.replace, 0, 0)
            #     self.updateHTML(htmlData, divID, self.turboApp.methods.update, nonBlockingWait, removeAfter)


            stream =  f'<turbo-stream action="{method}" target="{divID}"><template>{htmlData}</template></turbo-stream>'
            self.sendTurbo(stream, highPriority)
            if removeAfter: self.updateHTML("", divID, DynamicWebsite.UpdateMethods.remove, removeAfter)
            return divID


    def __init__(self, visitorArrivedCallback, visitorLeftCallback, formCallback, customMessageCallback, fernetKey:str=Imports.Fernet.generate_key(), appName:str = "Live App", actionsRoute:str= "/", extraHeads:str= "", body:str= HTMLElements.baseBody, title:str= "Live"):
        self.formSubmitCallback = formCallback
        self.customMessageCallback = customMessageCallback
        self.visitorArrivedCallback = visitorArrivedCallback
        self.visitorLeftCallback = visitorLeftCallback
        self.appName = appName
        self.actionsRoute = actionsRoute
        self.fernetKey = fernetKey
        self.extraHeads = extraHeads
        self.body = body
        self.title = title

        self.pendingL1Cookies:dict[str, dict[int, DynamicWebsite.CookieHolder|None]] = {}
        self.inCompleteViewers:dict[str, DynamicWebsite.Viewer] = {}
        self.completeViewers:dict[str, DynamicWebsite.Viewer] = {}

        self.serverKeys = self.ServerKeyHolder()
        self.stringGenerator = Imports.RandomisedString()

        self.baseApp = Imports.Flask(self.appName)
        self.visitorLeftCallback = visitorLeftCallback
        self.baseApp.config.setdefault('TURBO_WEBSOCKET_ROUTE', actionsRoute)
        self.sock = Imports.Sock(self.baseApp)


    def createL1Cookie(self, requestObj: Imports.Request) -> DynamicWebsite.CookieHolder:
        newL1Cookie = self.CookieHolder().readL1(requestObj)
        instanceID = newL1Cookie.instanceID = self.stringGenerator.AlphaNumeric(40, 40)
        newL1Cookie.viewerID = self.stringGenerator.AlphaNumeric(30, 30)
        presentL1Cookie = self.CookieHolder().decrypt(requestObj.cookies.get("DW-ID-L1"), self.fernetKey)
        presentL2Cookie = self.CookieHolder().decrypt(requestObj.cookies.get("DW-ID-L2"), self.fernetKey)
        self.pendingL1Cookies[instanceID] = {1: presentL1Cookie, 2: presentL2Cookie}
        Imports.Thread(target=self.freeL1Cookie, args=(instanceID, 5,)).start()
        return newL1Cookie


    def freeL1Cookie(self, instanceID: str, timeToWait: int):
        for _ in range(timeToWait, 0, -1):
            Imports.sleep(1)
            if instanceID not in self.pendingL1Cookies:
                return
        if instanceID in self.pendingL1Cookies: del self.pendingL1Cookies[instanceID]


    def createViewer(self, requestObj: Imports.Request, L2Values: dict) -> DynamicWebsite.Viewer | None:
        validCookie = self.CookieHolder().readL1(requestObj).readL2(L2Values)
        presentL1Cookie = self.CookieHolder().decrypt(requestObj.cookies.get("DW-ID-L1"), self.fernetKey)
        presentL2Cookie = self.CookieHolder().decrypt(requestObj.cookies.get("DW-ID-L2"), self.fernetKey)
        validCookie.viewerID = presentL1Cookie.viewerID
        if presentL1Cookie.instanceID in self.pendingL1Cookies and validCookie.match(presentL1Cookie, 1): # current person is recent person
            viewer = self.Viewer(self)
            dump = self.pendingL1Cookies.pop(presentL1Cookie.instanceID)
            previousL1Cookie = dump.get(1)
            previousL2Cookie = dump.get(2)
            if (previousL2Cookie.viewerID and
                    validCookie.match(previousL2Cookie, 1) and
                    presentL1Cookie.match(previousL1Cookie, 1) and
                    presentL2Cookie.match(previousL2Cookie, 2, True, True) and
                    previousL2Cookie.match(previousL1Cookie, 1, True, True)
            ):
                validCookie.viewerID = previousL2Cookie.viewerID
            else:
                validCookie.viewerID = presentL1Cookie.viewerID
            validCookie.instanceID = presentL1Cookie.instanceID
            viewer.cookie = validCookie
            viewer.viewerID = validCookie.viewerID
            self.makeViewerInComplete(viewer)
            Imports.Thread(target=self.makeViewerDying, args=(viewer, 4, False)).start()
            return viewer
        return None


    def createWSToken(self, viewer: DynamicWebsite.Viewer, purpose: str, future: bool):
        if not future and viewer.currentWS.get(purpose) is None:
            self.makeViewerInComplete(viewer)
            newCSRF = self.stringGenerator.AlphaNumeric(50, 50)
            viewer.currentWS[purpose] = newCSRF
            return newCSRF
        if future and viewer.futureWS.get(purpose) is None:
            newCSRF = self.stringGenerator.AlphaNumeric(50, 50)
            viewer.futureWS[purpose] = newCSRF
            return newCSRF


    def makeViewerComplete(self, viewer: DynamicWebsite.Viewer):
        viewer.currentState = self.VIEWER_STATES.COMPLETE
        if viewer.cookie.instanceID in self.inCompleteViewers:
            del self.inCompleteViewers[viewer.cookie.instanceID]
        if viewer.cookie.instanceID not in self.completeViewers:
            self.completeViewers[viewer.cookie.instanceID] = viewer


    def makeViewerInComplete(self, viewer: DynamicWebsite.Viewer):
        viewer.currentState = self.VIEWER_STATES.INCOMPLETE
        if viewer.cookie.instanceID in self.completeViewers:
            del self.completeViewers[viewer.cookie.instanceID]
        if viewer.cookie.instanceID not in self.inCompleteViewers:
            self.inCompleteViewers[viewer.cookie.instanceID] = viewer


    def makeViewerDying(self, viewer: DynamicWebsite.Viewer, timeToWait: int, triggerViewerLeftCallback: bool = True):
        for countDown in range(timeToWait, 0, -1):
            Imports.sleep(1)
            if viewer.currentState != self.VIEWER_STATES.DYING:
                return
        self.makeViewerDead(viewer, triggerViewerLeftCallback)


    def makeViewerDead(self, viewer: DynamicWebsite.Viewer, triggerViewerLeftCallback: bool = True):
        viewer.currentState = self.VIEWER_STATES.DEAD
        if viewer.cookie.instanceID not in self.inCompleteViewers:
            del self.inCompleteViewers[viewer.cookie.instanceID]
        if viewer.cookie.instanceID not in self.completeViewers:
            del self.completeViewers[viewer.cookie.instanceID]
        if triggerViewerLeftCallback: self.visitorLeftCallback(viewer)


    def createFile(self, viewer: DynamicWebsite.Viewer, fileID):
        file = self.FileHolder(viewer, fileID)
        viewer.pendingFiles[fileID] = file
        Imports.Thread(target=self.deleteFileOnInactivity, args=(file,)).start()
        return file


    def deleteFileOnInactivity(self, file: DynamicWebsite.FileHolder):
        while True:
            Imports.sleep(1)
            if (file.viewer.currentState == self.VIEWER_STATES.DEAD or file.isReady or Imports.time() - file.lastPartReceivedAt > 60) and file.ID in file.viewer.pendingFiles:
                del file.viewer.pendingFiles[file.ID]
                break


    @staticmethod
    def fixB64Pads(B64String):
        return B64String + '=' * (4 - len(B64String) % 4)


    def start(self):


        @self.baseApp.before_request
        def _modHeadersBeforeRequest():
            """
            Before any request goes to any route, it passes through this function.
            Applies user remote address correctly (received from proxy)
            :return:
            """
            if Imports.request.remote_addr == "127.0.0.1":
                if Imports.request.environ.get("HTTP_X_FORWARDED_FOR") is not None:
                    address = Imports.request.environ.get("HTTP_X_FORWARDED_FOR")
                else: address = "LOCALHOST"
                Imports.request.remote_addr = address


        @self.baseApp.route(self.actionsRoute, methods=["GET", "POST"])
        def _actionRoute():
            """
            Generates new ViewerID or uses old one and generates and sends a 2-phase cookie
            :return:
            """
            if Imports.request.args.get(self.HTMLElements.giveMeTheFile) == "dynamicWebsite.js":
                return Imports.send_file("dynamicWebsite.js"), 200
            elif Imports.request.args.get(self.HTMLElements.giveMeTheFile) == "hotwire.js":
                return Imports.send_file("hotwire.js"), 200
            # Requesting L2 Cookie
            if "RECEIVE_NEW_L2_COOKIE" in Imports.request.args:
                viewerObj = self.createViewer(Imports.request, Imports.request.get_json())
                if viewerObj is None:
                    return ""
                viewerObj.currentWS[self.WSPurposes.RESPONSIVE] = None
                viewerObj.currentWS[self.WSPurposes.LARGE] = None
                response = Imports.make_response({
                    self.WSPurposes.RESPONSIVE: self.createWSToken(viewerObj, self.WSPurposes.RESPONSIVE, True),
                    self.WSPurposes.LARGE: self.createWSToken(viewerObj, self.WSPurposes.LARGE, True)
                })
                return viewerObj.cookie.wrapResponse(response, self.fernetKey)

            # Requesting L1 Cookie
            else:
                response = Imports.make_response(Imports.render_template_string(self.HTMLElements.baseHTML
                                                                                .replace(self.HTMLElements.replaceActionRoutePlaceholder, self.actionsRoute)
                                                                                .replace(self.HTMLElements.replaceBodyPlaceholder, self.body)
                                                                                .replace(self.HTMLElements.replaceExtraHeadsPlaceholder, self.extraHeads)
                                                                                .replace(self.HTMLElements.replaceTitlePlaceholder, self.title)))
                return self.createL1Cookie(Imports.request).wrapResponse(response, self.fernetKey)


        @self.sock.route(self.actionsRoute)
        def _turboRoute(rawWS):
            """
            Executed for every websocket connection request received. Handles initial handshake token exchange along with all future communication
            :param rawWS: The Sock object that will be used for communication
            :return:
            """
            validCookie = self.CookieHolder().readL1(Imports.request)
            presentL1Cookie = self.CookieHolder().decrypt(Imports.request.cookies.get("DW-ID-L1"), self.fernetKey)
            presentL2Cookie = self.CookieHolder().decrypt(Imports.request.cookies.get("DW-ID-L2"), self.fernetKey)
            WSObj = self.WSHolder(rawWS, self.stringGenerator.AlphaNumeric(10,10).encode(), self.stringGenerator.AlphaNumeric(10,10).encode())
            WSObj.purpose = Imports.request.args.get("WS_PURPOSE")
            if presentL1Cookie.instanceID in self.inCompleteViewers and self.inCompleteViewers[presentL1Cookie.instanceID].currentWS.get(WSObj.purpose) is None and type(self.inCompleteViewers[presentL1Cookie.instanceID].futureWS.get(WSObj.purpose)) == str and validCookie.match(presentL1Cookie, 1) and presentL2Cookie.match(presentL1Cookie, 1, True, True): # current person is recent person
                viewerObj = self.inCompleteViewers[presentL1Cookie.instanceID]
                CSRFVerified = False
                while True:
                    try:
                        receivedBytes = rawWS.receive(timeout=60 if CSRFVerified else 5)
                    except (BrokenPipeError, Imports.ConnectionClosed):
                        WSObj.isActive = False
                        viewerObj.currentWS[WSObj.purpose] = None
                        futureCSRF = viewerObj.futureWS.get(WSObj.purpose)
                        if futureCSRF is None:
                            for _WSObj in viewerObj.currentWS.values():
                                if _WSObj.isActive: # Has active WS
                                    self.makeViewerInComplete(viewerObj)
                                    break
                            else: # No active WS
                                self.makeViewerDying(viewerObj, 2) ## Viewer left callback is called 2 seconds after he actually leaves (giving them a scope to reconnect in cases of network disconnections)
                        break
                    if receivedBytes is None and not CSRFVerified: break # WS couldn't prove authenticity in specified time
                    if receivedBytes:
                        dictReceived:dict = Imports.loads(receivedBytes)
                        reason = dictReceived.get("REASON")

                        if WSObj.key is None: # Should be the first data from WS
                            if reason == self.WS_DATA_REASONS.IN.VERIFY_CSRF:
                                if viewerObj.currentWS.get(WSObj.purpose) is None and viewerObj.futureWS.get(WSObj.purpose) == dictReceived["CSRF"] and viewerObj.futureWS.get(WSObj.purpose): # Viewer has pending CSRF of same purpose and is valid
                                    del viewerObj.futureWS[WSObj.purpose]
                                    viewerObj.currentWS[WSObj.purpose] = WSObj
                                    requireEncryption= dictReceived.get("REQUEST_ENCRYPTION", False)
                                    if requireEncryption:
                                        WSObj.key = self.serverKeys.sharedKey(dictReceived.get("CLIENT-KEY").get("PubB64"), WSObj.salt, WSObj.info)
                                        rawWS.send(Imports.dumps({"REASON": self.WS_DATA_REASONS.OUT.CSRF_ACCEPTED, "SERVER-KEY": {"PubB64":self.serverKeys.pubB64(), "SaltB64": Imports.urlsafe_b64encode(WSObj.salt).decode(), "InfoB64": Imports.urlsafe_b64encode(WSObj.info).decode()}}))
                                    else:
                                        WSObj.key = False
                                        rawWS.send(Imports.dumps({"REASON": self.WS_DATA_REASONS.OUT.CSRF_ACCEPTED}))
                                    CSRFVerified = True
                                else:
                                    break
                        elif WSObj.key is not None and WSObj.key != True and CSRFVerified: # Encryption handshake complete (either success or fail)
                            if WSObj.key:
                                dictReceived = Imports.loads(WSObj.decrypt(dictReceived))
                                reason = dictReceived.get("REASON")
                            if reason == self.WS_DATA_REASONS.IN.READY:
                                if WSObj.key:
                                    rawWS.send(Imports.dumps(WSObj.encrypt(Imports.dumps({"FUTURE-CSRF": self.createWSToken(viewerObj, WSObj.purpose, True)}), self.stringGenerator.AlphaNumeric(12,12).encode())))
                                else:
                                    rawWS.send(Imports.dumps({"FUTURE-CSRF": self.createWSToken(viewerObj, WSObj.purpose, True)}))

                                WSObj.isActive = True
                                for _WSObj in viewerObj.currentWS.values():
                                    if _WSObj is None or WSObj.isActive is None: # Has incomplete CSRF
                                        break
                                else:
                                    if not viewerObj.arrivalCalled:
                                        viewerObj.arrivalCalled = True
                                        self.visitorArrivedCallback(viewerObj)
                                    self.makeViewerComplete(viewerObj)
                                continue
                            Imports.Thread(target=viewerObj.receive, args=(dictReceived,)).start()
                rawWS.close()
        return self.baseApp, self.sock
