from customisedLogs import Manager as LogManager
from pooledMySQL import Manager as MySQLPool
from internal import SecretEnums


def checkRelatedIP(addressA: str, addressB: str):
    """
    Check if 2 IPv4 belong to same */24 subnet
    :param addressA: IPv4 as string
    :param addressB: IPv4 as string
    :return:
    """
    if addressA.count(".") == 3 and addressB.count(".") == 3:
        a = addressA.split(".")[:-1]
        b = addressB.split(".")[:-1]
        return a == b
    return addressA == addressB


def sqlISafe(parameter):
    """
    Sanitise SQL syntax before passing it to main Database
    :param parameter: String containing the syntax to execute
    :return:
    """
    if type(parameter) == str:
        return parameter.replace("'", "").replace('"', "").strip()
    return parameter


def connectDB(logger:LogManager) -> MySQLPool:
    """
    Blocking function to connect to DB
    :return: None
    """
    for host in SecretEnums.DBData.DBHosts.value:
        try:
            mysqlPool = MySQLPool(user=SecretEnums.DBData.DBUser.value, password=SecretEnums.DBData.DBPassword.value, dbName=SecretEnums.DBData.DBName.value, host=host)
            mysqlPool.execute(f"SELECT DATABASE();")
            logger.success("DB", f"connected to: {host}")
            return mysqlPool
        except:
            logger.failed("DB", f"failed: {host}")
    else:
        logger.fatal("DB", "Unable to connect to DataBase")
        input("EXIT...")
        exit(0)



def matchInternalJWT(flaskFunction):
    """
    Authentication Decorator to allow only matching (internalJWT, userUID, deviceUID, username) values
    :param flaskFunction: the function to switch context to if auth succeeds
    :return:
    """
    def __checkJWTCorrectness(request:Request):
        """
        Fetch values from request and match with DB
        :param request: Flask Request object
        :return: bool stating if values matched
        """
        username = commonMethods.sqlISafe(request.headers.get("USERNAME"))
        deviceUID = commonMethods.sqlISafe(request.headers.get("DEVICE-UID"))
        userUID = commonMethods.sqlISafe(request.headers.get("USER-UID"))
        internalJWT = commonMethods.sqlISafe(request.headers.get("INTERNAL-JWT"))
        userUIDExpectedTupList  = mysqlPool.execute(f"SELECT user_uid from user_connection_auth where internal_jwt=\"{internalJWT}\" and user_uid=\"{userUID}\"")
        userUIDReal = ""
        if len(userUIDExpectedTupList) == 1:
            userUIDReal = userUIDExpectedTupList[0][0].decode()
        if username and deviceUID and userUID and internalJWT and userUIDReal and userUIDReal == userUID:
            return True, userUID, deviceUID
        return False, "", ""
    @wraps(flaskFunction)
    def wrapper():
        """
        Function to decide if all requests are allowed or only recognised ones, else return a 403
        :return: Flask response object
        """
        if LOGIN_REQUIRED:
            jwtCorrect, userUID, deviceUID = __checkJWTCorrectness(request)
            if not jwtCorrect:
                logger.failed("JWT", f"{request.url_rule} incorrect")
                statusCode = 403
                statusDesc = Response403Messages.coreRejectedAuth.value
                return CustomResponse().readValues(statusCode, statusDesc, "").createFlaskResponse()
        else:
            userUID, deviceUID = "", ""
        return flaskFunction(userUID, deviceUID)
    return wrapper


