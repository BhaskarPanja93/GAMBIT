class CustomMessageTask:
    FRIEND_REMOVED = 'FRIEND_REMOVED'
    FRIEND_ADDED = 'FRIEND_ADDED'
    PAGE_CHANGED = 'PAGE_CHANGED'
    ADDED_PARTY_MEMBER = 'ADDED_PARTY_MEMBER'
    REMOVED_PARTY_MEMBER = 'REMOVED_PARTY_MEMBER'
    KICKED_FROM_PARTY = 'KICKED_FROM_PARTY'
    CHAT = 'CHAT'
    PARTY_CODE = 'PARTY_CODE'


class CustomMessages:
    @staticmethod
    def pageChanged(newPage):
        return {"MESSAGE": CustomMessageTask.PAGE_CHANGED, "PAGE": newPage}
    @staticmethod
    def friendRemoved(connectionID):
        return {"MESSAGE": CustomMessageTask.FRIEND_REMOVED, "CONNECTION_ID":connectionID}
    @staticmethod
    def friendAdded():
        return {"MESSAGE": CustomMessageTask.FRIEND_ADDED, "FRIEND_DATA": {}}
    @staticmethod
    def addedPartyMember(index, PFP, username, level, rank):
        return {"MESSAGE": CustomMessageTask.ADDED_PARTY_MEMBER, "INDEX": index, "PFP":PFP, "USERNAME": username, "LEVEL": level, "RANK": rank}
    @staticmethod
    def removedPartyMember():
        return {"MESSAGE": CustomMessageTask.REMOVED_PARTY_MEMBER}
    @staticmethod
    def kickedFromParty():
        return {"MESSAGE": CustomMessageTask.KICKED_FROM_PARTY}
    @staticmethod
    def partyCode(code):
        return {"MESSAGE": CustomMessageTask.PARTY_CODE, "CODE": code}
    @staticmethod
    def chatMessage(sender, text):
        return {"MESSAGE": CustomMessageTask.CHAT, "SENDER": sender, "TEXT": text}
