from peewee import *

from config.config import get_my_sql_database

db = get_my_sql_database()


class DataTransfer(Model):
    """
    DataSource对象对应表
    CREATE TABLE `data_transfer` (
      `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '主键自增',
      `name` VARCHAR(50) NOT NULL COMMENT '转换名称',
      `outdbid` INT(11) NOT NULL COMMENT '转出DB',
      `indbid` INT(11) NOT NULL COMMENT '转入DB',
      `outsql` TEXT NOT NULL COMMENT '转出语句',
      `insql` TEXT NOT NULL COMMENT '转入语句',
      `outfields` VARCHAR(200) NOT NULL COMMENT '转出字段,分割',
      `infields` VARCHAR(200) NOT NULL COMMENT '转入字段,分割',
      `transtype` TINYINT(1) NOT NULL COMMENT '转换类型 1 全量（先增后删） 2 增量（直接insert） 3 更新（根据key insert 或者update）',
      `transkey` VARCHAR(200) DEFAULT NULL COMMENT '转换类型key,分割',
      `fieldmap` TEXT DEFAULT NULL COMMENT '字段映射类型为 A:a:转换方法名称如果没有直接转换,B:b',
      `isdel` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
      `createTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `updateTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
      PRIMARY KEY (`id`)
    )
    """
    id = AutoField()
    name = CharField()
    outdbid = IntegerField()
    indbid = IntegerField()
    outsql = TextField()
    insql = TextField()
    outfields = CharField()
    infields = CharField()
    transtype = IntegerField()
    transkey = CharField()
    fieldmap = TextField()
    isdel = IntegerField()
    createTime = DateTimeField()
    updateTime = DateTimeField()

    class Meta:
        database = db
        table_name = 'data_transfer'
        primary_key = CompositeKey('id')
