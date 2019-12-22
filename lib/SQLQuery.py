# -*- coding:utf-8 -*-
import pymssql


class MSSQL():
    def __init__(self, dbName):  # 类的构造函数，初始化要连接的数据库名称
        self.db = dbName

    def _TestImport(self):
        print('测试引入成功!')

    def __GetConnect(self):  # 得到数据库连接信息函数， 返回: conn.cursor()
        self.conn = pymssql.connect(
            host='127.0.0.1', user='', password='', database=self.db, charset='utf8')
        cur = self.conn.cursor()  # 将数据库连接信息，赋值给cur。
        if not cur:
            raise(NameError, "连接数据库失败")
        else:
            return cur
    # 执行查询语句,返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

    def ExecQuery(self, sql):  # 执行Sql语句函数，返回结果
        cur = self.__GetConnect()  # 获得数据库连接信息
        cur.execute(sql)  # 执行Sql语句
        resList = cur.fetchall()  # 获得所有的查询结果
        self.conn.close()   # 查询完毕后必须关闭连接
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    '''ms = MSSQL('Library')
    a=ms.ExecQuery('SELECT COUNT(rdType) from TB_ReaderType')
    print(a[0][0])'''
    pass