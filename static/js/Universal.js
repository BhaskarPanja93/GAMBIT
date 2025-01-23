const CUSTOM_MESSAGE_TASKS = {
    FRIEND_REMOVED: 'FRIEND_REMOVED',
    FRIEND_ADDED: 'FRIEND_ADDED',
    PARTY_INVITE: 'PARTY_INVITE',
    PARTY_REQUEST: 'PARTY_REQUEST',
}

function WSListener(data) {
    if (data["TASK"] === CUSTOM_MESSAGE_TASKS.FRIEND_REMOVED) {
        removeFriend(data["CONNECTION_ID"])
    }

}

ConnmanagerWS.addEventListener("message", function (data) {WSListener(data);}, false);