document.addEventListener('DOMContentLoaded', function () {
    const musicTray = document.getElementById('music-tray');
    const musicTrayToggleButton = document.getElementById('music-tray-toggle-btn');
    const musicBtn = document.getElementById('music-pp-btn');
    const toggleImage = musicTrayToggleButton.querySelector('img');
    const audio = document.getElementById('audio');
    const icon = document.getElementById('icon');
    musicBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            icon.src = 'pause-button.png';
            icon.alt = 'Pause';
        } else {
            audio.pause();
            icon.src = 'play-button.png';
            icon.alt = 'Play';
        }
    });
    musicTrayToggleButton.addEventListener('click', () => {
        musicTray.classList.toggle('collapsed');
        if (musicTray.classList.contains('collapsed')) {
            toggleImage.src = 'upArrow.png';
        } else {
            toggleImage.src = 'downArrow.png';
        }
    });
});
