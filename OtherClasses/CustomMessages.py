class CustomMessageTask:
    REFRESH = "REFRESH"
    FRIEND_REMOVED = 'FRIEND_REMOVED'
    FRIEND_ADDED = 'FRIEND_ADDED'
    FRIEND_STATE_CHANGED = 'FRIEND_STATE_CHANGED'
    PAGE_CHANGED = 'PAGE_CHANGED'
    ADDED_PARTY_MEMBER = 'ADDED_PARTY_MEMBER'
    REMOVED_PARTY_MEMBER = 'REMOVED_PARTY_MEMBER'
    DECREMENT_PARTY_MEMBER_INDEX = 'DECREMENT_PARTY_MEMBER_INDEX'
    NEW_LEADER = 'NEW_LEADER'
    KICKED_FROM_PARTY = 'KICKED_FROM_PARTY'
    CHAT = 'CHAT'
    PARTY_CODE = 'PARTY_CODE'
    TOGGLE_SOCIALS = 'TOGGLE_SOCIALS'
    NEW_INTERACTION = 'NEW_INTERACTION'
    DELETE_INTERACTION = 'DELETE_INTERACTION'


class CustomMessages:
    @staticmethod
    def refreshBrowser():
        return {"MESSAGE": CustomMessageTask.REFRESH}
    @staticmethod
    def pageChanged(newPage):
        return {"MESSAGE": CustomMessageTask.PAGE_CHANGED, "PAGE": newPage}
    @staticmethod
    def friendRemoved(username):
        return {"MESSAGE": CustomMessageTask.FRIEND_REMOVED, "USERNAME":username}
    @staticmethod
    def friendAdded(player):
        return {"MESSAGE": CustomMessageTask.FRIEND_ADDED, "USERNAME": player.displayUserName(), "PFP": player.displayPFP(), "STATE": player.displayState()}
    @staticmethod
    def friendStateChanged(player):
        return {"MESSAGE": CustomMessageTask.FRIEND_STATE_CHANGED, "USERNAME": player.displayUserName(), "PFP": player.displayPFP(), "STATE": player.displayState()}
    @staticmethod
    def addedPartyMember(index, player):
        return {"MESSAGE": CustomMessageTask.ADDED_PARTY_MEMBER, "INDEX": index, "PFP":player.displayPFP(), "USERNAME": player.displayUserName(), "LEVEL": player.displayLevel(), "RANK": player.displayRank()}
    @staticmethod
    def removedPartyMember(index):
        return {"MESSAGE": CustomMessageTask.REMOVED_PARTY_MEMBER, "INDEX": index}
    @staticmethod
    def decrementPartyMemberIndex(start, end):
        return {"MESSAGE": CustomMessageTask.DECREMENT_PARTY_MEMBER_INDEX, "START": start, "END": end}
    @staticmethod
    def newLeader(oldIndex, newIndex):
        return {"MESSAGE": CustomMessageTask.NEW_LEADER, "OLD": oldIndex, "NEW": newIndex}
    @staticmethod
    def partyCode(code):
        return {"MESSAGE": CustomMessageTask.PARTY_CODE, "CODE": code}
    @staticmethod
    def chatMessage(receiver, sender, text):
        return {"MESSAGE": CustomMessageTask.CHAT, "TO":receiver, "FROM": sender, "TEXT": text}
    @staticmethod
    def toggleSocials(display:bool):
        return {"MESSAGE": CustomMessageTask.TOGGLE_SOCIALS, "DISPLAY": display}
    @staticmethod
    def newSocialInteraction(username, interactionID, interactionType):
        return {"MESSAGE": CustomMessageTask.NEW_INTERACTION, "USERNAME": username, "ID":interactionID, "TYPE":interactionType}
    @staticmethod
    def deleteInteraction(interactionID):
        return {"MESSAGE": CustomMessageTask.DELETE_INTERACTION, "ID":interactionID}