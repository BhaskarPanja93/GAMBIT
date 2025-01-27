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
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.PAGE_CHANGED) window["currentPage"] = data["PAGE"]
    else if (data["MESSAGE"] === CUSTOM_MESSAGE_TASKS.ADDED_PARTY_MEMBER) {
        const observer = new MutationObserver(() => {
            const playerElement = document.getElementById(`player-${data["INDEX"]}`);
            if (playerElement) {
                observer.disconnect();
                addedPartyMember(data);
            }
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
}


function addedPartyMember(playerData) {
    let playerPFP = document.createElement("img");
    playerPFP.src = playerData["PFP"]
    playerPFP.alt = playerData["USERNAME"]
    playerPFP.className = "h-10 w-20 sm:h-10 sm:w-20 md:h-36 md:w-36 lg:h-32 lg:w-32 mx-auto"
    let playerNameHeading = document.createElement("h3");
    playerNameHeading.className = "text-xs sm:text-xs md:text-xl lg:text-lg pt-10 sm:pt-10 md:pt-20 lg:pt-20 font-semibold mt-2"
    playerNameHeading.innerText = playerData["USERNAME"]
    let playerLevelParagraph = document.createElement("p");
    playerLevelParagraph.className = "text-gray-400 text-sm"
    playerLevelParagraph.innerText = playerData["LEVEL"]
    let rankImage = document.createElement("img");
    rankImage.src = playerData["RANK"]
    rankImage.className = "mx-auto h-10 w-10 mt-10 sm:h-10 sm:w-10 sm:mt-10 md:h-24 md:w-24 md:mt-20 lg:h-24 lg:w-24 lg:mt-20"
    document.getElementById(`player-${playerData["INDEX"]}`).appendChild(playerPFP)
    document.getElementById(`player-${playerData["INDEX"]}`).appendChild(playerNameHeading)
    document.getElementById(`player-${playerData["INDEX"]}`).appendChild(playerLevelParagraph)
    document.getElementById(`player-${playerData["INDEX"]}`).appendChild(rankImage)
}


ConnmanagerWS.addEventListener("message", function (data) {WSListener(data);}, false);