from mydbs import *
from sqlite3 import connect


class Sqlite(BaseDB):
    def __init__(self, db):
        super(Sqlite, self).__init__()

        self.__db = db
        self.set_conn(connect(self.__db))

        self.set_cursor((self.get_conn().cursor()))

        self.set_db_type('sqlite')
