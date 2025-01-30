ConnmanagerWS.addEventListener("message", (data) => WSListener(data), false);


const CUSTOM_MESSAGE_TASKS = {
    REFRESH: "REFRESH",
    FRIEND_REMOVED: 'FRIEND_REMOVED',
    FRIEND_ADDED: 'FRIEND_ADDED',
    PAGE_CHANGED: 'PAGE_CHANGED',
    ADDED_PARTY_MEMBER: 'ADDED_PARTY_MEMBER',
    REMOVED_PARTY_MEMBER: 'REMOVED_PARTY_MEMBER',
    DECREMENT_PARTY_MEMBER_INDEX: 'DECREMENT_PARTY_MEMBER_INDEX',
    NEW_LEADER: 'NEW_LEADER',
    KICKED_FROM_PARTY: 'KICKED_FROM_PARTY',
    CHAT: 'CHAT',
    PARTY_CODE: 'PARTY_CODE',
}


function WSListener(data) {
    console.log(data)
    if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.REFRESH) location.reload()
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.FRIEND_REMOVED) removeFriend(data["CONNECTION_ID"])
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.FRIEND_ADDED) addFriend(data["FRIEND_DATA"])
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.ADDED_PARTY_MEMBER) addedPartyMember(data)
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.REMOVED_PARTY_MEMBER) removedPartyMember(data)
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.DECREMENT_PARTY_MEMBER_INDEX) decrementPartyMemberIndex(data)
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.NEW_LEADER) newLeader(data)
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.PARTY_CODE) receivedPartyCode(data)
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.PAGE_CHANGED) window["currentPage"] = data["PAGE"]
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.CHAT) receiveText(data)
}


function waitForElementPresence(selector, callback) {
    const element = document.querySelector(selector)
    if (element) return callback(element)
    const observer = new MutationObserver((mutationsList, observer) => {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                const element = document.querySelector(selector)
                if (element) {
                    observer.disconnect()
                    return callback(element)
                }
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}

waitForElementPresence("#logout-button", (button)=>{
    console.log("BUTTONNNNN")
    button.onclick = () => sendCustomMessage({PURPOSE: "LOGOUT"})
})

