import pymysql

import simplejson


# 查询数据库
def query_helper(dbtype, conn, sql):
    """
    根据 dbtype 执行 sql，返回 JSON 形式的查询结果，包含列名和数据。
    :param dbtype:  数据库类型 包括 mysql oracle redis mongodb clickhouse
    :param conn:    数据库连接
    :param sql:     查询语句
    :return:        JSON 形式的查询结果，包含列名和数据
    """
    try:

        desc = None
        # 判断数据库类型并执行查询操作
        if dbtype == 'mysql':
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 设置游标返回字典形式的数据，含列名
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        elif dbtype == 'oracle':
            cursor = conn.cursor()  # 不支持返回字典形式的数据和含列名的查询操作
            cursor.execute(sql)
            desc = [col[0] for col in cursor.description]  # 获取列名
            result = [dict(zip(desc, row)) for row in cursor]  # 将查询结果转换为字典形式
            cursor.close()
        elif dbtype == 'redis':
            result = conn.execute_command(sql)
        elif dbtype == 'mongodb':
            result = list(conn.find(sql))
        elif dbtype == 'clickhouse':
            cursor = conn.cursor()
            cursor.execute(sql)
            desc = [col[0] for col in cursor.description]  # 获取列名
            result = [dict(zip(desc, row)) for row in cursor.fetchall()]  # 将查询结果转换为字典形式
            cursor.close()
    except Exception as e:
        return simplejson.dumps({"errMessage": str(e)}, default=str)

    return simplejson.dumps({"columns": desc, "data": result}, default=str)
