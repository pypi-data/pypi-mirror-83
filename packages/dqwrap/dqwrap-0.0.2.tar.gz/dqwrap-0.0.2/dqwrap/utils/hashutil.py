import hashlib


def md5(s):
    if str == type(s):
        s = s.encode("utf8")
    return hashlib.md5(s).hexdigest()


def md5file(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def sha1(s):
    if str == type(s):
        s = s.encode("utf8")
    return hashlib.sha1(s).hexdigest()


def sha1file(filename):
    m = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()
