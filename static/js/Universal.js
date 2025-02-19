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
    TOGGLE_SOCIALS: 'TOGGLE_SOCIALS',
    PARTY_JOIN_REQUEST: 'PARTY_JOIN_REQUEST',
    PARTY_INVITE: 'PARTY_INVITE',
    FRIEND_REQUEST: 'FRIEND_REQUEST',
    DELETE_INTERACTION: 'DELETE_INTERACTION',
}


function WSListener(data) {
    console.log(data)
    if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.REFRESH) location.reload()
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.FRIEND_REMOVED) waitForElementPresence("#script-friends", ()=>friendRemoved(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.FRIEND_ADDED) waitForElementPresence("#script-friends", ()=>friendAdded(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.ADDED_PARTY_MEMBER) waitForElementPresence("#script-lobby", ()=>addedPartyMember(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.REMOVED_PARTY_MEMBER) waitForElementPresence("#script-lobby", ()=>removedPartyMember(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.DECREMENT_PARTY_MEMBER_INDEX) waitForElementPresence("#script-lobby", ()=>decrementPartyMemberIndex(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.NEW_LEADER) waitForElementPresence("#script-lobby", ()=>newLeader(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.PAGE_CHANGED) window["currentPage"] = data["PAGE"]
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.CHAT) waitForElementPresence("#script-chat", ()=>receiveText(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.TOGGLE_SOCIALS) waitForElementPresence("#script-friends", ()=>toggleSocials(data["DISPLAY"]))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.PARTY_JOIN_REQUEST) waitForElementPresence("#script-friends", ()=>receivedPartyJoin(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.PARTY_INVITE) waitForElementPresence("#script-friends", ()=>receivedPartyInvite(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.FRIEND_REQUEST) waitForElementPresence("#script-friends", ()=>receivedFriendRequest(data))
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.DELETE_INTERACTION) waitForElementPresence("#script-friends", ()=>deleteInteraction(data["INTERACTION"]))
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



function firstLetterCapitalised(string) {
    if (!string || string.length === 0) return string
    else if (string.length === 1) return string.toUpperCase()
    else return string[0].toUpperCase() + string.substring(1).toLowerCase()
}