const musicTray = document.getElementById('music-tray');
const musicTrayCategories = document.getElementById('music-tray-categories');
const musicTrayToggleButton = document.getElementById('music-tray-toggle-btn');
const musicTrayPPButton = document.getElementById('music-pp-btn');
const musicTrayPPIcon = musicTrayPPButton.querySelector('img');
const musicTrayToggleIcon = musicTrayToggleButton.querySelector('img');
const musicPlayer = document.getElementById('music-player');


let knownStreams = []
musicPlayer.muted = true
window.currentlyPlaying = false


fetch("/music-categories").then((response) => {
    response.json().then((streams) => {
        knownStreams = streams
        knownStreams.forEach((cat)=>{
            let _split = cat.split("-")
            let mainCat = _split[0]
            let subCat = _split[1]
            if (document.getElementById(mainCat + "-music-category") === null) {
                let mainCategoryDiv = document.createElement('div');
                let subCategoryDiv = document.createElement('div');
                let mainCatButton = document.createElement('button');
                mainCategoryDiv.className = "music-tray-category-grp py-1"
                mainCategoryDiv.id = mainCat + "-music-category";
                mainCategoryDiv.innerHTML = mainCat;
                mainCategoryDiv.style.color = "rgba(255, 255, 255, 0.2)"
                subCategoryDiv.className = "music-tray-sub-category-grp"
                subCategoryDiv.id = mainCat + "-music-subcategory"
                mainCatButton.className = "music-tray-button-global"
                mainCategoryDiv.append(mainCatButton);
                mainCategoryDiv.append(subCategoryDiv);
                musicTrayCategories.appendChild(mainCategoryDiv);
            }
            let subCatButton = document.createElement('button');
            subCatButton.className = "music-tray-button-global music-tray-sub-category-button"
            subCatButton.id = cat
            subCatButton.innerHTML = subCat
            subCatButton.style.color = "rgba(255, 255, 255, 0.2)"
            subCatButton.onclick = () => {playMusicCategory(cat, mainCat).then()}
            document.getElementById(mainCat + "-music-subcategory").append(subCatButton);
        })
    })
})


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
        musicPlayer.children[0].src = "/music/" + category
        await musicPlayer.load()
        unmuteMusic()
        await musicPlayer.play()
    }
}


function unmuteMusic() {
    if (window.lastMusicCategory === null || musicPlayer.muted === true) {
        musicPlayer.volume = 0.08;
        musicPlayer.muted = false
        musicTrayPPIcon.src = '/cd?type=image&name=music-tray-pause.png';
        musicTrayPPIcon.alt = 'Pause';
        return true
    }
    return null
}


function muteMusic() {
    if (musicPlayer.muted === false) {
        musicPlayer.muted = true
        musicTrayPPIcon.src = '/cd?type=image&name=music-tray-resume.png';
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
        musicTrayToggleIcon.src = '/cd?type=image&name=music-tray-down.png';
        return true
    }
    return null
}


function closeMusicTray() {
    if (!musicTray.classList.contains('collapsed')) {
        musicTray.classList.toggle('collapsed');
        musicTrayToggleIcon.src = '/cd?type=image&name=music-tray-up.png';
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
