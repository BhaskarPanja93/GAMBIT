class Database:
    DATABASE_NAME ="GAMBIT"


    class FLASHCARD_COLLECTIONS:
        TABLE_NAME = "flashcard_collections"


        COLLECTION_ID = "collection_id"
        USERNAME = "username"
        SUBJECT = "subject"
        TITLE = "title"
        CARD_COUNT = "card_count"
        NOTE_ID = "note_id"
        CREATED_AT = "created_at"
        LAST_OPENED = "last_opened"


    class FLASHCARD_QUESTIONS:
        TABLE_NAME = "flashcard_questions"

        QUESTION_ID = "question_id"
        COLLECTION_ID = "collection_id"
        QUESTION = "question"
        ANSWER = "answer"
        LAST_ANSWERED = "last_answered"
        NEXT_APPEARANCE = "next_appearance"


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


    class NOTES:
        TABLE_NAME ="notes"

        NOTE_ID = "note_id"
        USERNAME = "username"
        SUBJECT = "subject"
        HEADER = "header"
        DESCRIPTION = "description"
        VISITS = "visits"
        PRIVATE = "private"
        CREATED_AT = "created_at"
        LAST_OPENED = "last_opened"


    class PURCHASABLE:
        TABLE_NAME ="purchasable"

        ITEM_ID = "item_id"
        PRICE = "price"
        ADDED_ON = "added_on"

    class ATTACHMENTS:
        TABLE_NAME ="attachments"

        ATTACHMENT_ID = "attachment_id"
        TYPE = "type"
        Y = "y"
        X = "x"

    class QUIZ_QUESTIONS:
        TABLE_NAME ="quiz_questions"

        QUESTION_ID = "question_id"
        TEXT = "text"
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
        HIDDEN_MMR = "hidden_mmr"
        VISIBLE_MMR = "visible_mmr"
        XP = "xp"


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
        SENT_AT = "sent_at"


    class PENDING_FRIEND_REQUESTS:
        TABLE_NAME ="pending_friend_requests"

        RECEIVER = "receiver"
        SENDER = "sender"


    class SESSION_DURATION:
        TABLE_NAME = "session_duration"

        USERNAME = "username"
        START = "start"
        END = "end"