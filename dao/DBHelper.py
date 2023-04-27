import cx_Oracle
import pymongo
import pymysql
# import pyodbc
import redis
from clickhouse_driver import Client


def get_db_connection(dbType, dbHost, dbPort, dbName, username, password):
    """
    获取数据库连接
    :param dbType: 包括 mysql oracle sqlserver redis mongodb clickhouse
    :param dbHost:
    :param dbPort:
    :param dbName:
    :param username:
    :param password:
    :return:
    """
    # 如果连接数据异常，返回None
    try:
        if dbType == "mysql":
            conn = pymysql.connect(host=dbHost, port=dbPort, user=username, password=password, database=dbName)
            return conn
        elif dbType == "oracle":
            dsn = cx_Oracle.makedsn(dbHost, dbPort, dbName)
            conn = cx_Oracle.connect(user=username, password=password, dsn=dsn)
            return conn
        # elif dbType == "sqlserver":
        #    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + dbHost + ';DATABASE=' + dbName + ';UID=' + username + ';PWD=' + password
        #    conn = pyodbc.connect(conn_str)
        #    return conn
        elif dbType == "redis":
            conn = redis.Redis(host=dbHost, port=dbPort, db=dbName, password=password)
            return conn
        elif dbType == "mongodb":
            client = pymongo.MongoClient(
                'mongodb://' + username + ':' + password + '@' + dbHost + ':' + str(dbPort) + '/' + dbName)
            db = client.get_database(dbName)
            return db
        elif dbType == "clickhouse":
            conn = Client(host=dbHost, port=dbPort, user=username, password=password, database=dbName)
            return conn
        else:
            return None
    except Exception as e:
        print(e)
        return None
