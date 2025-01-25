const CUSTOM_MESSAGE_TASKS = {
    FRIEND_REMOVED: 'FRIEND_REMOVED',
    FRIEND_ADDED: 'FRIEND_ADDED',
    PARTY_INVITE: 'PARTY_INVITE',
    PARTY_REQUEST: 'PARTY_REQUEST',
    PAGE_CHANGED: 'PAGE_CHANGED',
}

function WSListener(data) {
    console.log(data)
    if (data["TASK"] === CUSTOM_MESSAGE_TASKS.FRIEND_REMOVED) removeFriend(data["CONNECTION_ID"])
    else if (data["TASK"] === CUSTOM_MESSAGE_TASKS.FRIEND_ADDED) addFriend(data["CONNECTION_ID"], data["FRIEND_DATA"])
    else if (data["TASK"] === CUSTOM_MESSAGE_TASKS.PAGE_CHANGED) window["currentPage"] = data["PAGE"]

}

ConnmanagerWS.addEventListener("message", function (data) {WSListener(data);}, false);