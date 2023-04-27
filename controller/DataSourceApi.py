from typing import Optional

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from playhouse.shortcuts import model_to_dict

from dao.DataSourceDao import DataSourceDao, get_db_connection_for_datasource

"""
    数据源接口类型
"""

dataSourceApi = FastAPI()


# 查询数据源列表
@dataSourceApi.get("/list")
async def querylist(name: Optional[str] = None, dbType: Optional[str] = None):
    """
    查询数据源列表
    :param name: 数据库名称
    :param dbType: 数据库类型
    :return:
    """
    result = None
    # 根据 name 和 dbType 查询数据源列表
    if name is not None and dbType is not None:
        result = DataSourceDao.select().where(DataSourceDao.name == name, DataSourceDao.type == dbType)
    # 根据 name 查询数据源列表
    elif name is not None:
        result = DataSourceDao.select().where(DataSourceDao.name == name)
    # 根据 dbType 查询数据源列表
    elif dbType is not None:
        result = DataSourceDao.select().where(DataSourceDao.type == dbType)
    # 查询所有数据源列表
    else:
        result = DataSourceDao.select()

    rs = [model_to_dict(r) for r in result]

    return {'code': 200, 'msg': 'success', 'data': rs}


# 新增数据源
@dataSourceApi.post("/add")
async def add(req: Request):
    """
    新增数据源
    :param req
    :return:
    """
    item_json = await req.json()
    item_dict = jsonable_encoder(item_json)
    item = DataSourceDao(**item_dict)
    result = item.save()
    return jsonable_encoder(result, include="non-recursive")


# 修改数据源
@dataSourceApi.post("/update")
async def update(req: Request):
    """
    修改数据源
    :param name: 数据库名称
    :param dbType: 数据库类型
    :return:
    """
    item_json = await req.json()
    item_dict = jsonable_encoder(item_json)
    item = DataSourceDao(**item_dict)
    result = item.save();

    return jsonable_encoder(result, include="non-recursive")


# 删除数据源
@dataSourceApi.get("/delete")
async def delete(id):
    """
    删除数据源
    :param name: 数据库名称
    :param dbType: 数据库类型
    :return:
    """
    result = DataSourceDao.delete().where(DataSourceDao.id == id)

    return jsonable_encoder(result, include="non-recursive")


# 测试数据源连接
@dataSourceApi.get("/test")
async def test(id):
    """
    测试数据源连接
    :param name: 数据库名称
    :param dbType: 数据库类型
    :return:
    """
    # 1. 根据 id 查询数据源信息
    dataInfos = DataSourceDao.select().where(DataSourceDao.id == id)
    # 如果存在记录，则获取第一条记录的 id 值
    if dataInfos:
        dataInfo = dataInfos[0]
    else:
        return {'code': 500, 'msg': 'error', 'data': None}

    # 2. 根据数据源信息测试连接 ("mysql", "localhost", 3306, "config", "root", "123456")
    db = get_db_connection_for_datasource(dataInfo)
    # 3. 返回测试结果
    if db is not None:
        result = {'code': 200, 'msg': 'success', 'data': None}
    else:
        result = {'code': 500, 'msg': 'error', 'data': None}

    return jsonable_encoder(result, include="non-recursive")
