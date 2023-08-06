# class MySQL
import threading

import pymysql


class MySQL(object):
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_port, mysql_db):
        self.db = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port,
                                  db=mysql_db, charset='utf8mb4')
        self.cursor = self.db.cursor()
        self.lock = threading.Lock()

    def create(self, sql_create_table):
        try:
            self.db.ping(reconnect=True)
            self.lock.acquire()
            self.cursor.execute(sql_create_table)
            self.lock.release()
            self.db.commit()
        except Exception as e:
            print(e.args)

    def query(self, sql):
        result = None
        try:
            self.lock.acquire()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.commit()
        except Exception as e:
            print(e.args)
            self.db.rollback()
        finally:
            self.lock.release()
            return result

    def delete(self, sql):
        try:
            self.lock.acquire()
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e.args)
            self.db.rollback()
        finally:
            self.lock.release()

    def save(self, item, table_name):
        self.db.ping(reconnect=True)
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table} ({keys}) values ({values})'.format(table=table_name, keys=keys, values=values)
        try:
            self.lock.acquire()
            if self.cursor.execute(sql, tuple(data.values())):
                self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()
        finally:
            self.lock.release()

    # 保存到mysql
    def write(self, item, table_name):
        self.db.ping(reconnect=True)
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table_name,
                                                                                             keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        try:
            self.lock.acquire()
            if self.cursor.execute(sql, tuple(data.values()) * 2):
                self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()
        finally:
            self.lock.release()

    def close(self):
        self.db.close()


if __name__ == '__main__':
    obj = MySQL()
    if obj:
        print('OK')
        obj.close()
