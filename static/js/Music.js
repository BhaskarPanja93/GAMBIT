const music = document.getElementById('musicTray');
const musicTrayToggleButton = document.getElementById('music-tray-toggle-btn');
const musicTrayPPButton = document.getElementById('music-pp-btn');
const trayPPIcon = musicTrayPPButton.querySelector('img');
const trayToggleIcon = musicTrayToggleButton.querySelector('img');
const musicPlayer = document.getElementById('music-player');
musicPlayer.muted = true


const lofiPlayButton = document.getElementById('LOFI');
const jazzPlayButton = document.getElementById('JAZZ');
const classicalPlayButton = document.getElementById('CLASSICAL');
const ambientPlayButton = document.getElementById('AMBIENT');
const knownStreams = ["LOFI", "JAZZ", "CLASSICAL", "AMBIENT"]


window.lastMusicCategory = null
window.currentlyPlaying = false


lofiPlayButton.addEventListener('click', () => playMusicCategory(lofiPlayButton.id));
classicalPlayButton.addEventListener('click', () => playMusicCategory(classicalPlayButton.id));
jazzPlayButton.addEventListener('click', () => playMusicCategory(jazzPlayButton.id));
ambientPlayButton.addEventListener('click', () => playMusicCategory(ambientPlayButton.id));


async function playMusicCategory(category) {
    if (!knownStreams.includes(category)) return null
    if (window.lastMusicCategory === null || category!==window.lastMusicCategory) {
        muteMusic()
        if (window.lastMusicCategory !== null) document.getElementById(window.lastMusicCategory).style.color = "rgba(255, 255, 255, 0.5)";
        document.getElementById(category).style.color = "rgba(255, 255, 255, 1)";
        window.lastMusicCategory = category
        musicPlayer.children[0].src = "/music/" + category
        await musicPlayer.load()
        unmuteMusic()
        await musicPlayer.play()
    }
}


function unmuteMusic() {
    if (window.lastMusicCategory === null || musicPlayer.muted === true) {
        musicPlayer.volume = 0.05;
        musicPlayer.muted = false
        trayPPIcon.src = '/cd?type=image&name=music-tray-pause.png';
        trayPPIcon.alt = 'Pause';
        return true
    }
    return null
}
function muteMusic() {
    if (musicPlayer.muted === false) {
        musicPlayer.muted = true
        trayPPIcon.src = '/cd?type=image&name=music-tray-resume.png';
        trayPPIcon.alt = 'Play';
        return false
    }
    return null
}
function toggleMusicMute() {
    if (!(unmuteMusic() === true)) muteMusic()
}


function openMusicTray() {
    if (music.classList.contains('collapsed')) {
        music.classList.toggle('collapsed');
        trayToggleIcon.src = '/cd?type=image&name=music-tray-down.png';
        return true
    }
    return null
}
function closeMusicTray() {
    if (!music.classList.contains('collapsed')) {
        music.classList.toggle('collapsed');
        trayToggleIcon.src = '/cd?type=image&name=music-tray-up.png';
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
