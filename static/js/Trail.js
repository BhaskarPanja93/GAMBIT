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
