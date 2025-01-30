const MESSAGE_CATEGORY = {
    PARTY: "Party",
    TEAM: "Team",
    PLAYER: "Player",
    YOU: "You",
    SYSTEM: "System",
}

function openChatHistory() {
    waitForElementPresence("#chat-history", (chatHistory)=>{
        chatHistory.style.display = "block"
    })
    if (typeof closeMusicTray !== "undefined") closeMusicTray()
}

function closeChatHistory() {
    waitForElementPresence("#chat-history", (chatHistory)=>{
        chatHistory.style.display = ""
    })
}

function receiveText(data) {
    console.log(data)
    let backgroundDiv, senderSpan, textPara
    if (data["CATEGORY"] === MESSAGE_CATEGORY.PARTY) {
        backgroundDiv = document.createElement("div")
        backgroundDiv.className = "flex items-start space-x-1 text-gray-700 rounded-lg py-1 px-2"
        senderSpan = document.createElement("span")
        senderSpan.className = "text-sm font-semibold text-purple-500"
        textPara = document.createElement("p")
        textPara.className = "text-sm text-gray-300"
    } else if (data["CATEGORY"] === MESSAGE_CATEGORY.TEAM) {
        backgroundDiv = document.createElement("div")
        backgroundDiv.className = "flex items-start space-x-1 text-gray-700 rounded-lg py-1 px-2"
        senderSpan = document.createElement("span")
        senderSpan.className = "text-sm font-semibold text-green-500"
        textPara = document.createElement("p")
        textPara.className = "text-sm text-gray-300"
    } else if (data["CATEGORY"] === MESSAGE_CATEGORY.PLAYER) {
        backgroundDiv = document.createElement("div")
        backgroundDiv.className = "flex items-start space-x-1 text-gray-700 rounded-lg py-1 px-2"
        senderSpan = document.createElement("span")
        senderSpan.className = "text-sm font-semibold text-blue-500"
        textPara = document.createElement("p")
        textPara.className = "text-sm text-gray-300"
    } else if (data["CATEGORY"] === MESSAGE_CATEGORY.YOU) {
        backgroundDiv = document.createElement("div")
        backgroundDiv.className = "flex items-start space-x-1 text-gray-700 rounded-lg py-1 px-2"
        senderSpan = document.createElement("span")
        senderSpan.className = "text-sm font-semibold text-yellow-500"
        textPara = document.createElement("p")
        textPara.className = "text-sm text-gray-300"
    } else if (data["CATEGORY"] === MESSAGE_CATEGORY.SYSTEM) {
        backgroundDiv = document.createElement("div")
        backgroundDiv.className = "flex items-start space-x-1 text-gray-700 rounded-lg py-1 px-2 bg-white/10"
        senderSpan = document.createElement("span")
        senderSpan.className = "text-sm font-bold color-change"
        textPara = document.createElement("p")
        textPara.className = "text-sm font-semibold italic color-change"
    }
    senderSpan.innerText = `[${data["CATEGORY"]}] ${data["SENDER"]}`
    textPara.innerText = data["TEXT"]
    backgroundDiv.append(senderSpan)
    backgroundDiv.append(textPara)
    waitForElementPresence("#chat-history", (historyDiv) => {
        historyDiv.append(backgroundDiv)
        historyDiv.scrollTop = historyDiv.scrollHeight
    })
}

function sendTriggered() {
    waitForElementPresence("#chat-input-text", (input)=>{
        if (input.value !== "") {
            sendCustomMessage({PURPOSE: "CHAT", "CATEGORY": selectedChatCategory, "RECEIVER": selectedReceiver, "TEXT": input.value})
            receiveText({"CATEGORY": selectedChatCategory, "SENDER": MESSAGE_CATEGORY.YOU, "TEXT": input.value})
            input.value = ""
        }
    })
}

function changeChatCategory(category) {
    let probablyUsername = category
    category = category.toUpperCase()
    if (category===MESSAGE_CATEGORY.TEAM.toUpperCase()) {
        selectedChatCategory = category
        waitForElementPresence("#chat-sending-to", (element)=>{
            element.innerText = `[Team]:`
        })
        return true
    } else if (category===MESSAGE_CATEGORY.PARTY.toUpperCase()) {
        selectedChatCategory = category
        waitForElementPresence("#chat-sending-to", (element)=>{
            element.innerText = `[Party]:`
        })
        return true
    } else if (allFriendUsernames.has(probablyUsername)) {
        selectedChatCategory = MESSAGE_CATEGORY.PLAYER
        selectedReceiver = probablyUsername
        waitForElementPresence("#chat-sending-to", (element)=>{
            element.innerText = `[${probablyUsername}]:`
        })
        return true
    }
    return false
}


waitForElementPresence("#chat-input-text", (input)=>{
    input.addEventListener("input", function() {
        input.value = input.value.trim()
        let content = input.value
        if (content[0] === "/") {
            if (changeChatCategory(content.slice(1)) === true) {
                input.value = ""
            }
        }
    })
    input.addEventListener("focusin", function() {
        chatFocusCount++
        openChatHistory()
    })
    input.addEventListener("focusout", function() {
        chatFocusCount--
        if (chatFocusCount===0) closeChatHistory()
    })
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault()
            sendTriggered()
        }
    })
})

waitForElementPresence("#chat-send-btn", (sendButton)=>{
    sendButton.addEventListener("click", function() {
        sendTriggered()
    })
})

waitForElementPresence("#chat-holder", (chatHolder)=>{
    chatHolder.addEventListener("mouseenter", function() {
        openChatHistory()
        chatFocusCount++
    })
    chatHolder.addEventListener("mouseleave", function() {
        chatFocusCount--
        if (chatFocusCount===0) closeChatHistory()
    })
})

let chatFocusCount = 0
let selectedChatCategory = ""
let selectedReceiver = ""
changeChatCategory(MESSAGE_CATEGORY.PARTY)