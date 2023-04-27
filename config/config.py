from peewee import MySQLDatabase


def get_my_sql_database():
    """

    :return:
    """
    return MySQLDatabase('data_copilot', user='root', password='IyUn9@6{)qq',
                         host='172.18.12.33', port=3306)
