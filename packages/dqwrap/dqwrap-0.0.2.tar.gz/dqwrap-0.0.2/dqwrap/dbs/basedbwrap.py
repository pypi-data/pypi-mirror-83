import typing
from ..utils.collectionutil import pick_values



class BaseDbWrap(object):
    """
    Base database wrap
    """

    def __init__(self, con):
        self.con = con

    def get_raw_con_from_DBUtils(self):
        con = self.con
        while hasattr(con , '_con'):
            con = con._con
        return con

    def cursor(self):
        return self.con.cursor()

    def fetch_dict_rows(self,cursor):
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def query(self, sql: str, args=None):
        with self.cursor() as cursor:
            cursor.execute(sql, args)
            return self.fetch_dict_rows(cursor)

    def query_one(self, sql: str, args=None):
        r = self.query(sql, args)
        if len(r) > 0:
            if len(r) > 1:
                print("warning: BaseDbWrap.query_one the length of result set is " + str(len(r)))
            return r[0]
        return None

    def query_value(self, sql: str, args=None):
        r = self.query_one(sql, args)
        if r is None:
            return None
        if len(r) > 0:
            if len(r) > 1:
                print("warning: BaseDbWrap.query_value there are many value in result.", r)
            for k in r:
                return r[k]

    def get(self, table: str, id, append_sql="", id_field="id", fields=None):
        fields_sql = "*"
        if fields:
            fields_sql = self.sql_fields(fields)
        sql = "select " + fields_sql + " from " + self.escape_table(table) + " where " + self.escape_field(
            id_field) + "=%s "
        sql += append_sql
        print(sql)
        return self.query_one(sql, (id,))

    def list(self, table: str, ids: list, append_sql="", id_field="id", fields=None):
        fields_sql = "*"
        if fields:
            fields_sql = self.sql_fields(fields)
        sql = "select " + fields_sql + " from " + self.escape_table(table) + " where " + self.escape_field(
            id_field) + " in (" \
              + self.sql_holds(len(ids), "%s") + " " + append_sql
        sql += append_sql
        return self.query(sql, tuple(ids))

    def get_by_keys(self, table: str, kvs: dict, append_sql="", id_field="id", fields=None):
        fields_sql = "*"
        if fields:
            fields_sql = self.sql_fields(fields)
        sql = "select " + fields_sql + " from " + self.escape_table(table) + " where " + self.sql_keys_condition(
            kvs.keys()) \
              + " " + append_sql
        sql += append_sql
        return self.query_one(sql, tuple(kvs.values()))

    def list_by_keys(self, table: str, kvs: dict, append_sql="", id_field="id", fields=None):
        fields_sql = "*"
        if fields:
            fields_sql = self.sql_fields(fields)
        sql = "select " + fields_sql + " from " + self.escape_table(table) + " where " + self.sql_keys_condition(
            kvs.keys()) \
              + " " + append_sql
        sql += append_sql
        return self.query(sql, tuple(kvs.values()))

    def execute(self, sql: str, args=None, cb: typing.Callable = None):
        with self.cursor() as cursor:
            cursor.execute(sql, args)
            if cb is not None:
                return cb(cursor)

    def insert(self, table, record: dict, cb: typing.Callable = None, insert_id=True):
        sql = self.make_insert_sql(table, record, insert_id)
        return self.execute(sql, tuple(record.values()), cb)

    def make_insert_sql(self, table: str, record: dict, insert_id=True):
        return "insert into " + self.escape_table(table) + " (" + self.sql_fields(record.keys()) \
               + ") values (" + self.sql_holds(len(record)) + ")"

    def delete(self, table: str, id, id_field="id", cb: typing.Callable = None):
        sql = self.make_delete_sql(table, id, id_field)
        return self.execute(sql, (id,), cb)

    def make_delete_sql(self, table, id, id_field):
        return "delete from " + self.escape_table(table) + " where " + self.escape_field(id_field) + "=%s"

    def update(self, table: str, param: dict, id_field="id", cb: typing.Callable = None):
        id_value = param[id_field]
        del param[id_field]
        sql = self.make_update_sql(table, param, id_field)
        return self.execute(sql, tuple(param.values()) + [id_value], cb)

    def make_update_sql(self, table: str, param: dict, id_field="id"):
        return "update " + self.escape_table(table) + " set " + self.sql_keys_update(
            param.keys()) + " where " + self.escape_field(id_field) + "=%s"

    def make_batch_insert_sql(self, table: str, records, batch=50):
        keys = records[0].keys()
        sql = "insert into " + self.escape_table(table) + " (" + self.sql_fields(keys) + ") values "
        n = len(records) // batch

        batch_sqls = []
        batch_args = []
        batches = [batch] * n
        nkey = len(keys)
        if batch * n != len(records):
            batches.append(len(records) - batch * n)
        for b in range(batches):
            values_sql = ""
            batch_arg = []
            for i in range(b):
                values_sql += "(" + self.sql_holds(nkey) + "),"
                batch_arg += pick_values(records[b * batch + i], keys)
            batch_sqls.append(sql + values_sql[0:len(values_sql) - 1])
            batch_args.append(batch_arg)
        return batch_sqls, batch_args

    def batch_insert(self, table: str, records, batch_size=50):
        if not records or len(records) == 0:
            return
        sqls, args = self.make_batch_insert_sql(table, records, batch_size)
        with self.cursor() as cursor:
            for i, sql in enumerate(sqls):
                cursor.execute(sql, args[i])

    def batch_update(self, table: str, records, id_field="id"):
        if not records or len(records) == 0:
            return
        with self.cursor() as cursor:
            for record in records:
                sql = self.make_update_sql(table, record, id_field)
                cursor.execute(sql, list(record.values()))

    def make_batch_delete_sql(self, table: str, ids, id_field="id"):
        return "delete from " + self.escape_table(table) + " where " + self.escape_field(
            id_field) + " in (" + self.sql_holds(len(ids)) + ")"

    def batch_delete(self, table: str, ids, id_field="id"):
        if not ids or len(ids) == 0:
            return
        sql = self.make_batch_delete_sql(table, ids, id_field)
        return self.execute(sql, ids)

    def set_auto_commit(self, b: bool):
        pass

    def close(self):
        self.con.close()

    def __enter__(self):
        self.set_auto_commit(False)

    def __exit__(self, exc_type, exc_value, exc_trackback):
        if exc_trackback:
            # log.error("rollback transaction")
            # log.error(exc_trackback)
            print(exc_trackback)
            self.con.rollback()
        else:
            # log.info("commit transaction")
            self.con.commit()

    def escape_table(self, table: str):
        return table

    def escape_field(self, field: str):
        return field

    def sql_holds(self, n, hold="%s"):
        """
        :param n: 2
        :param hold: %s
        :return: %s,%s
        """
        return ','.join([hold] * n)

    def sql_keys_condition(self, fields):
        """
        :param keys: eg.['name','age']
        :return: `name`=%s and `age`=%s
        """
        if not dict:
            return "", []
        sql = ""
        for f in fields:
            sql += self.escape_field(f) + "=%s and "
        return sql[:len(sql) - 5]

    def sql_keys_update(self, fields):
        """
        :param keys: eg.['name','age']
        :return: `name`=%s,`age`=%s
        """
        if not dict:
            return "", []
        sql = ""
        for k in fields:
            sql += self.escape_field(k) + '=%s,'
        return sql[:len(sql) - 1]

    def sql_fields(self, fields):
        """
        :param fields: eg.['name','age']
        :return: `name`,`age`
        """
        return ",".join([self.escape_field(f) for f in fields])
