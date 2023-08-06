from .basedbwrap import BaseDbWrap


class BaseDao:

    def __init__(self, table: str, con: BaseDbWrap):
        self.table = table
        self.con = con

    def insert(self, param):
        return self.con.insert(self.table, param)

    def delete(self, id, id_field="id"):
        return self.con.delete(self.table, id, id_field=id_field)

    def update(self, param, id_field="id"):
        return self.con.update(self.table, param, id_field=id_field)

    def get(self, id, id_field="id", fields=None):
        return self.con.get(self.table, id, id_field=id_field, fields=fields)

    def list(self, ids, append_sql="", id_field="id", fields=None):
        return self.con.list(self.table, ids, append_sql, id_field=id_field, fields=fields)

    def get_by_keys(self, kvs: dict, append_sql: str, id_field="id", fields=None):
        return self.con.get_by_keys(self.table, kvs=kvs, append_sql=append_sql, id_field=id_field, fields=fields)

    def list_by_keys(self, kvs: dict, append_sql: str, id_field="id", fields=None):
        return self.con.list_by_keys(self.table, kvs=kvs, append_sql=append_sql, id_field=id_field, fields=fields)

