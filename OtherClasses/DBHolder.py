from threading import Thread
from time import sleep
from customisedLogs import CustomisedLogs
from pooledMySQL import PooledMySQL


class DBHolder:
    from internal.Credentials import DBData
    def __init__(self, logger:CustomisedLogs):
        self.db:None|PooledMySQL = None
        self.logger:CustomisedLogs = logger
        self.initialised = False
        Thread(target=self.__initialise).start()


    def __connect(self, logger: CustomisedLogs) -> None:
        """
        Blocking function to connect to DB
        :return: None
        """
        for host in DBHolder.DBData.DBHosts:
            try:
                mysqlPool = PooledMySQL(user=DBHolder.DBData.DBUser, password=DBHolder.DBData.DBPassword, dbName=DBHolder.DBData.DBName, host=host)
                mysqlPool.execute("SHOW DATABASES", dbRequired=False, catchErrors=False)
                logger.log(logger.Colors.green_800, "DB", f"connected to: {host}")
                self.db=mysqlPool
                return
            except:
                logger.log(logger.Colors.red_500, "DB", f"failed: {host}")
        else:
            logger.log(logger.Colors.red_800, "DB", "Unable to connect to DataBase")
            input("EXIT...")
            exit(0)


    def __initialise(self):
        """
        Initialise DB when called for
        :return:
        """
        if self.initialised: return
        sleep(0.001)
        self.__connect(self.logger)
        self.initialised = True


    def useDB(self):
        """
        Waits till DB preparation and then executes DB commands
        :return:
        """
        while not self.initialised: sleep(1)
        return self.db

