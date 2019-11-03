#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Create instance of these flask extensions '''
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Flask-Cors plugin
from sqlalchemy import MetaData

cors = CORS()
# Flask-SQLAlchemy plugin

"""
 Can't emit DROP CONSTRAINT for constraint ForeignKeyConstraint(..., None, .......); it has no name

意思是，删除这个约束，但是这个约束叫None，他没有名字，删不掉！！！！
"""
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
# # Flask-Migrate plugin

"""
这次坑的是sqlite，主要是sqlite自己太坑。它不支持drop列，不支持完整的数据库alter语句功能等等。当使用sqlite做migrate和upgrade以及downgrade时，模型有字段的减少或者约束的减少，会报错：

        No support for ALTER of constraints in SQLite dialect

        解决方法：

        初始化Migrate对象时可以设置其提交类型为批处理
"""
migrate = Migrate(render_as_batch=True)