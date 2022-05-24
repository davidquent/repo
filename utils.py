import logging
import traceback


# 连接mysql
class MysqlCon:
    import threading
    _instance = None
    _lock = threading.RLock()

    # def __init__(self, user='david', pwd='david', database='erp'):
    def __init__(self, **kwargs):
        import pymysql
        self._con = pymysql.connect(**kwargs)
        self._cursor = self._con.cursor()
        self._result = None
        self._rows = None
        self.con = self._con

    def __new__(cls, *args, **kwargs):

        if cls._instance:
            return cls._instance

        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
            return cls._instance

    def executesql(self, mysql: str, args=None) -> tuple:
        try:
            # print(mysql)
            self._rows = self._cursor.execute(mysql, args)
            self._con.commit()
            self._result = self._cursor.fetchall()
        except Exception as e:
            logging.exception(traceback.format_exc(e))
            self._con.rollback()
            self._result = ()
            print(e)
        return self._rows, self._result



