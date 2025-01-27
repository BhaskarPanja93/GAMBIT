// document.getElementById("dynamicWebsiteWebsocketHandshake").remove();
// let type1 = {T:"FP", D:{}
// let type2 = {T:"F", D:}
// let type3 = {T:"C", D:}


const WS_DATA_TYPES = {
    FILE_PART: "FP",
    FORM: "F",
    CUSTOM: "C",
}

const FORM_FILE_LIST_NAME = "DW_FILES_IN_FORM"


const WS_DATA_REASONS = {
    OUT : {
        VERIFY_CSRF: "CSRF-VERIFY",
        CLIENT_KEY: "CLIENT-KEY",
        READY: "READY"
    },
    IN : {
        TURBO: "TURBO",
        FUTURE_CSRF: "FUTURE-CSRF",
        CSRF_ACCEPTED: "CSRF-ACCEPTED",
    }
}


const WS_PURPOSES = {
    RESPONSIVE : "RESPONSIVE",
    LARGE : "LARGE",
}


const getDeviceFingerprint = function () {
    return JSON.stringify({
        L: navigator.language,
        PF: navigator.platform,
        S_R: `${screen.width}x${screen.height}`,
        C_D: screen.colorDepth,
        T_Z: Intl.DateTimeFormat().resolvedOptions().timeZone,
        PL: JSON.stringify(Array.from(navigator.plugins).map((plugin) => plugin.name)),
    })
}


const urlSafeBase64Encoded = function (arrayBuffer) {
    const uint8Array = new Uint8Array(arrayBuffer);
    let binaryString = '';
    const CHUNK_SIZE = 1024 * 1024;

    for (let i = 0; i < uint8Array.length; i += CHUNK_SIZE) {
        const chunk = uint8Array.subarray(i, i + CHUNK_SIZE);
        binaryString += Array.from(chunk, byte => String.fromCharCode(byte)).join('');
    }

    return btoa(binaryString)
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
};



const urlSafeBase64Decoded = function (base64String) {
    let padded = base64String.replace(/-/g, '+').replace(/_/g, '/');
    while (padded.length % 4) {
        padded += '=';
    }
    const binaryString = atob(padded);
    const CHUNK_SIZE = 1024*1024;
    const uint8Array = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i += CHUNK_SIZE) {
        const chunk = binaryString.slice(i, i + CHUNK_SIZE);
        for (let j = 0; j < chunk.length; j++) {
            uint8Array[i + j] = chunk.charCodeAt(j);
        }
    }
    return uint8Array;
}


class EventEmitter {
    constructor() {
        this.events = {};
    }
    addEventListener(eventName, listener) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }
        this.events[eventName].push(listener);
    }
    emit(eventName, ...args) {
        if (this.events[eventName]) {
            this.events[eventName].forEach(listener => listener(...args));
        }
    }
    removeEventListener(eventName, listener) {
        if (this.events[eventName]) {
            this.events[eventName] = this.events[eventName].filter(l => l !== listener);
        }
    }
}


class WSConnectionManager extends EventEmitter {
    constructor(RESPONSIVE_CSRF, LARGE_CSRF) {
        super();
        this.createNewWS(WS_PURPOSES.RESPONSIVE, RESPONSIVE_CSRF).then()
        this.createNewWS(WS_PURPOSES.LARGE, LARGE_CSRF).then()
        this.stopOperation = false
        window.addEventListener('beforeunload', (event) => {
            this.stopOperation = true;
            this.collectionWS.RESPONSIVE.close();
            this.collectionWS.LARGE.close();
        });
        this.sendCustomMessage = sendCustomMessage
    }

    async createNewWS(purpose, CSRF) {
        let WSObj = new this.WSClass(this, purpose)
        await WSObj.initialise(CSRF)
    }

    async handleAcceptedWS(WSObj) {
        if (this.collectionWS[WSObj.purpose] === undefined) this.collectionWS[WSObj.purpose] = WSObj
    }

    onMessageReceived(data) {
        if (data.REASON === WS_DATA_REASONS.IN.TURBO) {
            Turbo.session.streamObserver.receiveMessageHTML(data["DATA"])
        } else if (data.T===WS_DATA_TYPES.CUSTOM) {
            this.emit("message", data["DATA"])
        }
    }

    handleClosedWS(WSObj) {
        if (this.collectionWS[WSObj.purpose] !== undefined && this.stopOperation === false) {
            delete this.collectionWS[WSObj.purpose]
            if (WSObj.futureCSRF !== null) this.createNewWS(WSObj.purpose, WSObj.futureCSRF)
        }
    }

    totalBufferedAmount = () => {
        let totalBufferedAmount = 0
        Object.values(this.collectionWS).forEach(function(WSObj) {
            totalBufferedAmount += WSObj.bufferedAmount()
        })
        return totalBufferedAmount;
    }

    sendInQueue = async (string, purpose, ignoreBuffered, ignoreAuthentication, ignoreState) => {
        if (Object.keys(this.collectionWS).length < 1) {
            console.error("No active WS");
            return -1;
        }
        let WSObj = this.collectionWS[purpose]
        if (WSObj.canSend(ignoreBuffered, ignoreAuthentication, ignoreState)) {
            await WSObj.sendWS(string);
            return this.totalBufferedAmount();
        }
        return new Promise((resolve) => {
            setTimeout(async () => {
                const result = await this.sendInQueue(string, purpose, ignoreBuffered, ignoreAuthentication, ignoreState);
                resolve(result);
            }, window.DELAY_TIME);
        });
    };


    sendFORM = (form) => {
        const purpose = WS_PURPOSES.RESPONSIVE
        let form_data = Object.fromEntries(new FormData(form));
        form_data[FORM_FILE_LIST_NAME] = {}
        let filesToUpload = {};

        for (let formElementIndex = 0; formElementIndex < form.children.length; formElementIndex++)
        {
            let element = form.children[formElementIndex];
            if (element.type === "file")
            {
                let elementName = element.name;
                form_data[FORM_FILE_LIST_NAME][elementName] = {};
                delete form_data[elementName];
                for (let fileIndex = 0; fileIndex < element.files.length; fileIndex++)
                {
                    let file = element.files[fileIndex];
                    let fileID = this.fileIndex++
                    form_data[FORM_FILE_LIST_NAME][elementName][fileID] = {"NAME":file.name, "SIZE":file.size, "TYPE":file.type, "MAXPART":Math.ceil(file.size/window.CHUNK_SIZE)-1}
                    filesToUpload[fileID] = file;
                }
            }
        }
        form_data[FORM_FILE_LIST_NAME] = Object.assign({}, form_data[FORM_FILE_LIST_NAME])
        window.ConnmanagerWS.sendInQueue(JSON.stringify({T: WS_DATA_TYPES.FORM, D: form_data}), purpose).then(()=>{
            for (const [fileID, fileObj] of Object.entries(filesToUpload)) {
                let fileSender = new this.FileClass(this, fileID, fileObj);
                fileSender.resumeSending().then()
            }
        })
        return false
    }



    collectionWS = Object();
    fileIndex = 1;


    FileClass = class {
        constructor (connManager, fileID, file) {
            this.connManager = connManager
            this.fileID = fileID
            this.file = file
            this.lastSentPartIndex = -1
            this.maxPartIndex = Math.ceil(file.size/window.CHUNK_SIZE)-1
            this.reader = new FileReader();
            this.reader.fileClass = this
        }


        sendFile = (fileClass, index) => {
            let start_byte = index*window.CHUNK_SIZE
            this.reader.readAsArrayBuffer(this.file.slice(start_byte, Math.min(this.file.size, start_byte+(window.CHUNK_SIZE))));
            this.reader.onload = function (e) {
                fileClass.connManager.sendInQueue(JSON.stringify({
                    T: WS_DATA_TYPES.FILE_PART,
                    FID: fileClass.fileID,
                    C: index,
                    D: urlSafeBase64Encoded(e.target.result)
                }), WS_PURPOSES.LARGE).then(()=>{fileClass.resumeSending()})
            }
        }


        resumeSending = async () => {
            let indexToSend = ++this.lastSentPartIndex
            if (indexToSend > this.maxPartIndex) return
            this.sendFile(this, indexToSend)
        }
    }


    WSClass = class {

        constructor (handler, purpose) {
            this.handler = handler
            this.purpose = purpose
            this.futureCSRF = null
            this.key = (window.crypto.subtle !== undefined) && false
            this.clientKeyPair = null
            this.rawWS = new WebSocket(`ws${location.protocol.substring(4)}//${location.host}/?WS_PURPOSE=${this.purpose}`)
        }

        bufferedAmount = () => {
            return this.rawWS.bufferedAmount
        }

        canSend = (ignoreBuffer, ignoreAuthentication, ignoreState) => {
            return (ignoreAuthentication|| this.key===false || this.key!==true) && (ignoreBuffer || this.bufferedAmount() < window.MAX_BUFFER_SIZE) && (ignoreState || this.rawWS.readyState === this.rawWS.OPEN)
        }

        initialise = async(CSRF) => {
            this.rawWS.addEventListener("open", () => {
                if (this.key === true) {
                    this.generateClientKey().then((clientPublicKey) => {
                        this.sendWS(JSON.stringify({REASON: WS_DATA_REASONS.OUT.VERIFY_CSRF, CSRF: CSRF, REQUEST_ENCRYPTION: true, "CLIENT-KEY": {PubB64: btoa(String.fromCharCode(...new Uint8Array(clientPublicKey)))}}))
                    })
                } else {
                    this.sendWS(JSON.stringify({REASON: WS_DATA_REASONS.OUT.VERIFY_CSRF, CSRF: CSRF, REQUEST_ENCRYPTION: false}))
                }
            })
            this.rawWS.addEventListener("close", () => {
                this.handler.handleClosedWS(this)
            })
            this.rawWS.addEventListener("message", (event) => {
                this.processReceived(event.data)
            })
        }

        sendWS = async (string) => {
            if (this.key === false || this.key === true) {
                this.rawWS.send(string)
            } else {
                this.rawWS.send(JSON.stringify(await this.encrypt(string)))
            }
        }

        processReceived = async(data) => {
            let receivedDict = await JSON.parse(data)
            if (this.key !== false && this.key !== true) receivedDict = await JSON.parse(await this.decrypt(receivedDict["eB64"], receivedDict["ivB64"], receivedDict["tagB64"]))
            let reason = receivedDict["REASON"]

            if (reason === WS_DATA_REASONS.IN.CSRF_ACCEPTED) {
                if (this.key === true) await this.generateSharedKey(receivedDict["SERVER-KEY"])
                await this.sendWS(JSON.stringify({REASON: WS_DATA_REASONS.OUT.READY}))
                if (this.key !== true || this.key === false) await this.handler.handleAcceptedWS(this)
            } else if (this.key !== true) {
                if (reason === WS_DATA_REASONS.IN.FUTURE_CSRF) {
                    this.futureCSRF = receivedDict["CSRF"]
                } else {
                    this.handler.onMessageReceived(receivedDict)
                }
            } else {
                new Promise((resolve) => {
                    setTimeout(async () => {
                        const r = await this.processReceived(data)
                        resolve(r);
                    }, 100);
                });
            }
        }

        async generateClientKey() {
            this.clientKeyPair = await window.crypto.subtle.generateKey(
                {
                    name: "ECDH",
                    namedCurve: "P-256",
                },
                true,
                ["deriveKey", "deriveBits"]
            )
            return await window.crypto.subtle.exportKey(
                "spki",
                this.clientKeyPair.publicKey
            )
        }

        async generateSharedKey(serverKey) {
            const serverPublicKey = await window.crypto.subtle.importKey(
                "spki",
                urlSafeBase64Decoded(serverKey["PubB64"]),
                {name: "ECDH", namedCurve: "P-256"},
                false,
                []
            )
            const sharedSecret = await window.crypto.subtle.deriveBits(
                {
                    name: "ECDH",
                    public: serverPublicKey,
                },
                this.clientKeyPair.privateKey,
                256
            )
            const hkdfKey = await crypto.subtle.importKey(
                "raw",
                sharedSecret,
                "HKDF",
                false,
                ["deriveKey"]
            )
            this.key = await crypto.subtle.deriveKey(
                {
                    name: "HKDF",
                    hash: "SHA-256",
                    salt: urlSafeBase64Decoded(serverKey["SaltB64"]),
                    info: urlSafeBase64Decoded(serverKey["InfoB64"]),
                },
                hkdfKey,
                {name: "AES-GCM", length: 256},
                false,
                ["encrypt", "decrypt"]
            )
        }

        async decrypt(ciphertextB64, ivB64, tagB64) {
            const ciphertext = urlSafeBase64Decoded(ciphertextB64)
            const iv = urlSafeBase64Decoded(ivB64)
            const tag = urlSafeBase64Decoded(tagB64)
            const combinedBuffer = new Uint8Array(ciphertext.length + tag.length)
            combinedBuffer.set(ciphertext)
            combinedBuffer.set(tag, ciphertext.length)
            const decryptedBuffer = await crypto.subtle.decrypt(
                {
                    name: "AES-GCM",
                    iv: iv,
                },
                this.key,
                combinedBuffer
            )
            const decoder = new TextDecoder()
            return decoder.decode(decryptedBuffer)
        }

        async encrypt(plaintext) {
            const iv = crypto.getRandomValues(new Uint8Array(12))
            const encoder = new TextEncoder()
            const ciphertextBuffer = await crypto.subtle.encrypt(
                {
                    name: "AES-GCM",
                    iv: iv,
                },
                this.key,
                encoder.encode(plaintext)
            )
            const tagLength = 16
            const ciphertext = new Uint8Array(ciphertextBuffer)
            const tag = ciphertext.slice(ciphertext.length - tagLength)
            const actualCiphertext = ciphertext.slice(0, ciphertext.length - tagLength)
            return {
                eB64: urlSafeBase64Encoded(actualCiphertext),
                ivB64: urlSafeBase64Encoded(iv),
                tagB64: urlSafeBase64Encoded(tag),
            }
        }
    }
}

window.CHUNK_SIZE = 1024*1024*10;
window.MAX_BUFFER_SIZE = 1024*1024*5;
window.DELAY_TIME = 500

fetch('/?RECEIVE_NEW_L2_COOKIE', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: getDeviceFingerprint(),
    credentials: "include",
}).then((response)=>{
    response.json().then((parsed)=>{
        window.ConnmanagerWS = new WSConnectionManager(parsed[WS_PURPOSES.RESPONSIVE], parsed[WS_PURPOSES.LARGE])
    })
});


function sendCustomMessage(data, isLargeData) {
    let purpose = WS_PURPOSES.RESPONSIVE
    if (isLargeData) purpose = WS_PURPOSES.LARGE
    window.ConnmanagerWS.sendInQueue(JSON.stringify({T: WS_DATA_TYPES.CUSTOM, D: data}), purpose).then()
}


