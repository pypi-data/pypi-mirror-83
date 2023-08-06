from urllib import parse
# from DBUtils.PooledDB import PooledDB
from dbutils.pooled_db import PooledDB
from functools import wraps
import redis
from .rediswrap import RedisWrap


# class PoolConfig:
#     type: str
#     user: str
#     password: str
#     host: str
#     port: int
#     db: str
#     charset: str = "utf8"
#     mincached: int = 0
#     maxcached: int = 0
#     maxshared: int = 0
#     maxconnections: int = 0
#     blocking: bool = True
#     maxusage: int = 0
#     setsession: str = None
#     use_unicode: str = False


def parse_db_url(db_url: str):
    """
    :param db_url: eg. mysql://root:123456@localhost:3306?maxcached=100
    :return:
    """
    # r = PoolConfig()
    r = {}
    parts = parse.urlparse(db_url)
    r['schema'] = parts.scheme
    r['user'] = parts.username
    r['password'] = parts.password
    r['host'] = parts.hostname
    r['port'] = parts.port
    # r['db'] = parts.path[1:]
    query = parse.parse_qs(parts.query)
    # param_keys = ("charset")
    params_types = {'mincached': int, 'maxcached': int, 'port': int,
                    'maxshared': int, 'maxconnections': int, 'blocking': bool, 'maxusage': int}
    for k, [v] in query.items():
        if k in params_types:
            if bool == params_types[k]:
                r[k] = False if v == '0' or v.lower() == 'false' else True
                continue
            r[k] = params_types[k](v)
        else:
            r[k] = v
    return r


def create_pool(creator, url) -> PooledDB:
    config = parse_db_url(url)
    # print("config:", config)
    # type = config['schema']
    del config['schema']
    return PooledDB(creator=creator, **config)

class RedisPool:
    def __init__(self , url):
        """
        :param url: redis://[[username]:[password]]@localhost:6379/0
        """
        self.pool = redis.ConnectionPool.from_url(url)

    def connection(self):
        return RedisWrap(connection_pool = self.pool)

def con_injection_factory(dbs , db_wraps):
    """
    datasource injection factory dbs={"con1" :ds1}.
    ds shold have connection(), close() method.

    :param dbs: {"mysql" :datasource},datasource should have create method
    :param wraps: eg.{pymysql: MysqlWrap}
    :return: injection object
    """

    def injection(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cons = []
            varnames = func.__code__.co_varnames
            for varname in varnames:
                if varname in dbs:
                    if varname not in kwargs or not kwargs:
                        con = dbs[varname].connection()  # create new connection from datasource
                        if varname in db_wraps :
                            con = db_wraps[varname](con)
                        kwargs[varname] = con
                        cons.append(con)
            try:
                result = func(*args, **kwargs)
            finally:
                for con in cons:
                    con.close()  # connection should have close method
            return result

        return wrapper

    return injection
