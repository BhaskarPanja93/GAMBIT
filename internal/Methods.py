from customisedLogs import CustomisedLogs
from pooledMySQL import PooledMySQL
try: from SecretEnums import * ## change
except: from internal.SecretEnums import * ## change


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


def connectDB(logger:CustomisedLogs) -> PooledMySQL:
    """
    Blocking function to connect to DB
    :return: None
    """
    for host in DBData.DBHosts.value:
        try:
            mysqlPool = PooledMySQL(user=DBData.DBUser.value, password=DBData.DBPassword.value, dbName=DBData.DBName.value, host=host)
            mysqlPool.execute(f"SELECT DATABASE();")
            logger.log(logger.Colors.green_800, "DB", f"connected to: {host}")
            return mysqlPool
        except:
            logger.log(logger.Colors.red_500, "DB", f"failed: {host}")
    else:
        logger.log(logger.Colors.red_800, "DB", "Unable to connect to DataBase")
        input("EXIT...")
        exit(0)



