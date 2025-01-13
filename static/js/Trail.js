const windowWidth = window.innerWidth;
const windowHeight = window.innerHeight;
const maxX = windowWidth - 10;
const maxY = windowHeight - 10;
document.addEventListener("mousemove", function (e) {
    if (Math.random() < 0.9) {
        const particle = document.createElement('div');
        const posX = Math.min(Math.max(e.pageX - 5, 0), maxX);
        const posY = Math.min(Math.max(e.pageY - 5, 0), maxY);
        particle.classList.add('particle');
        particle.style.left = `${posX}px`;
        particle.style.top = `${posY}px`;
        document.body.appendChild(particle);
        setTimeout(() => {
            particle.remove();
        }, 1000);
    }
});