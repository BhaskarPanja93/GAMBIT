from OtherClasses.Player import Player


class CustomMessageTask:
    REFRESH = "REFRESH"
    FRIEND_REMOVED = 'FRIEND_REMOVED'
    FRIEND_ADDED = 'FRIEND_ADDED'
    PAGE_CHANGED = 'PAGE_CHANGED'
    ADDED_PARTY_MEMBER = 'ADDED_PARTY_MEMBER'
    REMOVED_PARTY_MEMBER = 'REMOVED_PARTY_MEMBER'
    DECREMENT_PARTY_MEMBER_INDEX = 'DECREMENT_PARTY_MEMBER_INDEX'
    NEW_LEADER = 'NEW_LEADER'
    KICKED_FROM_PARTY = 'KICKED_FROM_PARTY'
    CHAT = 'CHAT'
    PARTY_CODE = 'PARTY_CODE'
    TOGGLE_SOCIALS = 'TOGGLE_SOCIALS'


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
    def friendAdded(username, pfp, state):
        return {"MESSAGE": CustomMessageTask.FRIEND_ADDED, "FRIEND_DATA": {"USERNAME": username, "PFP": pfp, "STATE": state}}
    @staticmethod
    def addedPartyMember(index, player: Player):
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
    def chatMessage(category, sender, text):
        return {"MESSAGE": CustomMessageTask.CHAT, "CATEGORY":category, "SENDER": sender, "TEXT": text}
    @staticmethod
    def toggleSocials(display:bool):
        return {"MESSAGE": CustomMessageTask.TOGGLE_SOCIALS, "DISPLAY": display}