const friendsPage = document.getElementById("friends-page");
const friendElements = document.getElementsByClassName("friend-element")
const friendDetails = document.getElementsByClassName("friend-details")


const FRIEND_STATES = {
    AVAILABLE: "Available",
    IN_GAME: "In Game",
    OFFLINE: "Offline",
}


function createInviteButton(connectionID) {
    deleteInviteButton(connectionID)
    let button = document.createElement("button")
    button.className = "px-2 py-1 text-xs bg-blue-500 hover:bg-blue-600 text-white rounded friend-action-invite"
    document.getElementById(connectionID).getElementsByClassName("friend-action-invite")[0].innerHTML = state
}


function deleteInviteButton(connectionID) {
    let inviteButton = document.getElementById(connectionID).getElementsByClassName("friend-action-invite")
    if (inviteButton.length === 0) document.getElementById(connectionID).getElementsByClassName("friend-action-invite")[0].remove()
}


function changeFriendState(connectionID, state) {
    let friendDiv = document.getElementById(connectionID)
    if (state === FRIEND_STATES.AVAILABLE) createInviteButton()
    else deleteInviteButton(connectionID)
    friendDiv.getElementsByClassName("friend-state")[0].innerHTML = state
}


function removeFriend(connectionID) {
    let friendDiv = document.getElementById(connectionID)
    if (friendDiv !== null) {
        friendDiv.remove()
    }
}


function addFriend(connectionID, friendData) {
    // TODO:
}


friendsPage.onmouseleave = function() {
    Array.prototype.filter.call(
        friendElements,
        (friendElement) => {
            friendElement.classList.remove("w-60")
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


friendsPage.onmouseenter = function() {
    Array.prototype.filter.call(
        friendElements,
        (friendElement) => {
            friendElement.classList.add("w-60")
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

