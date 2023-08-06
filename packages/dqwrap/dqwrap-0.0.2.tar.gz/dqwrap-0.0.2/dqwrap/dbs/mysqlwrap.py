import pymysql, typing
from .basedbwrap import BaseDbWrap


class MysqlWrap(BaseDbWrap):
    def __init__(self, con):
        super(MysqlWrap, self).__init__(con)

    def cursor(self):
        return self.con.cursor(pymysql.cursors.DictCursor)

    def set_auto_commit(self, b: bool):
        self.execute("set autocommit=" + "1" if b else "0")

    def escape_field(self, field: str):
        i = field.find(".")
        if -1 == i:
            return "`" + field + "`"
        else:
            return field[0:i + 1] + "`" + field[i + 1:] + "`"

    def escape_table(self, table:str):
        return "`" + table + "`"

    def _inesrt_id(self, cursor: pymysql.cursors.DictCursor):
        return cursor.lastrowid

    def insert(self, table:str, record: dict, insert_id=True):
        return super(MysqlWrap, self).insert(table, record, self._inesrt_id if insert_id else None, insert_id)

    def update(self, table:str, param: dict, id_field="id", cb: typing.Callable = None):
        return super(MysqlWrap, self).update(table,param,id_field,lambda c:c.rowcount)

    def delete(self, table:str, id, id_field="id", cb: typing.Callable = None):
        return super(MysqlWrap, self).delete(table,id,id_field,lambda c:c.rowcount)