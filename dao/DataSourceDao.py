from peewee import *

from config.config import get_my_sql_database
from dao.DBHelper import get_db_connection

db = get_my_sql_database()


class DataSourceDao(Model):
    """
    DataSource对象对应表
    CREATE TABLE `datasource_config` (
      `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '主键自增',
      `name` VARCHAR(50) NOT NULL COMMENT '名称',
      `type` VARCHAR(50) NOT NULL COMMENT '数据库类型',
      `url` VARCHAR(200) NOT NULL COMMENT '数据库连接URL',
      `host` VARCHAR(50) NOT NULL COMMENT '数据库地址',
      `port` INT(11) NOT NULL COMMENT '数据库端口',
      `db` VARCHAR(50) NOT NULL COMMENT '数据库名称',
      `username` VARCHAR(50) NOT NULL COMMENT '用户名',
      `password` VARCHAR(50) NOT NULL COMMENT '密码',
      `isdel` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
      `createTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `updateTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
      PRIMARY KEY (`id`)
    )
    """
    id = AutoField()
    name = CharField()
    type = CharField()
    url = CharField()
    host = CharField()
    port = IntegerField()
    db = CharField()
    username = CharField()
    password = CharField()
    isdel = IntegerField()
    createTime = DateTimeField()
    updateTime = DateTimeField()

    class Meta:
        database = db
        table_name = 'datasource_config'
        # primary_key = CompositeKey('id')


def get_db_connection_for_datasource(dataInfo: DataSourceDao):
    """
    根据数据源信息，获取到数据库连接
    :param dataInfo:
    :return:
    """
    return get_db_connection(dbType=dataInfo.type, dbHost=dataInfo.host, dbPort=dataInfo.port, dbName=dataInfo.db,
                             username=dataInfo.username,
                             password=dataInfo.password);