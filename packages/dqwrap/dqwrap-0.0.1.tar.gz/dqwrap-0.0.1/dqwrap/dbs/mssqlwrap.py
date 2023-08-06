from .basedbwrap import BaseDbWrap


class MssqlWrap(BaseDbWrap):
    def __init__(self, con):
        super(MssqlWrap, self).__init__(con)

    def cursor(self):
        return self.con.cursor(as_dict=True)

    def set_auto_commit(self, b: bool):
        self.get_raw_con_from_DBUtils().autocommit(b)

    def escape_field(self, field: str):
        i = field.find(".")
        if -1 == i:
            return '[' + field + ']'
        else:
            return field[0:i + 1] + '[' + field[i + 1:] + ']'

    def _inesrt_id(self, cursor):
        r = cursor.fetchone()
        if r and len(r) > 0:
            return r[0]

    def insert(self, table, record: dict, insert_id=True):
        return super(MssqlWrap, self).insert(table, record, self._inesrt_id if insert_id else None, insert_id)
