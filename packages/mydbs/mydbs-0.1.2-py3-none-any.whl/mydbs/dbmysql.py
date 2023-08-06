from mydbs import *
from pymysql import connect


class MySql(BaseDB):
    def __init__(self, user='', pwd='', db='', host='localhost', port=3306, charset='utf8'):
        """
        初始化参数
        :param user: 用户名
        :param pwd: 用户密码
        :param db: 使用的数据库名称
        """
        super(MySql, self).__init__()
        self.__host = host
        self.__user = user
        self.__port = port
        self.__pwd = pwd
        self.__db = db
        self.__charset = charset
        self.set_conn(connect(host=self.__host,
                              user=self.__user,
                              port=self.__port,
                              password=self.__pwd,
                              database=self.__db,
                              charset=self.__charset))

        self.set_cursor(self.get_conn().cursor())

        self.set_db_type('mysql')
