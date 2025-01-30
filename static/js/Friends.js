const friendElements = document.getElementsByClassName("friend-element")
const friendDetails = document.getElementsByClassName("friend-details")
const allFriendUsernames = new Set()

const FRIEND_STATES = {
    AVAILABLE: "Available",
    IN_GAME: "In Game",
    OFFLINE: "Offline",
}


function createInviteButton(username) {
    deleteInviteButton(username)
    let button = document.createElement("button")
    button.className = "px-2 py-1 text-xs bg-blue-500 hover:bg-blue-600 text-white rounded friend-action-invite"
    document.getElementById(`connection-${username}`).getElementsByClassName("friend-action-invite")[0].innerHTML = state
}


function deleteInviteButton(username) {
    let inviteButton = document.getElementById(`connection-${username}`).getElementsByClassName("friend-action-invite")
    if (inviteButton.length === 0) document.getElementById(`connection-${username}`).getElementsByClassName("friend-action-invite")[0].remove()
}


function changeFriendState(username, state) {
    let friendDiv = document.getElementById(`connection-${username}`)
    if (state === FRIEND_STATES.AVAILABLE) createInviteButton()
    else deleteInviteButton({username})
    friendDiv.getElementsByClassName("friend-state")[0].innerHTML = state
}


function removeFriend(username) {
    allFriendUsernames.delete(`connection-${username}`)
    let friendDiv = document.getElementById(`connection-${username}`)
    if (friendDiv !== null) {
        friendDiv.remove()
    }
}


function addFriend(friendData) {
    console.log(friendData)
    allFriendUsernames.add(friendData["USERNAME"])
    let friendElement = document.createElement("div")
    friendElement.id = `connection-${friendData["USERNAME"]}`
    friendElement.className = "flex items-center space-x-2 hover:bg-gray-600 p-2 rounded-lg w-16 relative overflow-visible friend-element"
    let group = document.createElement("div")
    group.className = "relative group flex items-center space-x-2"
    let PFP = document.createElement("img")
    PFP.src = friendData["PFP"]
    PFP.className = "h-10 w-10"
    group.appendChild(PFP)
    let visiblePart = document.createElement("div")
    visiblePart.className = "flex flex-col text-sm friend-details"
    let usernameDIV = document.createElement("div")
    usernameDIV.className = "flex items-center space-x-2"
    usernameDIV.innerText = friendData["USERNAME"]
    let stateDiv = document.createElement("div")
    stateDiv.className = "text-green-400 friend-state"
    stateDiv.innerText = friendData["STATE"]
    visiblePart.append(usernameDIV)
    visiblePart.append(stateDiv)
    group.appendChild(visiblePart)
    let hoverPart = document.createElement("div")
    hoverPart.className = "gap-1 flex flex-col absolute top-1/2 left-full transform -translate-y-1/2 translate-x-2 p-2 rounded shadow-md opacity-0 transition-opacity duration-300 group-hover:opacity-100 whitespace-nowrap"
    let inviteButton = document.createElement("button")
    inviteButton.className = "bg-gray-800 text-white border border-white/30 text-sm rounded px-2 py-1 friend-action-invite friend-sub-category-button"
    inviteButton.innerText = "INVITE"
    let joinButton = document.createElement("button")
    joinButton.className = "bg-gray-800 text-white border border-white/30 text-sm rounded px-2 py-1 friend-action-request friend-sub-category-button"
    joinButton.innerText = "JOIN"
    let messageButton = document.createElement("button")
    messageButton.className = "bg-gray-800 text-white border border-white/30 text-sm rounded px-2 py-1 friend-action-request friend-sub-category-button"
    messageButton.innerText = "MESSAGE"
    hoverPart.append(inviteButton)
    hoverPart.append(joinButton)
    hoverPart.append(messageButton)
    group.appendChild(hoverPart)
    friendElement.appendChild(group)
    waitForElementPresence("#online-friend-list", (div)=> {
        if (div.classList.contains("expanded") === false) visiblePart.classList.add("hidden")
        div.append(friendElement)
    })
}


function inviteFriend(username) {

}


function joinFriend(username) {

}


waitForElementPresence("#friends-page", (friendsPage)=> {
    friendsPage.onmouseleave = function() {
        Array.prototype.filter.call(
            friendElements,
            (friendElement) => {
                friendElement.classList.remove("w-48")
                friendElement.parentElement.classList.remove("expanded")
                friendElement.classList.add("w-16")
            },
        );
        Array.prototype.filter.call(
            friendDetails,
            (friendDetail) => {
                friendDetail.classList.add("hidden")
            },
        );
    }
    friendsPage.onmouseenter = function () {
        Array.prototype.filter.call(
            friendElements,
            (friendElement) => {
                friendElement.classList.add("w-48")
                friendElement.parentElement.classList.add("expanded")
                friendElement.classList.remove("w-16")
            },
        );
        Array.prototype.filter.call(
            friendDetails,
            (friendDetail) => {
                friendDetail.classList.remove("hidden")
            },
        );
    }
})