class Database:
    SELF = "GAMBIT"

    class CAREER:
        SELF = "career"

        QUIZ_ID = "quiz_id"
        USER_ID = "user_id"
        END_AT = "end_at"
        MMR_OFFSET = "mmr_offset"

    class IP_PENALTY:
        SELF = "ip_penalty"

        ADDRESS = "address"
        COUNT = "count"

    class NOTE_RELEVANCE:
        SELF = "note_relevance"

        NOTE_ID = "note_id"
        SUBJECT = "subject"
        HEADER = "header"
        DESCRIPTION = "description"

    class NOTE:
        SELF = "note"

        NOTE_ID = "note_id"
        USER_ID = "user_id"

    class PURCHASABLE:
        SELF = "purchasable"

        ITEM_ID = "item_id"
        PRICE = "price"
        ADDED_ON = "added_on"

    class QUESTION:
        SELF = "question"

        QUESTION_ID = "question_id"
        TEXT = "text"
        QUIZ_ELIGIBLE = "quiz_eligible"
        CORRECT = "correct"
        INCORRECT = "incorrect"
        ATTACHMENTS = "attachments"

    class QUIZ:
        SELF = "quiz"

        QUIZ_ID = "quiz_id"
        END_AT = "end_at"
        TEAM_DATA = "team_data"
        PLAYER_DATA = "player_data"

    class USER_INFO:
        SELF = "user_info"

        USER_ID = "user_id"
        PERSON_NAME = "person_name"
        AGE = "age"
        JOINED = "joined"

    class USER_AUTH:
        SELF = "user_auth"

        USER_ID = "user_id"
        USERNAME = "username"
        PW_HASH = "pw_hash"

    class USER_DEVICES:
        SELF = "user_devices"

        VIEWER_ID = "viewer_id"
        USER_ID = "user_id"
        CREATED = "created"

    class PURCHASES:
        SELF = "purchases"

        PURCHASE_ID = "purchase_id"
        USER_ID = "user_id"
        ITEM_ID = "item_id"

