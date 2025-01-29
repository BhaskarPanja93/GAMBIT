class CustomMessageTask:
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
    def chatMessage(sender, text):
        return {"MESSAGE": CustomMessageTask.CHAT, "SENDER": sender, "TEXT": text}
