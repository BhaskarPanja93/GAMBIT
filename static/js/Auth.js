waitForElementPresence("#auth-renderer", (button)=>{
    button.onclick = () => sendCustomMessage({PURPOSE: "RENDER_AUTH_FORMS"})
})