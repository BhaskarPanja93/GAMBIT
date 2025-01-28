ConnmanagerWS.addEventListener("message", function (data) {WSListener(data);}, false);


const CUSTOM_MESSAGE_TASKS = {
    FRIEND_REMOVED: 'FRIEND_REMOVED',
    FRIEND_ADDED: 'FRIEND_ADDED',
    PAGE_CHANGED: 'PAGE_CHANGED',
    ADDED_PARTY_MEMBER: 'ADDED_PARTY_MEMBER',
    REMOVED_PARTY_MEMBER: 'REMOVED_PARTY_MEMBER',
    KICKED_FROM_PARTY: 'KICKED_FROM_PARTY',
    CHAT: 'CHAT',
}


function WSListener(data) {
    console.log(data)
    if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.FRIEND_REMOVED) removeFriend(data["CONNECTION_ID"])
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.FRIEND_ADDED) addFriend(data["CONNECTION_ID"], data["FRIEND_DATA"])
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.ADDED_PARTY_MEMBER) addedPartyMember(data)
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.PAGE_CHANGED) window["currentPage"] = data["PAGE"]
}
function waitForElementCreation(selector, callback) {
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



