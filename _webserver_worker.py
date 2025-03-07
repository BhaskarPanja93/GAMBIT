from gevent import monkey

monkey.patch_all()

from datetime import datetime
from time import time, sleep
from sys import argv
from typing import Any
from flask import request, redirect, make_response
from jinja2 import Template
from argon2 import PasswordHasher

from OtherClasses.PlayerStatus import PlayerStatus
from OtherClasses.Question import Question
from OtherClasses.ChatMessageNodes import ChatMessageNodes
from OtherClasses.Quiz import Quiz
from OtherClasses.PrivateData import PrivateData
from OtherClasses.Matchmaker import Matchmaker, Match
from OtherClasses.FileNames import FileNames
from OtherClasses.Database import Database
from OtherClasses.CachedElements import CachedElements
from OtherClasses.CoreValues import CoreValues
from OtherClasses.DivIDs import DivID
from OtherClasses.Pages import Pages
from OtherClasses.Social import Player, SocialInteraction
from OtherClasses.Party import Party
from OtherClasses.Routes import Routes
from OtherClasses.CustomMessages import CustomMessages
from OtherClasses.WSGIElements import WSGIRunner
from OtherClasses.DBHolder import DBHolder
from OtherClasses.Interactions import Interactions


from customisedLogs import CustomisedLogs
from internal.dynamicWebsite import DynamicWebsite


##############################################################################################################################
# NAVBAR


def renderBaseNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.BaseNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.BaseNavbar)
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.BaseNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar1, UpdateMethods.update)


def removeBaseNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.BaseNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.BaseNavbar)
        viewerObj.updateHTML("", DivID.navbar1, UpdateMethods.update)


def renderLobbyNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.LobbyNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.LobbyNavbar)
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.LobbyNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar2, UpdateMethods.update)


def removeLobbyNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.LobbyNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.LobbyNavbar)
        viewerObj.updateHTML("", DivID.navbar2, UpdateMethods.update)



def renderQuizNavbar(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.QuizNavbar):
        viewerObj.privateData.renderElement(FileNames.HTML.QuizNavbar)
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.QuizNavbar)).render(baseURI=viewerObj.privateData.baseURI), DivID.navbar2, UpdateMethods.update)


def removeQuizNavbar(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.isElementRendered(FileNames.HTML.QuizNavbar):
        viewerObj.privateData.removeElement(FileNames.HTML.QuizNavbar)
        viewerObj.updateHTML("", DivID.navbar2, UpdateMethods.update)


##############################################################################################################################
# AUTH PAGES


def __renderAuthStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() not in [Pages.AUTH, Pages.PRE_AUTH, Pages.HOMEPAGE]:
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.AuthStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.Ghost3d)).render(baseURI=viewerObj.privateData.baseURI), DivID.ghost3d, UpdateMethods.update)


def renderAuthPre(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    removeBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    #hideSocials(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.PRE_AUTH:
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.AuthPre)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.PRE_AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.PRE_AUTH))


def renderAuthForms(viewerObj: DynamicWebsite.Viewer):
    __renderAuthStructure(viewerObj)
    removeBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    hideSocials(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.AUTH:
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.AuthForms)).render(baseURI=viewerObj.privateData.baseURI), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.AUTH)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.AUTH))
        sendLoginForm(viewerObj)
        sendRegisterForm(viewerObj)


def renderHomePage(viewerObj: DynamicWebsite.Viewer):
    #return renderLobby(viewerObj)
    updateStatus(viewerObj.privateData.player, PlayerStatus.ONLINE)
    __renderAuthStructure(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    renderBaseNavbar(viewerObj)
    showSocials(viewerObj)
    if viewerObj.privateData.currentPage() != Pages.HOMEPAGE:
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.Homepage)).render(baseURI=viewerObj.privateData.baseURI, player=viewerObj.privateData.player), DivID.auth, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.HOMEPAGE)
        viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.HOMEPAGE))


##############################################################################################################################
# CHAT ELEMENTS


def renderChatStructure(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.ChatFull):
        viewerObj.privateData.renderElement(FileNames.HTML.ChatFull)
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.ChatFull)).render(baseURI=viewerObj.privateData.baseURI), DivID.chatBox, UpdateMethods.update)
        pendingChats = DBHolder.useDB().execute(f"SELECT * FROM {Database.PENDING_CHATS.TABLE_NAME} WHERE {Database.PENDING_CHATS.RECEIVER}=? ORDER BY {Database.PENDING_CHATS.SENT_AT}", [viewerObj.privateData.userName])
        DBHolder.useDB().execute(f"DELETE FROM {Database.PENDING_CHATS.TABLE_NAME} WHERE {Database.PENDING_CHATS.RECEIVER}=?", [viewerObj.privateData.userName])
        for chat in pendingChats: viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, chat[Database.PENDING_CHATS.SENDER].decode(), chat[Database.PENDING_CHATS.TEXT]))


##############################################################################################################################
# MUSIC TRAY


def renderMusicTray(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.MusicTray)).render(baseURI=viewerObj.privateData.baseURI), DivID.musicTrayHolder, UpdateMethods.update)


##############################################################################################################################
# FRIEND ELEMENTS


def showSocials(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isElementRendered(FileNames.HTML.SocialsStructure):
        viewerObj.privateData.renderElement(FileNames.HTML.SocialsStructure)
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.SocialsStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.friendsStructure, UpdateMethods.update)
        for friendInfo in [{"result":b"SleepBot"}]+DBHolder.useDB().execute(f"""SELECT CASE
            WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
            WHEN {Database.FRIEND.P2} = ? THEN {Database.FRIEND.P1}
            END AS result FROM {Database.FRIEND.TABLE_NAME}""", [viewerObj.privateData.userName, viewerObj.privateData.userName]):
            if friendInfo and friendInfo["result"]:
                friendUsername = friendInfo["result"].decode()
                if friendUsername in activeUsernames:
                    player = activeUsernames[friendUsername].privateData.player
                else:
                    player = Player(None, friendUsername)
                    player.setStatus(PlayerStatus.OFFLINE)
                viewerObj.sendCustomMessage(CustomMessages.friendAdded(player))
    viewerObj.sendCustomMessage(CustomMessages.toggleSocials(True))


def hideSocials(viewerObj: DynamicWebsite.Viewer):
    viewerObj.sendCustomMessage(CustomMessages.toggleSocials(False))


##############################################################################################################################
# NAVGRID PAGES


def renderNavGrid(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() != Pages.NAVGRID:
        viewerObj.privateData.newPage(Pages.NAVGRID)
        viewerObj.updateHTML(cachedElements.fetchStaticHTML(FileNames.HTML.NavgridStructure), DivID.changingPage, UpdateMethods.update)
        updateStatus(viewerObj.privateData.player, PlayerStatus.ONLINE)
        renderBaseNavbar(viewerObj)
        removeLobbyNavbar(viewerObj)
        removeQuizNavbar(viewerObj)
        showSocials(viewerObj)


##############################################################################################################################
# LOBBY PAGES


def __renderLobbyStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() != Pages.LOBBY:
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.LobbyStructure)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
        viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.LobbyFeatures)).render(baseURI=viewerObj.privateData.baseURI), DivID.lobbyFeatures, UpdateMethods.update)
        viewerObj.privateData.newPage(Pages.LOBBY)


def renderLobby(viewerObj: DynamicWebsite.Viewer):
    __renderLobbyStructure(viewerObj)
    updateStatus(viewerObj.privateData.player, PlayerStatus.LOBBY)
    renderBaseNavbar(viewerObj)
    renderLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    showSocials(viewerObj)
    if viewerObj.privateData.player.party is None:
        createParty(viewerObj.privateData.player)
    else:
        viewerObj.privateData.player.party.reRenderLobby(viewerObj.privateData.player)


##############################################################################################################################
# QUIZ PAGES


def __renderQuizStructure(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.currentPage() != Pages.QUIZ:
        viewerObj.privateData.newPage(Pages.QUIZ)
        viewerObj.privateData.player.viewer.sendCustomMessage(CustomMessages.pageChanged(Pages.QUIZ))


def renderQuiz(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.QuizFull)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)
    renderQuizNavbar(viewerObj)


def renderMatchFound(viewerObj: DynamicWebsite.Viewer):
    __renderQuizStructure(viewerObj)
    hideSocials(viewerObj)
    removeBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    viewerObj.updateHTML(cachedElements.fetchStaticHTML(FileNames.HTML.MatchFound), DivID.changingPage, UpdateMethods.update)


##############################################################################################################################
# NOTES DASHBOARD


def renderDashboard(viewerObj):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.Dashboard)).render(baseURI=viewerObj.privateData.baseURI, player=viewerObj.privateData.player), DivID.changingPage, UpdateMethods.update)
    renderBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)


##############################################################################################################################
# NOTES PAGES


def __renderNotesFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.NotesPageFull)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)


def renderNotes(viewerObj: DynamicWebsite.Viewer):
    __renderNotesFullPage(viewerObj)
    updateStatus(viewerObj.privateData.player, PlayerStatus.NOTES)
    renderBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    hideSocials(viewerObj)
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.NOTES))



##############################################################################################################################
# FLASHCARD PAGES


def __renderFlashcardsFullPage(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.Flashcard)).render(baseURI=viewerObj.privateData.baseURI), DivID.changingPage, UpdateMethods.update)


def renderFlashcards(viewerObj: DynamicWebsite.Viewer):
    __renderFlashcardsFullPage(viewerObj)
    updateStatus(viewerObj.privateData.player, PlayerStatus.FLASHCARD)
    renderBaseNavbar(viewerObj)
    removeLobbyNavbar(viewerObj)
    removeQuizNavbar(viewerObj)
    hideSocials(viewerObj)
    viewerObj.sendCustomMessage(CustomMessages.pageChanged(Pages.FLASHCARD))


##############################################################################################################################
# CONTEXTUAL


def renderPreAuthUniversal(viewerObj: DynamicWebsite.Viewer):
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.PreAuthUniversal):
        viewerObj.privateData.renderScript(FileNames.JS.PreAuthUniversal)
        viewerObj.updateHTML(f"<script id='{FileNames.JS.PreAuthUniversal}'>" + cachedElements.fetchStaticJS(FileNames.JS.PreAuthUniversal) + "</script>", DivID.scripts, UpdateMethods.append)
    if not viewerObj.privateData.isScriptRendered(FileNames.JS.Trail):
        viewerObj.privateData.renderScript(FileNames.JS.Trail)
        viewerObj.updateHTML(f"<script id='{FileNames.JS.Trail}'>" + cachedElements.fetchStaticJS(FileNames.JS.Trail) + "</script>", DivID.scripts, UpdateMethods.append)
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.UniversalContainer)).render(baseURI=viewerObj.privateData.baseURI), DivID.root, UpdateMethods.update)


##############################################################################################################################
# DECIDE FIRST PAGE


def renderFirstPage(viewerObj: DynamicWebsite.Viewer, isAuthenticated: bool):
    if isAuthenticated:
        setPlayerDetails(viewerObj)
        if viewerObj.privateData.expectedPostAuthPage == Pages.LOBBY: renderLobby(viewerObj)
        elif viewerObj.privateData.expectedPostAuthPage == Pages.QUIZ: renderQuiz(viewerObj)
        #elif viewerObj.privateData.expectedPostAuthPage == Pages.marketPlace: renderMarketPlace(viewerObj)
        else: renderHomePage(viewerObj)
        renderChatStructure(viewerObj)
    else:
        renderAuthPre(viewerObj)


##############################################################################################################################
# USER ACTIONS


def performActionPostSecurity(viewerObj: DynamicWebsite.Viewer, form: dict, isSecure:bool):
    if "PURPOSE" not in form: return
    purpose = form.pop("PURPOSE")
    print(purpose, viewerObj.privateData.currentPage())

    if viewerObj.privateData.currentPage() == Pages.AUTH:
        if purpose == "LOGIN" and isSecure:
            resetFormErrors(viewerObj)
            identifier = form.get("identifier").strip()
            password = form.get("password").strip()
            if not identifier:
                sendLoginCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.loginIdentifierError, "Invalid Username/Email")
            if not password:
                sendLoginCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.loginIdentifierError, "Invalid Password")

            accepted, reason = manualLogin(viewerObj, identifier, password)
            if accepted:
                return renderFirstPage(viewerObj, accepted)
            else:
                sendLoginCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.loginIdentifierError, reason)
        elif purpose == "REGISTER" and isSecure:
            resetFormErrors(viewerObj)
            username = form.get("user-name").strip()
            password = form.get("password").strip()
            confirmPassword = form.get("confirm-password").strip()
            email = form.get("email").strip()
            name = form.get("person-name").strip()
            if not username:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerUsernameError, "Invalid Username")
            if not password:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerPasswordError, "Invalid Password")
            if password != confirmPassword:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerPasswordError, "Passwords Do Not Match")
            if not email:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerEmailError, "Invalid Email")
            if not name:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerNameError, "Invalid Name")

            accepted, reason = createUser(viewerObj, username, password, name, email)
            if accepted:
                return renderFirstPage(viewerObj, accepted)
            else:
                sendRegisterCSRF(viewerObj)
                return rejectForm(viewerObj, DivID.registerGeneralError, reason)
    if viewerObj.privateData.currentPage() == Pages.PRE_AUTH:
        if purpose == "RENDER_AUTH_FORMS":
            return renderAuthForms(viewerObj)
    if viewerObj.privateData.currentPage() == Pages.LOBBY:
        if purpose == "PARTY_CODE":
            return viewerObj.privateData.player.party.generatePartyCode()
        if purpose == "PARTY_CODE_INPUT":
            newParty = partyCodes.get(form.get("CODE"))
            if newParty is not None:
                oldParty = viewerObj.privateData.player.party
                if oldParty.partyID != newParty.partyID:
                    viewerObj.privateData.player.party = newParty
                    if oldParty: oldParty.removePlayer(viewerObj.privateData.player, True)
                    cleanupPartyInvites(viewerObj)
                    return newParty.addPlayer(viewerObj.privateData.player)
        if purpose == "READY":
            return viewerObj.privateData.player.party.playerReady(viewerObj.privateData.player)
        if purpose == "UN_READY":
            return viewerObj.privateData.player.party.playerUnready(viewerObj.privateData.player)
    if viewerObj.privateData.currentPage() == Pages.QUIZ:
        if purpose == "OPTION_SELECTED":
            if form.get("QUESTION") in viewerObj.privateData.player.quizQuestions and viewerObj.privateData.player.party.team.match.quiz.currentQuestionID == form.get("QUESTION"):
                question:Question = viewerObj.privateData.player.quizQuestions[form.get("QUESTION")]
                question.selectedOption = question.fetchOption(form.get("OPTION"))
                question.timeTaken = time() - question.startTime
                return
    if viewerObj.privateData.currentPage() not in [Pages.AUTH, Pages.PRE_AUTH, Pages.HOMEPAGE, Pages.QUIZ]:
        if purpose == "RENDER_HOMEPAGE":
            return renderHomePage(viewerObj)
    if viewerObj.privateData.currentPage() not in [Pages.AUTH, Pages.PRE_AUTH, Pages.NAVGRID, Pages.QUIZ]:
        if purpose == "RENDER_NAVGRID":
            return renderNavGrid(viewerObj)
    if viewerObj.privateData.currentPage() == Pages.NAVGRID:
        if purpose == "RENDER_LOBBY":
            return renderLobby(viewerObj)
    if viewerObj.privateData.currentPage() == Pages.NAVGRID:
        if purpose == "RENDER_NOTES":
            return renderNotes(viewerObj)
    if viewerObj.privateData.currentPage() == Pages.NAVGRID:
        if purpose == "RENDER_DASHBOARD":
            return renderDashboard(viewerObj)
    if viewerObj.privateData.currentPage() == Pages.NAVGRID:
        if purpose == "RENDER_FLASHCARD":
            return renderFlashcards(viewerObj)
    if viewerObj.privateData.currentPage() == Pages.NAVGRID:
        if purpose == "RENDER_MARKETPLACE":
            return renderMarketplace(viewerObj)
    if viewerObj.privateData.currentPage() == Pages.NAVGRID:
        if purpose == "RENDER_CHATBOT":
            return renderChatbot(viewerObj)

    if viewerObj.privateData.currentPage() not in [Pages.PRE_AUTH, Pages.AUTH]:
        if purpose == "CHAT":
            form["TEXT"] = Template(form["TEXT"][:100]).render()
            form["TO"] = Template(form["TO"]).render()
            if form["TO"] == ChatMessageNodes.PARTY:
                if viewerObj.privateData.player.party is not None:
                    return viewerObj.privateData.player.party.receiveMessage(viewerObj.privateData.userName, form["TEXT"])
                else:
                    viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, "You need to be in a party to send this message."))
            elif form["TO"] == ChatMessageNodes.TEAM:
                if viewerObj.privateData.player.party is not None:
                    if viewerObj.privateData.player.party.team is not None:
                        return viewerObj.privateData.player.party.team.receiveMessage(viewerObj.privateData.userName, form["TEXT"])
                    else:
                        viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, "You need to be in a team to send this message."))
            elif form["TO"] in viewerObj.privateData.player.friends:
                if form["TO"] in activeUsernames: activeUsernames[form["TO"]].sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, viewerObj.privateData.userName, form["TEXT"]))
                else: DBHolder.useDB().execute(f"INSERT INTO {Database.PENDING_CHATS.TABLE_NAME} VALUES (?, ?, ?, ?)", [form['TO'], viewerObj.privateData.userName, form['TEXT'], datetime.now()])
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(form["TO"], ChatMessageNodes.YOU, form["TEXT"]))
            else:
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, "Unable to send. Recipient unknown"))
        if purpose == "PARTY_INVITE":
            friendUsername = Template(form["USERNAME"]).render()
            if friendUsername in viewerObj.privateData.player.friends and friendUsername in activeUsernames: # person valid
                if activeUsernames[friendUsername].privateData.player.party.partyID == viewerObj.privateData.player.party.partyID: # Same party
                    return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{friendUsername} already in your party"))
                if friendUsername in viewerObj.privateData.player.outgoingPartyInvites: # Already invited
                    return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{friendUsername} already has a pending invite"))
                if friendUsername in viewerObj.privateData.player.incomingPartyJoinRequests:
                    invite = viewerObj.privateData.player.incomingPartyJoinRequests[friendUsername]
                    del viewerObj.privateData.player.incomingPartyJoinRequests[friendUsername]
                    invite.destroy()
                    if viewerObj.privateData.userName in activeUsernames[friendUsername].privateData.player.outgoingPartyJoinRequests:
                        del activeUsernames[friendUsername].privateData.player.outgoingPartyJoinRequests[viewerObj.privateData.userName]
                    if form.get("ACTION") is None or form.get("ACTION")==True:
                        oldParty = activeUsernames[friendUsername].privateData.player.party
                        activeUsernames[friendUsername].privateData.player.party = viewerObj.privateData.player.party
                        if oldParty: oldParty.removePlayer(activeUsernames[friendUsername].privateData.player, True)
                        cleanupPartyInvites(viewerObj)
                        return viewerObj.privateData.player.party.addPlayer(activeUsernames[friendUsername].privateData.player)
                    else:
                        return
                else:
                    if not viewerObj.privateData.player.party:
                        return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"Unable to invite {friendUsername}. You are not in a party"))
                    if len(viewerObj.privateData.player.party.players) < viewerObj.privateData.player.party.maxPlayers:
                        invite = SocialInteraction(Interactions.PARTY_INVITE, viewerObj.privateData.player, activeUsernames[friendUsername].privateData.player, viewerObj.privateData.player.party)
                        viewerObj.privateData.player.outgoingPartyInvites[friendUsername] = invite
                        activeUsernames[friendUsername].privateData.player.incomingPartyInvites[viewerObj.privateData.userName] = invite
                        return invite.sendToReceiver()
                    else:
                        return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"Unable to invite {friendUsername}. Party full"))
            else:
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"Unable to invite {friendUsername}. Recipient unknown"))
        if purpose == "PARTY_JOIN_REQUEST":
            friendUsername = Template(form["USERNAME"]).render()
            if friendUsername in viewerObj.privateData.player.friends and friendUsername in activeUsernames: # person valid
                if activeUsernames[friendUsername].privateData.player.party.partyID == viewerObj.privateData.player.party.partyID: # Same party
                    return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{friendUsername} already in your party"))
                if friendUsername in viewerObj.privateData.player.outgoingPartyJoinRequests: # Already requested
                    return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{friendUsername} already has a pending request"))
                if friendUsername in viewerObj.privateData.player.incomingPartyInvites:
                    invite = viewerObj.privateData.player.incomingPartyInvites[friendUsername]
                    del viewerObj.privateData.player.incomingPartyInvites[friendUsername]
                    invite.destroy()
                    if viewerObj.privateData.userName in activeUsernames[friendUsername].privateData.player.outgoingPartyInvites:
                        del activeUsernames[friendUsername].privateData.player.outgoingPartyInvites[viewerObj.privateData.userName]
                    if form.get("ACTION") is None or form.get("ACTION")==True:
                        oldParty = viewerObj.privateData.player.party
                        viewerObj.privateData.player.party = activeUsernames[friendUsername].privateData.player.party
                        if oldParty: oldParty.removePlayer(viewerObj.privateData.player, True)
                        cleanupPartyInvites(viewerObj)
                        return activeUsernames[friendUsername].privateData.player.party.addPlayer(viewerObj.privateData.player)
                    else:
                        return
                else:
                    if not activeUsernames[friendUsername].privateData.player.party:
                        return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"Unable to request {friendUsername}. Player not in a party"))
                    if len(activeUsernames[friendUsername].privateData.player.party.players) < activeUsernames[friendUsername].privateData.player.party.maxPlayers:
                        invite = SocialInteraction(Interactions.PARTY_JOIN_REQUEST, viewerObj.privateData.player, activeUsernames[friendUsername].privateData.player, activeUsernames[friendUsername].privateData.player.party)
                        viewerObj.privateData.player.outgoingPartyJoinRequests[friendUsername] = invite
                        activeUsernames[friendUsername].privateData.player.incomingPartyJoinRequests[viewerObj.privateData.userName] = invite
                        return invite.sendToReceiver()
                    else:
                        return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"Unable to invite {friendUsername}. Party disallowed"))
            else:
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"Unable to invite {friendUsername}. Recipient unknown"))

        if purpose == "FRIEND_REQUEST":
            friendUsername = Template(form["USERNAME"]).render()
            if friendUsername == viewerObj.privateData.userName:
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"You are your own friend!"))
            if friendUsername in viewerObj.privateData.player.friends: # Already a friend
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{friendUsername} is already a friend"))
            if not DBHolder.useDB().execute(f"SELECT {Database.USER_INFO.USERNAME} FROM {Database.USER_INFO.TABLE_NAME} WHERE {Database.USER_INFO.USERNAME} = ?", [friendUsername]): # No such username
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"ID {friendUsername} doesn't exist"))
            if friendUsername in viewerObj.privateData.player.outgoingFriendRequests: # Already sent a request
                return viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{friendUsername} didn't accept your last request"))
            if friendUsername in viewerObj.privateData.player.incomingFriendRequests: # Already received a request
                if form.get("ACTION") is None or form.get("ACTION")==True:
                    return registerBiDirectionFriend(viewerObj.privateData.userName, friendUsername, True)
                else:
                    cleanupFriendRequest(viewerObj.privateData.userName, friendUsername, True)
            else: # First interaction
                DBHolder.useDB().execute(f"INSERT INTO {Database.PENDING_FRIEND_REQUESTS.TABLE_NAME} VALUES (?, ?)", [friendUsername, viewerObj.privateData.userName])
                if friendUsername in activeUsernames:
                    friendReq = SocialInteraction(Interactions.FRIEND_REQUEST, viewerObj.privateData.player, activeUsernames[friendUsername].privateData.player)
                    friendReq.sendToReceiver()
                    activeUsernames[friendUsername].privateData.player.incomingFriendRequests[viewerObj.privateData.userName] = friendReq
                    activeUsernames[friendUsername].sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{viewerObj.privateData.userName} sent friend request"))
                else:
                    player = Player(None, friendUsername)
                    friendReq = SocialInteraction(Interactions.FRIEND_REQUEST, viewerObj.privateData.player, player)
                viewerObj.privateData.player.outgoingFriendRequests[friendUsername] = friendReq
                viewerObj.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"Sent Friend Request to {friendUsername}"))
                return
        if purpose == "FRIEND_REMOVE":
            username = form["USERNAME"]
            if username in viewerObj.privateData.player.friends:
                DBHolder.useDB().execute(f"DELETE FROM {Database.FRIEND.TABLE_NAME} WHERE ({Database.FRIEND.P1}=? AND {Database.FRIEND.P2}=?) OR ({Database.FRIEND.P1}=? AND {Database.FRIEND.P2}=?) LIMIT 1", [username, viewerObj.privateData.userName, viewerObj.privateData.userName, username])
                viewerObj.privateData.player.friends.remove(username)
                viewerObj.sendCustomMessage(CustomMessages.friendRemoved(username))
                if username in activeUsernames:
                    activeUsernames[username].privateData.player.friends.remove(viewerObj.privateData.userName)
                    activeUsernames[username].sendCustomMessage(CustomMessages.friendRemoved(viewerObj.privateData.userName))
                    return


    if viewerObj.privateData.currentPage() in [Pages.LOBBY, Pages.HOMEPAGE, Pages.NOTES, Pages.MARKETPLACE]:
        if purpose == "LOGOUT":
            freeActiveUsername(viewerObj.privateData.userName)
            logoutDevice(viewerObj)
            viewerObj.privateData.player.removePFP()
            updateStatus(viewerObj.privateData.player, PlayerStatus.OFFLINE)
            cleanupPartyInvites(viewerObj)
            return viewerObj.sendCustomMessage(CustomMessages.refreshBrowser())

    return rejectForm(viewerObj, form, "Unknown Purpose")


def rejectForm(viewerObj: DynamicWebsite.Viewer, divToTarget, reason):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.FormErrorElement)).render(errorText=reason), divToTarget, UpdateMethods.update)
    print("FORM REJECTED")


def formSubmitCallback(viewerObj: DynamicWebsite.Viewer, form: dict):
    print("Form received: ", viewerObj.viewerID, form, type(form))
    performActionPostSecurity(viewerObj, form, True)


def customWSMessageCallback(viewerObj: DynamicWebsite.Viewer, message: Any):
    print("WS received: ", viewerObj.viewerID, message, type(message))
    performActionPostSecurity(viewerObj, message, False)


def visitorLeftCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Left: ", viewerObj.viewerID)
    if viewerObj.privateData.player is not None and viewerObj.privateData.player.party is not None:
        viewerObj.privateData.player.party.removePlayer(viewerObj.privateData.player, False)
    if viewerObj.privateData.player is not None: viewerObj.privateData.player.removePFP()
    updateStatus(viewerObj.privateData.player, PlayerStatus.OFFLINE)
    cleanupPartyInvites(viewerObj)
    freeActiveUsername(viewerObj.privateData.userName)


def newVisitorCallback(viewerObj: DynamicWebsite.Viewer):
    print("Visitor Joined: ", viewerObj.viewerID)
    setPrivateDetails(viewerObj)
    accepted, reason = autoLogin(viewerObj)
    renderPreAuthUniversal(viewerObj)
    renderMusicTray(viewerObj)
    renderFirstPage(viewerObj, accepted)


def firstPageCreator():
    return make_response(Template(cachedElements.fetchStaticHTML(FileNames.HTML.FirstPage)).render(title="GAMBIT", baseURI=request.path))


def freeActiveUsername(userName):
    if userName in activeUsernames:
        del activeUsernames[userName]
        print("Freed username:", userName)


##############################################################################################################################
# AUTHENTICATION


def resetFormErrors(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML("", DivID.loginIdentifierError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerGeneralError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerNameError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerEmailError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerUsernameError, UpdateMethods.update)
    viewerObj.updateHTML("", DivID.registerPasswordError, UpdateMethods.update)


def sendLoginCSRF(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(viewerObj.purposeManager.createCSRF("LOGIN"), DivID.loginCSRF, UpdateMethods.update)


def sendRegisterCSRF(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(viewerObj.purposeManager.createCSRF("REGISTER"), DivID.registerCSRF, UpdateMethods.update)


def sendLoginForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.Login)).render(baseURI=viewerObj.privateData.baseURI), DivID.loginForm, UpdateMethods.update)
    sendLoginCSRF(viewerObj)


def sendRegisterForm(viewerObj: DynamicWebsite.Viewer):
    viewerObj.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.Register)).render(baseURI=viewerObj.privateData.baseURI), DivID.registerForm, UpdateMethods.update)
    sendRegisterCSRF(viewerObj)


def checkPasswordStrength(password:str):
    return len(password) >= 8 and password.isalnum()


def logoutDevice(viewerObj: DynamicWebsite.Viewer):
    DBHolder.useDB().execute(f"DELETE FROM {Database.USER_DEVICES.TABLE_NAME} WHERE {Database.USER_DEVICES.VIEWER_ID}=? LIMIT 1", [viewerObj.viewerID])


def createDevice(viewerObj: DynamicWebsite.Viewer):
    logoutDevice(viewerObj)
    DBHolder.useDB().execute(f"INSERT INTO {Database.USER_DEVICES.TABLE_NAME} VALUES (?, ?, ?)", [viewerObj.viewerID, viewerObj.privateData.userName, viewerObj.privateData.activeSince])


def setPrivateDetails(viewerObj: DynamicWebsite.Viewer):
    viewerObj.privateData = PrivateData()
    viewerObj.privateData.baseURI = request.path.split("?")[0]


def setPlayerDetails(viewerObj: DynamicWebsite.Viewer):
    if viewerObj.privateData.player is None:
        viewerObj.privateData.player = Player(viewerObj)
        r = DBHolder.useDB().execute(f"""SELECT {Database.USER_INFO.XP}, {Database.USER_INFO.HIDDEN_MMR}, {Database.USER_INFO.VISIBLE_MMR} FROM {Database.USER_INFO.TABLE_NAME} WHERE {Database.USER_INFO.USERNAME}=? LIMIT 1""", [viewerObj.privateData.userName])
        r= r[0]
        viewerObj.privateData.player.setXP(r[Database.USER_INFO.XP])
        viewerObj.privateData.player.setVisibleMMR(r[Database.USER_INFO.VISIBLE_MMR])
        viewerObj.privateData.player.hiddenMMR = r[Database.USER_INFO.HIDDEN_MMR]
        viewerObj.privateData.player.setPFP()
        for friend in DBHolder.useDB().execute(f"""SELECT CASE
                WHEN {Database.FRIEND.P1} = ? THEN {Database.FRIEND.P2}
                WHEN {Database.FRIEND.P2} = ? THEN {Database.FRIEND.P1}
                END AS result FROM {Database.FRIEND.TABLE_NAME}""", [viewerObj.privateData.userName, viewerObj.privateData.userName]):
            if friend and friend["result"]: viewerObj.privateData.player.friends.append(friend["result"].decode())
        for incomingFriendReq in DBHolder.useDB().execute(f"SELECT {Database.PENDING_FRIEND_REQUESTS.SENDER} FROM {Database.PENDING_FRIEND_REQUESTS.TABLE_NAME} WHERE {Database.PENDING_CHATS.RECEIVER}=?", [viewerObj.privateData.userName]):
            senderUsername = incomingFriendReq[Database.PENDING_FRIEND_REQUESTS.SENDER].decode()
            if senderUsername in activeUsernames:
                player = activeUsernames[senderUsername].privateData.player
            else:
                player = Player(None, senderUsername)
            friendRequest = SocialInteraction(Interactions.FRIEND_REQUEST, player, viewerObj.privateData.player)
            viewerObj.privateData.player.incomingFriendRequests[senderUsername] = friendRequest
            friendRequest.sendToReceiver()
        for outgoingFriendReq in DBHolder.useDB().execute(f"SELECT {Database.PENDING_FRIEND_REQUESTS.RECEIVER} FROM {Database.PENDING_FRIEND_REQUESTS.TABLE_NAME} WHERE {Database.PENDING_CHATS.SENDER}=?", [viewerObj.privateData.userName]):
            if not outgoingFriendReq[Database.PENDING_FRIEND_REQUESTS.RECEIVER]: continue
            receiverUsername = outgoingFriendReq[Database.PENDING_FRIEND_REQUESTS.RECEIVER].decode()
            if receiverUsername in activeUsernames:
                player = activeUsernames[receiverUsername].privateData.player
            else:
                player = Player(None, receiverUsername)
            viewerObj.privateData.player.outgoingFriendRequests[receiverUsername] = SocialInteraction(Interactions.FRIEND_REQUEST, viewerObj.privateData.player, player)
        updateStatus(viewerObj.privateData.player, PlayerStatus.ONLINE)


def createUser(viewerObj: DynamicWebsite.Viewer, username:str, password:str, personName:str, email:str):
    username = Template(username).render()
    if len(username) > 9:
        return False, "Username too long (max 9)"
    elif not username.isalnum():
        return False, "Username only allows [A-Z, a-z, 0-9]"
    elif len(password)<6:
        return False, "Password should be minimum 6 letters"
    elif DBHolder.useDB().execute(f"SELECT {Database.USER_AUTH.USERNAME} from {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.USERNAME}=? LIMIT 1", [username]):
        return False, "Username already registered"
    elif DBHolder.useDB().execute(f"SELECT {Database.USER_AUTH.EMAIL} from {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.EMAIL}=? LIMIT 1", [email]):
        return False, "Email already registered"
    else:
        DBHolder.useDB().execute(f"INSERT INTO {Database.USER_INFO.TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?)", [username, personName, viewerObj.privateData.activeSince, 1000, 1000, 1000])
        DBHolder.useDB().execute(f"INSERT INTO {Database.USER_AUTH.TABLE_NAME} VALUES (?, ?, ?)", [username, email, passwordHasher.hash(password)])
        allowed, reason = freezeViewerTillUsernameRelease(viewerObj, username)
        if allowed:
            createDevice(viewerObj)
            return True, "User registered"
        else:
            return False, reason


def manualLogin(viewerObj: DynamicWebsite.Viewer, identifier:str, password:str):
    savedCredentials = DBHolder.useDB().execute(f"SELECT {Database.USER_AUTH.USERNAME}, {Database.USER_AUTH.PW_HASH} FROM {Database.USER_AUTH.TABLE_NAME} where {Database.USER_AUTH.USERNAME}=? OR {Database.USER_AUTH.EMAIL}=? LIMIT 1", [identifier, identifier])
    if savedCredentials:
        savedCredentials = savedCredentials[0]
        username = savedCredentials[Database.USER_AUTH.USERNAME].decode()
        pwHash = savedCredentials[Database.USER_AUTH.PW_HASH]
        try:
            if passwordHasher.verify(pwHash.decode(), password):
                allowed, reason = freezeViewerTillUsernameRelease(viewerObj, username)
                if allowed:
                    createDevice(viewerObj)
                    return True, "Manual Logged In"
                else:
                    return False, reason
        except:
            pass
    return False, "Invalid Credentials"


def autoLogin(viewerObj: DynamicWebsite.Viewer):
    savedDevice = DBHolder.useDB().execute(f"SELECT {Database.USER_DEVICES.USERNAME} FROM {Database.USER_DEVICES.TABLE_NAME} WHERE {Database.USER_DEVICES.VIEWER_ID}=? LIMIT 1", [viewerObj.viewerID])
    if savedDevice:
        savedDevice = savedDevice[0]
        username = savedDevice[Database.USER_DEVICES.USERNAME].decode()
        allowed, reason = freezeViewerTillUsernameRelease(viewerObj, username)
        if allowed: return True, "Auto Logged In"
        else: return False, reason
    return False, "Unknown Device"


def freezeViewerTillUsernameRelease(viewerObj:DynamicWebsite.Viewer, username):
    print(viewerObj.cookie.instanceID, viewerObj.cookie.viewerID, username, "freezer")
    if username in activeUsernames:
        viewerObj.updateHTML("Please close any other instances/tabs to use GAMBIT on this tab.", DivID.root, DynamicWebsite.UpdateMethods.update)
        while username in activeUsernames and viewerObj.currentState != DynamicWebsite.VIEWER_STATES.DEAD:
            print(username, "FROZEN LOGIN")
            sleep(1)
        if viewerObj.currentState == DynamicWebsite.VIEWER_STATES.DEAD: return False, "Disconnected"
    print("Activated username:", username)
    activeUsernames[username] = viewerObj
    viewerObj.privateData.userName = username
    print(username, "ALLOWED LOGIN")
    return True, "Username free"


##############################################################################################################################
# PARTY


def closeParty(party: Party):
    if party.partyID in partyIDs: del partyIDs[party.partyID]
    if party.partyCode in partyCodes: del partyCodes[party.partyCode]
    matchmaker.removeFromQueue(party)


def onPartyCodeGenerated(party: Party):
    partyCodes[party.partyCode] = party


def createParty(player):
    party = Party(onPartyCodeGenerated, closeParty, renderLobby, cachedElements, matchmaker)
    partyIDs[party.partyID] = party
    if player: party.addPlayer(player)
    return party


##############################################################################################################################
# FRIENDS


def updateStatus(player:Player, newStatus):
    if player.state != newStatus:
        player.setStatus(newStatus)
        for friendUsername in player.friends:
            if friendUsername in activeUsernames:
                activeUsernames[friendUsername].sendCustomMessage(CustomMessages.friendStateChanged(player))


def cleanupPartyInvites(viewerObj: DynamicWebsite.Viewer):
    for friendUsername in list(viewerObj.privateData.player.outgoingPartyInvites):
        viewerObj.privateData.player.outgoingPartyInvites[friendUsername].destroy()
        del viewerObj.privateData.player.outgoingPartyInvites[friendUsername]
        if friendUsername in activeUsernames and viewerObj.privateData.userName in activeUsernames[friendUsername].privateData.player.incomingPartyInvites:
            del activeUsernames[friendUsername].privateData.player.incomingPartyInvites[viewerObj.privateData.userName]
    for friendUsername in list(viewerObj.privateData.player.outgoingPartyJoinRequests):
        viewerObj.privateData.player.outgoingPartyJoinRequests[friendUsername].destroy()
        del viewerObj.privateData.player.outgoingPartyJoinRequests[friendUsername]
        if friendUsername in activeUsernames and viewerObj.privateData.userName in activeUsernames[friendUsername].privateData.player.incomingPartyInvites:
            del activeUsernames[friendUsername].privateData.player.incomingPartyInvites[viewerObj.privateData.userName]
    for friendUsername in list(viewerObj.privateData.player.incomingPartyInvites):
        viewerObj.privateData.player.incomingPartyInvites[friendUsername].destroy()
        del viewerObj.privateData.player.incomingPartyInvites[friendUsername]
        if friendUsername in activeUsernames and viewerObj.privateData.userName in activeUsernames[friendUsername].privateData.player.outgoingPartyInvites:
            del activeUsernames[friendUsername].privateData.player.outgoingPartyInvites[viewerObj.privateData.userName]
    for friendUsername in list(viewerObj.privateData.player.outgoingPartyInvites):
        viewerObj.privateData.player.outgoingPartyInvites[friendUsername].destroy()
        del viewerObj.privateData.player.outgoingPartyInvites[friendUsername]
        if friendUsername in activeUsernames and viewerObj.privateData.userName in activeUsernames[friendUsername].privateData.player.outgoingPartyJoinRequests:
            del activeUsernames[friendUsername].privateData.player.outgoingPartyJoinRequests[viewerObj.privateData.userName]


def cleanupFriendRequest(username1, username2, flip=False):
    if username1 in activeUsernames:
        sender = activeUsernames[username1]
        friendRequest = sender.privateData.player.incomingFriendRequests.get(username2)
        if friendRequest:
            del sender.privateData.player.incomingFriendRequests[username2]
            friendRequest.destroy()
        friendRequest = sender.privateData.player.outgoingFriendRequests.get(username2)
        if friendRequest:
            del sender.privateData.player.outgoingFriendRequests[username2]
            friendRequest.destroy()
    if flip:
        DBHolder.useDB().execute(f"DELETE FROM {Database.PENDING_FRIEND_REQUESTS.TABLE_NAME} WHERE {Database.PENDING_FRIEND_REQUESTS.SENDER}=? AND {Database.PENDING_FRIEND_REQUESTS.RECEIVER}=?", [username1, username2])
        DBHolder.useDB().execute(f"DELETE FROM {Database.PENDING_FRIEND_REQUESTS.TABLE_NAME} WHERE {Database.PENDING_FRIEND_REQUESTS.SENDER}=? AND {Database.PENDING_FRIEND_REQUESTS.RECEIVER}=?", [username2, username1])
        cleanupFriendRequest(username2, username1)


def registerBiDirectionFriend(username1, username2, flip=False):
    if username1 in activeUsernames:
        receiver = activeUsernames[username1]
        receiver.privateData.player.friends.append(username2)
        receiver.sendCustomMessage(CustomMessages.chatMessage(ChatMessageNodes.YOU, ChatMessageNodes.SYSTEM, f"{username2} is now your friend"))
        if username2 in activeUsernames:
            other = activeUsernames[username2].privateData.player
        else:
            other = Player(None, username2)
        receiver.sendCustomMessage(CustomMessages.friendAdded(other))
    if flip:
        DBHolder.useDB().execute(f"INSERT INTO {Database.FRIEND.TABLE_NAME} VALUES (?, ?)", [username1, username2])
        cleanupFriendRequest(username1, username2, True)
        registerBiDirectionFriend(username2, username1, False)


##############################################################################################################################
# QUIZ


def onQuizEnd(quiz:Quiz):
    sortedPlayers = sorted(quiz.match.teamA.allPlayers()+quiz.match.teamB.allPlayers(), reverse=True)
    for toSend in sortedPlayers:
        if toSend.viewer is not None:
            toSend.viewer.privateData.newPage(Pages.QUIZ_SCOREBOARD)
            updateStatus(toSend, PlayerStatus.RESULT)
            renderBaseNavbar(toSend.viewer)
            removeQuizNavbar(toSend.viewer)
            toSend.viewer.updateHTML(Template(cachedElements.fetchStaticHTML(FileNames.HTML.QuizScoreBoard)).render(resultWord="VICTORY" if toSend.party.team.winner else "DEFEAT"), DivID.changingPage, DynamicWebsite.UpdateMethods.update)
            for player in sortedPlayers:
                player.healthImpact = int(player.healthImpact)
                player.score = int(player.score)
                if player.party.team.winner:
                    toSend.viewer.updateHTML(Template(quiz.cachedElements.fetchStaticHTML(FileNames.HTML.QuizScoreBoardWinnerElement)).render(player=player), DivID.quizScoreBoard, DynamicWebsite.UpdateMethods.append)
                else:
                    toSend.viewer.updateHTML(Template(quiz.cachedElements.fetchStaticHTML(FileNames.HTML.QuizScoreBoardLoserElement)).render(player=player), DivID.quizScoreBoard, DynamicWebsite.UpdateMethods.append)
    for player in sortedPlayers:
        player.party.team = None


def onMatchFound(match: Match):
    quiz = Quiz(match, onQuizEnd, cachedElements, DBHolder.useDB())
    for party in match.teamB.parties+match.teamA.parties:
        for player in party.players:
            if player.viewer is not None:
                updateStatus(player, PlayerStatus.QUIZ)
                player.score = 0
                player.correct = 0
                player.incorrect = 0
                player.healthImpact = 0
                player.quizQuestions = {}
                renderMatchFound(player.viewer)
    sleep(3)
    for party in match.teamB.parties+match.teamA.parties:
        for player in party.players:
            if player.viewer is not None:
                renderQuiz(player.viewer)
    quiz.start()


##############################################################################################################################
# TEST


def testMatchmaking():
    sleep(2)
    for _ in range(1):
        party = createParty(Player(None))
        matchmaker.addToQueue(party)
        #sleep(0.5)


##############################################################################################################################
# VARIABLES


serverStartTime = time()
fernetKey = argv[1]
webPort = int(argv[2])
cdPort = int(argv[3])
partyIDs:dict[str, Party] = {}
partyCodes:dict[str, Party] = {}

logger = CustomisedLogs()
DBHolder = DBHolder(logger)
passwordHasher = PasswordHasher()
UpdateMethods = DynamicWebsite.UpdateMethods
cachedElements = CachedElements()
matchmaker = Matchmaker(onMatchFound, cachedElements)
activeUsernames:dict[str, DynamicWebsite.Viewer] = {}
dynamicWebsiteApp = DynamicWebsite(firstPageCreator, newVisitorCallback, visitorLeftCallback, formSubmitCallback, customWSMessageCallback, fernetKey, CoreValues.appName, Routes.webHomePage)


@dynamicWebsiteApp.baseApp.get("/debug")
def _debug():
    final = ""
    final += "<br><br>Parties<br>"
    for partyID in partyIDs:
        final += "<br>&emsp;"+partyID
        final+="<br>&emsp;&emsp;Players"
        for player in partyIDs[partyID].players:
            final += "<br>&emsp;&emsp;"+player.userName
    final += "<br><br>Party Codes<br>"
    for partyCode in partyCodes:
        final += "<br>&emsp;"+partyCode+"&emsp;&emsp;"+partyCodes[partyCode].partyID
    return final


@dynamicWebsiteApp.baseApp.before_request
def _modHeadersBeforeRequest():
    """
    Before any request goes to any route, it passes through this function.
    Applies user remote address correctly (received from proxy)
    :return:
    """
    if request.remote_addr == "127.0.0.1":
        if request.environ.get("HTTP_X_FORWARDED_FOR") is not None:
            address = request.environ.get("HTTP_X_FORWARDED_FOR")
        else: address = "LOCALHOST"
        request.remote_addr = address
    if request.environ.get("HTTP_X_FORWARDED_PATH") is not None:
        request.path = request.environ.get("HTTP_X_FORWARDED_PATH")
    else:
        request.path = ""
    if request.environ.get("HTTP_X_FORWARDED_PROTO") is not None:
        request.scheme = request.environ.get("HTTP_X_FORWARDED_PROTO")


@dynamicWebsiteApp.baseApp.errorhandler(Exception)
def handle_404(error):
    return redirect("http://"+request.environ["HTTP_HOST"].replace(str(webPort), str(cdPort))+request.environ["PATH_INFO"]+"?"+request.environ["QUERY_STRING"])


#Thread(target=testMatchmaking).start()

WSGIRunner(dynamicWebsiteApp.baseApp, webPort, Routes.webHomePage, logger)