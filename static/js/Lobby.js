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
    waitForElementCreation(`#player-${playerData["INDEX"]}`, (div)=>{
        div.appendChild(playerPFP)
        div.appendChild(playerNameHeading)
        div.appendChild(playerLevelParagraph)
        div.appendChild(rankImage)
    })
}