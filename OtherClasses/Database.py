class Database:
    DATABASE_NAME ="GAMBIT"


    class CAREER:
        TABLE_NAME ="career"

        QUIZ_ID = "quiz_id"
        USERNAME = "username"
        END_AT = "end_at"
        MMR_OFFSET = "mmr_offset"


    class IP_PENALTY:
        TABLE_NAME ="ip_penalty"

        ADDRESS = "address"
        COUNT = "count"


    class NOTE_RELEVANCE:
        TABLE_NAME ="note_relevance"

        NOTE_ID = "note_id"
        SUBJECT = "subject"
        HEADER = "header"
        DESCRIPTION = "description"


    class NOTE:
        TABLE_NAME ="note"

        NOTE_ID = "note_id"
        USERNAME = "username"


    class PURCHASABLE:
        TABLE_NAME ="purchasable"

        ITEM_ID = "item_id"
        PRICE = "price"
        ADDED_ON = "added_on"


    class QUESTION:
        TABLE_NAME ="question"

        QUESTION_ID = "question_id"
        TEXT = "text"
        QUIZ_ELIGIBLE = "quiz_eligible"
        OPTIONS = "options"
        CORRECT = "correct"
        ATTACHMENTS = "attachments"


    class QUIZ:
        TABLE_NAME ="quiz"

        QUIZ_ID = "quiz_id"
        END_AT = "end_at"
        TEAM_DATA = "team_data"
        PLAYER_DATA = "player_data"


    class USER_INFO:
        TABLE_NAME ="user_info"

        USERNAME = "username"
        PERSON_NAME = "person_name"
        AGE = "age"
        JOINED = "joined"


    class USER_AUTH:
        TABLE_NAME = "user_auth"

        USERNAME = "username"
        EMAIL = "email"
        PW_HASH = "pw_hash"


    class USER_DEVICES:
        TABLE_NAME ="user_devices"

        VIEWER_ID = "viewer_id"
        USERNAME = "username"
        LAST_SEEN = "last_seen"


    class PURCHASES:
        TABLE_NAME ="purchases"

        PURCHASE_ID = "purchase_id"
        USERNAME = "username"
        ITEM_ID = "item_id"


    class FRIEND:
        TABLE_NAME ="friend"

        P1 = "p1"
        P2 = "p2"

    class PENDING_CHATS:
        TABLE_NAME ="pending_chats"

        RECEIVER = "receiver"
        SENDER = "sender"
        TEXT = "text"


    class PENDING_FRIEND_REQUESTS:
        TABLE_NAME ="pending_friend_requests"

        RECEIVER = "receiver"
        SENDER = "sender"