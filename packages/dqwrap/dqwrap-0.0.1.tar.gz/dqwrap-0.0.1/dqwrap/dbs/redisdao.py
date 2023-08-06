from .basedbwrap import BaseDbWrap
from .rediswrap import RedisWrap
from .basedao import BaseDao


def redis_key(table, *kvs, prefix=""):
    return prefix + table + "/" + "/".join([str(v) for v in kvs])


class RedisDao(BaseDao):
    """
    We should clear cache after any update methods.
    Two type cache in redis:
    1. Cache by primary key: id -> json(obj) ,the redis key: eg.table/id/1
    2. Cache by index: key-values -> ids -> objects, key: table/type/1/state/1 -> ids
    """
    def __init__(self, table: str, con: BaseDbWrap, redis: RedisWrap, ttl=1800, redis_key_prefix=""):
        super(RedisDao, self).__init__(table, con)
        self.redis = redis
        self.ttl = ttl
        self.redis_key_prefix = redis_key_prefix

    def redis_key(self, *args):
        return redis_key(self.table, *args, prefix=self.redis_key_prefix)

    def redis_key_dict(self, dict_args: dict):
        keys = sorted(dict_args.keys())
        args = [None] * (2 * len(keys))
        for i in range(len(keys)):
            args[2 * i] = keys[i]
            args[2 * i + 1] = dict_args[keys[i]]
        return redis_key(self.table, *args, prefix=self.redis_key_prefix)

    def get(self, id, id_field="id", fields=None):
        rk = self.redis_key(id_field, id)
        obj = self.redis.get_json(rk)
        if obj is not None:
            return obj
        obj = super(RedisDao, self).get(id, id_field, fields)
        self.redis.set_json(rk, obj, ex=self.ttl)
        return obj

    def list(self, ids, append_sql="", id_field="id", fields=None):
        rks = [self.redis_key(id_field, v) for v in ids]
        objs = self.redis.mget_json(rks)
        objs = [v for v in objs if v is not None]
        if len(ids) == len(objs):
            return objs
        miss_ids = set(ids) - set([v[id_field] for v in objs])
        miss_objs = super(RedisDao, self).list(miss_ids, append_sql, id_field, fields)
        self.redis.mset_json(miss_objs, lambda v: self.redis_key(id_field, v[id_field]), self.ttl)
        return objs + miss_objs

    def get_by_keys(self, kvs: dict, append_sql: str, id_field="id", fields=None):
        """
        redis_key -> id -> obj
        :param kvs:
        :param append_sql:
        :param id_field:
        :param fields:
        :return:
        """
        rk = self.redis_key_dict(kvs)
        id_value = self.redis.get_json(rk)
        if id_value is not None:
            return self.get(id_value, id_field, fields)
        obj = self.get_by_keys(kvs, append_sql, id_field, fields)
        self.redis.set_json(rk, obj[id_field], ex=self.ttl)
        return obj

    def list_by_keys(self, kvs: dict, append_sql: str, id_field="id", fields=None):
        """
        redis_key ->[id] ->objs
        :param kvs:
        :param append_sql:
        :param id_field:
        :param fields:
        :return:
        """
        rk = self.redis_key_dict(kvs)
        id_values = self.redis.get_json(rk)
        if id_values is not None:
            return self.list(id_values, id_field, fields)
        objs = self.list_by_keys(kvs, append_sql, id_field, fields)
        self.redis.set_json(rk, [obj[id_field] for obj in objs], ex=self.ttl)
        return objs

    def clear_cache(self,id=None, *dicts,id_field="id"):
        rks = []
        if id is not None:
            rks.append(self.redis_key(id_field,id))
        for d in dicts:
            rks.append(self.redis_key_dict(d))
        if len(rks)>0:
            self.redis.delete(*rks)

