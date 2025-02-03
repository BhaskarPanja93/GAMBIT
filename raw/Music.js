const musicTray = document.getElementById('music-tray');
const musicTrayCategories = document.getElementById('music-tray-categories');
const musicTrayToggleButton = document.getElementById('music-tray-toggle-btn');
const musicTrayPPButton = document.getElementById('music-pp-btn');
const musicTrayPPIcon = musicTrayPPButton.querySelector('img');
const musicTrayToggleIcon = musicTrayToggleButton.querySelector('img');
const musicPlayer = document.getElementById('music-player');


let knownStreams = []
musicPlayer.muted = true
window.lastMusicCategory = null
window.currentlyPlaying = false


fetch(baseURI+"/music-categories").then((response) => {
    response.json().then((streams) => {
        knownStreams = streams
        knownStreams.forEach((cat)=>{
            let _split = cat.split("-")
            let mainCat = _split[0]
            let subCat = _split[1]
            if (document.getElementById(mainCat + "-music-category") === null) {
                let mainCategoryDiv = document.createElement('div');
                mainCategoryDiv.className = "music-tray-category-grp"
                let mainCatButton = document.createElement('button');
                mainCatButton.className = "music-tray-button-global"
                mainCatButton.innerHTML = mainCat;
                mainCategoryDiv.append(mainCatButton);
                musicTrayCategories.appendChild(mainCategoryDiv);

                let subCategoryDiv = document.createElement('div');
                subCategoryDiv.className = "music-tray-sub-category-grp"
                subCategoryDiv.id = mainCat + "-music-category"
                mainCategoryDiv.append(subCategoryDiv);
            }
            let subCatButton = document.createElement('button');
            subCatButton.className = "music-tray-button-global music-tray-sub-category-button"
            subCatButton.id = cat
            subCatButton.innerText = subCat
            subCatButton.onclick = () => {playMusicCategory(cat).then()}
            document.getElementById(mainCat + "-music-category").append(subCatButton);
        })
    })
})


async function playMusicCategory(category) {
    if (!knownStreams.includes(category)) return null
    if (window.lastMusicCategory === null || category!==window.lastMusicCategory) {
        muteMusic()
        if (window.lastMusicCategory !== null) document.getElementById(window.lastMusicCategory).style.color = "rgba(255, 255, 255, 0.5)";
        document.getElementById(category).style.color = "rgba(255, 255, 255, 1)";
        window.lastMusicCategory = category
        musicPlayer.children[0].src = baseURI + "/music/" + category
        await musicPlayer.load()
        unmuteMusic()
        await musicPlayer.play()
    }
}


function unmuteMusic() {
    if (window.lastMusicCategory === null || musicPlayer.muted === true) {
        musicPlayer.volume = 0.01;
        musicPlayer.muted = false
        musicTrayPPIcon.src = baseURI+'/cd?type=image&name=music-tray-pause.png';
        musicTrayPPIcon.alt = 'Pause';
        return true
    }
    return null
}


function muteMusic() {
    if (musicPlayer.muted === false) {
        musicPlayer.muted = true
        musicTrayPPIcon.src = baseURI+'/cd?type=image&name=music-tray-resume.png';
        musicTrayPPIcon.alt = 'Play';
        return false
    }
    return null
}


function toggleMusicMute() {
    if (!(unmuteMusic() === true)) muteMusic()
}


function openMusicTray() {
    if (musicTray.classList.contains('collapsed')) {
        musicTray.classList.toggle('collapsed');
        musicTrayToggleIcon.src = baseURI+'/cd?type=image&name=music-tray-down.png';
        return true
    }
    return null
}


function closeMusicTray() {
    if (!musicTray.classList.contains('collapsed')) {
        musicTray.classList.toggle('collapsed');
        musicTrayToggleIcon.src = baseURI+'/cd?type=image&name=music-tray-up.png';
        return false
    }
    return null
}


function toggleMusicTray() {
    if (!(openMusicTray() === true)) closeMusicTray()
}


musicTrayToggleButton.addEventListener('click', toggleMusicTray)
musicTrayPPButton.addEventListener('click', () => {
    if (window.lastMusicCategory === null) {
        openMusicTray()
    } else {
        toggleMusicMute()
    }
});
