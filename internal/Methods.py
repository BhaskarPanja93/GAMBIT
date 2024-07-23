from customisedLogs import Manager as LogManager
from pooledMySQL import Manager as MySQLPool
from internal import SecretEnums


class commonMethods:
    @staticmethod
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


    @staticmethod
    def sqlISafe(parameter):
        """
        Sanitise SQL syntax before passing it to main Database
        :param parameter: String containing the syntax to execute
        :return:
        """
        if type(parameter) == str:
            return parameter.replace("'", "").replace('"', "").strip()
        return parameter


    @staticmethod
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
