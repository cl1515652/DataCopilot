from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder

from dao.DataSourceDao import DataSourceDao, get_db_connection_for_datasource
from utils.DBQueryUtils import query_helper

queryDataApi = FastAPI()


@queryDataApi.post('/query')
async def query(req: Request):
    """
    查询数据
    :param sc_id: 数据源Id
    :param sql: 查询的SQL语句
    :return:
    """
    # 1. 根据 id 查询数据源信息

    item_json = await req.json()
    item_dict = jsonable_encoder(item_json)
    item = DataSourceDao(**item_dict)

    sc_id = item.id
    sql = item.sql

    datasources = DataSourceDao.select().where(DataSourceDao.id == sc_id)
    if datasources.count() == 0:
        return {'code': 500, 'msg': '数据源不存在', 'data': None}
    else:
        dataInfo = datasources[0]

    # 2. 根据数据源信息，获取到数据库连接
    conn = get_db_connection_for_datasource(dataInfo)

    # 3. 执行sql
    data = query_helper(dataInfo.type, conn, sql)

    return {'code': 200, 'msg': 'success', 'data': data}
