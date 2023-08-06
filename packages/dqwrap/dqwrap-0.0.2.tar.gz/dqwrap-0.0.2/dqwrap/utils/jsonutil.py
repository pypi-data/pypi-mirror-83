import json
import datetime as dt
from datetime import datetime, date
from dqwrap.utils.collectionutil import object2dict
from .timeutil import SYSTEM_TIMEZONE


class JSON:
    def marshal(self, obj):
        return None

    def unmarshal(self, s):
        return None


class JSONSerializer(JSON):
    def marshal(self, obj):
        return dumps(obj)

    def unmarshal(self, s):
        return loads(s)


class JSONable(object):
    def marshal(self):
        return object2dict(self)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            if obj.tzinfo is None:
                return obj.replace(tzinfo=SYSTEM_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S%z')
            else:
                return obj.strftime('%Y-%m-%d %H:%M:%S%z')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, dt.time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, JSONable):
            return obj.marshal()
        else:
            return super(JSONEncoder, self).default(obj)


def dumps(obj):
    return json.dumps(obj, cls=JSONEncoder)


def loads(s):
    if s is None:
        return None
    return json.loads(s)
