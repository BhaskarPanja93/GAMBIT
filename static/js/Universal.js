
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// MOUSE TRACKING ANIMATION



document.addEventListener("mousemove", function (e) {
    const particle = document.createElement('div');
    particle.classList.add('mouse-trail-particle');
    particle.style.left = `${Math.min(Math.max(e.pageX - 5, 0), window.innerWidth - 10)}px`;
    particle.style.top = `${Math.min(Math.max(e.pageY - 5, 0), window.innerHeight - 10)}px`;
    document.getElementById("particles-animation").appendChild(particle);
    setTimeout(() => {
        particle.remove();
    }, 100);
})




////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// FRIEND LIST ACTIONS




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

function inviteFriend(connectionID) {

}

function joinFriend(connectionID) {

}

function contractFriendsPage() {
    Array.prototype.filter.call(
        document.getElementsByClassName("friend-element"),
        (friendElement) => {
            friendElement.classList.remove("w-48")
            friendElement.classList.add("w-16")
        },
    );
    Array.prototype.filter.call(
        document.getElementsByClassName("friend-details"),
        (friendDetail) => {
            friendDetail.classList.add("hidden")
        },
    );
}

function expandFriendPage() {
    Array.prototype.filter.call(
        document.getElementsByClassName("friend-element"),
        (friendElement) => {
            friendElement.classList.add("w-48")
            friendElement.classList.remove("w-16")
        },
    );
    Array.prototype.filter.call(
        document.getElementsByClassName("friend-details"),
        (friendDetail) => {
            friendDetail.classList.remove("hidden")
        },
    );
}


const friendsPageRenderObserver = new MutationObserver(() => {
    if (document.getElementById("friends-page") !== null) {
        friendsPageRenderObserver.disconnect();
        document.getElementById("friends-page").onmouseleave = contractFriendsPage
        document.getElementById("friends-page").onmouseenter = expandFriendPage
    }
})
friendsPageRenderObserver.observe(document.body, {
    childList: true,
    subtree: true
})





////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// MUSIC TRAY ACTIONS



function enableMusicService() {
    fetch("/music-categories").then((response) => {
        response.json().then((streams) => {
            document.getElementById('music-tray-toggle-btn').addEventListener('click', toggleMusicTray)
            document.getElementById('music-pp-btn').addEventListener('click', () => {
                if (window.lastMusicCategory === null) {
                    openMusicTray()
                } else {
                    toggleMusicMute()
                }
            });
            knownStreams = streams
            knownStreams.forEach((cat)=>{
                let _split = cat.split("-")
                let mainCat = _split[0]
                let subCat = _split[1]
                if (document.getElementById(mainCat + "-music-category") === null) {
                    let mainCategoryDiv = document.createElement('div');
                    let subCategoryDiv = document.createElement('div');
                    mainCategoryDiv.className = "music-tray-category-grp py-1"
                    mainCategoryDiv.id = mainCat + "-music-category";
                    mainCategoryDiv.innerHTML = mainCat;
                    mainCategoryDiv.style.color = "rgba(255, 255, 255, 0.4)"
                    subCategoryDiv.className = "music-tray-sub-category-grp"
                    subCategoryDiv.id = mainCat + "-music-subcategory"
                    mainCategoryDiv.append(subCategoryDiv);
                    document.getElementById('music-tray-categories').appendChild(mainCategoryDiv);
                }
                let subCatButton = document.createElement('button');
                subCatButton.className = "music-tray-button-global music-tray-sub-category-button"
                subCatButton.id = cat
                subCatButton.innerHTML = subCat
                subCatButton.style.color = "rgba(255, 255, 255, 0.4)"
                subCatButton.onclick = () => {playMusicCategory(cat, mainCat).then()}
                document.getElementById(mainCat + "-music-subcategory").append(subCatButton);
            })
        })
    })
}

const musicButtonRenderObserver = new MutationObserver(() => {
    if (document.getElementById('music-player') !== null && document.getElementById('music-player') !== null) {
        musicButtonRenderObserver.disconnect();
        enableMusicService()
    }
});
musicButtonRenderObserver.observe(document.body, {
    childList: true,
    subtree: true
})


let knownStreams = []
window.currentlyPlaying = false
window.lastMusicCategory = null
window.lastMusicMainCategory = null
window.lastMusicSubCategory = null
async function playMusicCategory(category, mainCategory) {
    if (!knownStreams.includes(category)) return null
    if (window.lastMusicCategory === null || category!==window.lastMusicCategory) {
        muteMusic()
        if (window.lastMusicCategory !== null) document.getElementById(window.lastMusicCategory).style.color = "rgba(255, 255, 255, 0.2)";
        if (window.lastMusicMainCategory !== null) document.getElementById(window.lastMusicMainCategory+"-music-category").style.color = "rgba(255, 255, 255, 0.2)";
        document.getElementById(category).style.color = "rgba(255, 255, 255, 1)";
        document.getElementById(mainCategory+"-music-category").style.color = "rgba(255, 255, 255, 1)";
        window.lastMusicCategory = category
        window.lastMusicMainCategory = mainCategory
        document.getElementById('music-player').children[0].src = "/music/" + category
        await document.getElementById('music-player').load()
        unmuteMusic()
        await document.getElementById('music-player').play()
    }
}


function unmuteMusic() {
    if (window.lastMusicCategory === null || document.getElementById('music-player').muted === true) {
        document.getElementById('music-player').volume = 0.08;
        document.getElementById('music-player').muted = false
        document.getElementById('music-pp-btn').querySelector('img').src = '/cd?type=image&name=music-tray-pause.png';
        document.getElementById('music-pp-btn').querySelector('img').alt = 'Pause';
        return true
    }
    return null
}


function muteMusic() {
    if (document.getElementById('music-player').muted === false) {
        document.getElementById('music-player').muted = true
        document.getElementById('music-pp-btn').querySelector('img').src = '/cd?type=image&name=music-tray-resume.png';
        document.getElementById('music-pp-btn').querySelector('img').alt = 'Play';
        return false
    }
    return null
}


function toggleMusicMute() {
    if (!(unmuteMusic() === true)) muteMusic()
}


function openMusicTray() {
    if (document.getElementById('music-tray').classList.contains('collapsed')) {
        document.getElementById('music-tray').classList.toggle('collapsed');
        document.getElementById('music-tray-toggle-btn').querySelector('img').src = '/cd?type=image&name=music-tray-down.png';
        return true
    }
    return null
}


function closeMusicTray() {
    if (!document.getElementById('music-tray').classList.contains('collapsed')) {
        document.getElementById('music-tray').classList.toggle('collapsed');
        document.getElementById('music-tray-toggle-btn').querySelector('img').src = '/cd?type=image&name=music-tray-up.png';
        return false
    }
    return null
}


function toggleMusicTray() {
    if (!(openMusicTray() === true)) closeMusicTray()
}



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// CUSTOM MESSAGE ACTIONS




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