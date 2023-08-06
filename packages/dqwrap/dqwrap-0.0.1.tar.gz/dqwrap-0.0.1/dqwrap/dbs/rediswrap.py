import redis
from ..utils.jsonutil import JSONSerializer


class RedisWrap(redis.Redis):

    def __init__(self, *args, **kwargs):
        super(RedisWrap, self).__init__(*args, **kwargs)
        self.json = JSONSerializer

    def set_json(self, key, obj, ex=None, px=None, nx=False, xx=False, keepttl=False):
        return self.set(key, self.json.marshal(obj), ex, px, nx, xx, keepttl)

    def get_json(self, key):
        return self.json.unmarshal(self.get(key))

    def mget_json(self, keys):
        if not keys:
            return
        rs = self.mget(keys)
        return [self.json.unmarshal(r) for r in rs]

    def mset_json(self, objs, key_fn, ex=0):
        if not objs:
            return
        kvs = [None] * len(objs)
        for i, v in enumerate(objs):
            kvs[2 * i] = key_fn(v)
            kvs[2 * i + 1] = self.json.marshal(v)
        self.mset(*kvs)
        if ex > 0:
            for i in range(0, len(kvs), 2):
                self.expire(kvs[i], ex)

    def hget_json(self, name, key):
        return self.json.unmarshal(self.hget(name, key))

    def hset_json(self, name, key, value):
        return self.hset(name, key, self.json.marshal(value))

    def hgetall_json(self, name):
        raw = self.hgetall(name)
        r = {}
        for k, v in raw:
            r[k] = self.json.unmarshal(v)
        return r
