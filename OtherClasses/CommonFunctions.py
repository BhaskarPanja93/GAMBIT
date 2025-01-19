from pathlib import Path

from customisedLogs import CustomisedLogs
from flask import Flask
from pooledMySQL import PooledMySQL

from OtherClasses.WSGIElements import LoggerAttachedWSGIServer
from internal.Credentials import DBData


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


def connectDB(logger: CustomisedLogs) -> PooledMySQL:
    """
    Blocking function to connect to DB
    :return: None
    """
    for host in DBData.DBHosts:
        try:
            mysqlPool = PooledMySQL(user=DBData.DBUser, password=DBData.DBPassword, dbName=DBData.DBName, host=host)
            mysqlPool.execute("SHOW DATABASES", dbRequired=False, catchErrors=False)
            logger.log(logger.Colors.green_800, "DB", f"connected to: {host}")
            return mysqlPool
        except:
            logger.log(logger.Colors.red_500, "DB", f"failed: {host}")
    else:
        logger.log(logger.Colors.red_800, "DB", "Unable to connect to DataBase")
        input("EXIT...")
        exit(0)


def WSGIRunner(app: Flask, port: int, route: str, logger: CustomisedLogs):
    cert_file = r'C:\cert\fullchain1.pem'
    key_file = r'C:\cert\privkey1.pem'
    if Path(cert_file).is_file() and Path(key_file).is_file():
        print(f"https://127.0.0.1:{port}{route}")
        LoggerAttachedWSGIServer(('0.0.0.0', port,), app, logger, certfile=cert_file, keyfile=key_file).serve_forever()
    else:
        print(f"http://127.0.0.1:{port}{route}")
        LoggerAttachedWSGIServer(('0.0.0.0', port,), app, logger).serve_forever()