class Error(Exception):
    def __init__(self, state, msg=""):
        super(Error, self).__init__()


class UserError(Error):
    def __init__(self, state, msg=""):
        super(UserError, self).__init__(state, msg)


DB_ERROR = 20
