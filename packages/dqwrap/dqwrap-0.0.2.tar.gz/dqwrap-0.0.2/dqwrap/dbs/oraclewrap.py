from .basedbwrap import BaseDbWrap


class OracleWrap(BaseDbWrap):
    def __init__(self, con):
        super(OracleWrap, self).__init__(con)


    def set_auto_commit(self, b: bool):
        self.execute("set autocommit " + "on" if b else "off")

    def escape_field(self, field: str):
        i = field.find(".")
        if -1 == i:
            return '"' + field + '"'
        else:
            return field[0:i + 1] + '"' + field[i + 1:] + '"'
    def escape_table(self, table):
        return '"'+table+'"'
