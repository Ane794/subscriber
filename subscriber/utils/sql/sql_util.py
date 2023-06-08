import importlib


class SqlUtil:
    """ 数据库的工具类 """

    def __init__(self, **kwargs):
        # 连接数据库.
        self.kwargs: dict[str] = kwargs
        self.db = importlib.import_module(self.kwargs.pop('engine', 'sqlite3'))
        if self.db == 'sqlite3':
            _database = self.kwargs.pop('database', 'db/subscriber.sqlite')
            self.kwargs['database'] = _database
        self.db_conn = None
        self.cursor = None

        # `self.insert`, `self.delete` 与 `self.update` 的实现相同.
        self.insert = self.update
        self.delete = self.update

    def connect(self):
        self.db_conn = self.db.connect(**self.kwargs)
        self.cursor = self.db_conn.cursor()

    def update(self, sql: str):
        """
        修改数据库中的数据.
        :param sql: SQL 查询语句
        """
        try:
            self.connect()
            self.cursor.execute(sql)
            self.db_conn.commit()
        except self.db.Error as error:
            self.db_conn.rollback()
            raise error
        finally:
            self.db_conn.close()

    def fetchone(self, sql: str):
        """
        查询数据库的下一个结果.
        :param sql: SQL 查询语句
        :return: 结果集
        """
        try:
            self.connect()
            self.cursor.execute(sql)
            _result = self.cursor.fetchone()
        except self.db.Error as error:
            self.db_conn.rollback()
            raise error
        else:
            return _result
        finally:
            self.db_conn.close()

    def fetchall(self, sql: str):
        """
        查询数据库的所有结果.
        :param sql: SQL 查询语句
        :return: 结果集
        """
        try:
            self.connect()
            self.cursor.execute(sql)
            _result = self.cursor.fetchall()
        except self.db.Error as error:
            self.db_conn.rollback()
            raise error
        else:
            return _result
        finally:
            self.db_conn.close()

    def res_to_dict(self, res: tuple | dict) -> dict:
        """
        将查询结果转换成 `dict`.
        :param res: 查询结果
        :return: 转换后的查询结果
        """
        if isinstance(res, tuple):
            return {
                self.cursor.description[i][0]: res[i]
                for i in range(0, len(self.cursor.description))
            }
        return res
