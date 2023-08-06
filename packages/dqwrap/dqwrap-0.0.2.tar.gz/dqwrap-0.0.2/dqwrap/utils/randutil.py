import random, string


def rand_str(n, uppercase=False, digits=True):
    l = string.ascii_lowercase
    if uppercase:
        l += string.ascii_uppercase
    if digits:
        l += string.digits
    return "".join(random.sample(l, n))
