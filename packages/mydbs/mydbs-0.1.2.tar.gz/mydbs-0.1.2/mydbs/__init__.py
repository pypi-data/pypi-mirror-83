from inspect import ismethod
from logging import getLogger, FileHandler, Formatter

logger = getLogger(__name__)
handler = FileHandler("error.log", encoding='utf-8')
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def str_pop(s='', pos=0):
    list_from_str = list(s)
    list_from_str.pop(pos)
    return ''.join(list_from_str)


class BaseDB:
    def __init__(self):
        self.__db_type = None
        self.__conn = None
        self.__cursor = None

    def __getattribute__(self, item):
        """建议对item进行一下判断，不要全局增加"""
        class_member = super().__getattribute__(item)
        if ismethod(class_member):
            def wrapper(*args, **kwargs):
                try:
                    result = class_member(*args, **kwargs)
                except Exception as e:
                    func_class_name = class_member.__qualname__
                    logger.error('Engine: '+self.__db_type+'\n'+'Error in ' + func_class_name + '\n' + str(e))
                    result = 1
                return result
            return wrapper
        else:
            return class_member

    def set_db_type(self, db_type):
        if db_type not in ['mysql', 'sqlite', 'mongodb', 'oracle']:
            raise Exception('unidentified database type')
        self.__db_type = db_type

    def get_db_type(self):
        return self.__db_type

    def set_conn(self, conn):
        self.__conn = conn

    def get_conn(self):
        return self.__conn

    def set_cursor(self, cursor):
        self.__cursor = cursor

    def get_cursor(self):
        return self.__cursor

    def close(self):
        """
        释放进程
        :return: None
        """
        self.__cursor.close()
        self.__conn.close()

    def show_databases(self):
        """
        列出所有现存数据库
        :return: 数据库名称列表
        """
        sql = 'SHOW DATABASES;'
        self.__cursor.execute(sql)
        return [ele[0] for ele in self.__cursor.fetchall()]

    def use_database(self, db_name=''):
        """
        切换数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = 'USE %s;'
        return self.__cursor.execute(sql % db_name)

    def create_database(self, db_name=''):
        """
        创建新数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = 'CREATE DATABASE %s;'
        return self.__cursor.execute(sql % db_name)

    def drop_database(self, db_name=''):
        """
        删除数据库
        :param db_name:数据库名称
        :return: 0为执行成功
        """
        sql = 'DROP DATABASE %s;'
        return self.__cursor.execute(sql % db_name)

    def show_tables(self):
        """
        列出数据库中所有现存表
        :return: 0为执行成功
        """
        sql = 'SHOW TABLES;'
        self.__cursor.execute(sql)
        return [ele[0] for ele in self.__cursor.fetchall()]

    def desc_table(self, table_name=''):
        """
        列出表的结构
        :param table_name: 表名称
        :return: 表的结构表
        """
        sql = 'DESC %s;'
        self.__cursor.execute(sql % table_name)
        return [ele for ele in self.__cursor.fetchall()]

    def create_table(self, table_name='', pri_key_name='', engine='InnoDB', charset='utf8', **item_type_dict):
        """
        创建新表
        :param table_name: 数据表名称
        :param pri_key_name: 主键名称
        :param engine: 数据库引擎
        :param charset: 数据库字符集
        :param item_type_dict: 关键字与数据类型键值对字典
        :return: 0为执行成功
        """
        item_type_str = ''
        sql_mysql = 'CREATE TABLE IF NOT EXISTS %s (%s)ENGINE=%s DEFAULT CHARSET=%s;'
        sql_sqlite = 'CREATE TABLE IF NOT EXISTS %s (%s);'
        for k, v in item_type_dict.items():
            if k != pri_key_name:
                item_type_str += k + ' ' + v + ' NOT NULL,'
            else:
                if self.__db_type == 'mysql':
                    item_type_str += k + ' ' + v + ' PRIMARY KEY AUTO_INCREMENT NOT NULL, '
                elif self.__db_type == 'sqlite':
                    item_type_str += k + ' ' + v + ' PRIMARY KEY AUTOINCREMENT NOT NULL, '
        item_type_str = item_type_str.strip(',')
        if self.__db_type == 'mysql':
            return self.__cursor.execute(sql_mysql % (table_name, item_type_str, pri_key_name, engine, charset))
        elif self.__db_type == 'sqlite':
            return self.__cursor.execute(sql_sqlite % (table_name, item_type_str))

    def truncate_table(self, table_name):
        sql = 'TRUNCATE TABLE %s'
        return self.__cursor.execute(sql % table_name)

    def drop_table(self, table_name=''):
        """
        删除数据表
        :param table_name: 数据表名称
        :return: 执行成功返回1
        """
        sql = 'DROP TABLE %s;'
        self.__cursor.execute(sql % table_name)
        return 1

    def select(self, table_name='', columns='*'):
        """
        选择
        :param table_name: 数据表名称
        :param columns: 选择的关键字
        :return: 所选择的结果
        """
        sql = 'SELECT %s FROM %s;'
        self.__cursor.execute(sql % (columns, table_name))
        return [ele for ele in self.__cursor.fetchall()]

    def select_where(self, columns='*', table_name='', where_clause=''):
        """
        带条件的选择
        注意：where句如果赋值字符串需要打引号
        :param columns: 选择的关键字
        :param table_name: 数据表名称
        :param where_clause: where子句
        :return: 所选择的结果
        """
        sql = 'SELECT %s FROM %s WHERE %s;'

        self.__cursor.execute(sql % (columns, table_name, where_clause))
        return [ele for ele in self.__cursor.fetchall()]

    def select_where_file(self, table_name='', column_name='', file_name='', where_clause=''):
        """
        将数据库文件数据写入文件
        注意：where句如果赋值字符串需要打引号
        :param table_name: 数据表名称
        :param column_name: 所选列名称
        :param file_name: 文件路径
        :param where_clause: where子句
        :return: 执行成功返回1
        """
        f = open(file_name, 'wb')
        content = self.select_where(column_name, table_name, where_clause)[0][0]
        f.write(eval(content.decode('utf-8')))
        f.close()
        return 1

    def insert(self, table_name='', fields=tuple(), values=tuple()):
        """
        最后一行之后插入数据
        :param table_name: 数据表名称
        :param fields: 关键字元组
        :param values: 对应的值元组
        :return: 0表示执行成功
        """
        sql = 'INSERT INTO %s %s VALUES %s;'

        str_fields = str(fields).replace('\'', '')
        str_values = str(values)
        if len(fields) == 1:
            str_fields = str_pop(str_fields, -2)
            str_values = str_pop(str_values, -2)
        print(sql % (table_name, str_fields, str_values))
        if self.__cursor.execute(sql % (table_name, str_fields, str_values)):
            self.__conn.commit()
            return 1
        else:
            return 0

    def update(self, table_name='', set_clause='', where_clause=''):
        """
        更新
        :param table_name: 数据表名称
        :param set_clause: set子句
        :param where_clause: where子句
        :return: 执行成功返回1
        """
        sql = 'UPDATE %s SET %s WHERE %s'
        print(sql % (table_name, set_clause, where_clause))
        self.__cursor.execute(sql % (table_name, set_clause, where_clause))
        self.__conn.commit()
        return 1

    def update_file(self, table_name='', column_name='', file_name='', where_clause=''):
        f = open(file_name, 'rb')
        content = repr(str(f.read()))
        f.close()
        self.update(table_name, column_name + ' = ' + content, where_clause)

    def delete(self, table_name='', where_clause=''):
        """
        删除数据表任意一行
        :param table_name: 数据表名称
        :param where_clause: where子句
        :return: 执行成功返回1
        """
        sql = 'DELETE FROM %s WHERE %s'

        self.__cursor.execute(sql % (table_name, where_clause))
        self.__conn.commit()
        return 1

    def alter(self, table_name='', mode='', content=''):
        """
        修改
        :param table_name: 数据表名称
        :param mode: 模式选择
        :param content: 修改内容
        :return: 执行成功返回1
        """
        sql = ''
        if mode == 'drop':
            sql = 'ALTER TABLE %s DROP %s'
        elif mode == 'add':
            sql = 'ALTER TABLE %s ADD %s'
        elif mode == 'modify':
            sql = 'ALTER TABLE %s MODIFY %s'
        elif mode == 'change':
            sql = 'ALTER TABLE %s CHANGE %s'
        self.__cursor.execute(sql % (table_name, content))
        self.__conn.commit()
        return 1

    def pri_key_reset(self, table_name='', pri_key_name=''):
        """
        重置数据标主键
        :param table_name: 数据表名称
        :param pri_key_name: 主键名称
        :return: 执行成功返回1
        """
        self.alter(table_name, 'drop', pri_key_name)
        self.alter(table_name, 'add', pri_key_name + ' INT(10) AUTO_INCREMENT PRIMARY KEY FIRST')
        return 1
