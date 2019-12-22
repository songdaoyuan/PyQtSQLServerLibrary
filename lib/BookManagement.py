# -*- coding:utf-8 -*-
from lib.SQLQuery import MSSQL


class BookManagement():
    def __init__(self):
        pass

    def BookClassified(self, bkType):
        '''
        分类号		    分类名
        TP			   自动化技术、计算机技术
        TP3			   计算技术、计算机技术
        TP31		   计算机软件
        TP311	       程序设计、软件工程
        TP312		   程序语言、算法语言
        TP311.13	   数据库理论与系统
        TP311.131	   数据库理论
        '''

        return bkType

    def NewBookIn(self, bkInfoList):
        '''
        避免传参过多，将参数打包成一个列表后再传递
        示例：
        BM = BookManagement()
        bkInfoList = ['9787115313980','SQL必知必会','Ben Forta','人民邮电出版社','2013-05-01 00:00:00','9787115313980','TP311.131',0,239,29.00,'畅销全球的数据库入门经典','','在馆']
        BM.NewBookIn(bkInfoList)
        '''
        self.bkCode = bkInfoList[0]
        self.bkName = bkInfoList[1]
        self.bkAuthor = bkInfoList[2]
        self.bkPress = bkInfoList[3]
        self.bkDatePress = bkInfoList[4]
        self.bkISBN = bkInfoList[5]
        self.bkCatalog = bkInfoList[6]
        self.bkLanguage = bkInfoList[7]
        self.bkPages = bkInfoList[8]
        self.bkPrice = bkInfoList[9]
        # 这里略过了bkDateIn,用默认GetDate()函数就行
        self.bkBrief = bkInfoList[10]
        self.bkCover = bkInfoList[11]
        self.bkStatus = bkInfoList[12]
        Library = MSSQL('Library')
        QueryList = Library.ExecQuery('Select bkID from TB_Book')
        if QueryList == []:
            self.bkID = 1
            Library.ExecNonQuery(
                f"INSERT INTO TB_Book VALUES({self.bkID},'{self.bkCode}','{self.bkName}','{self.bkAuthor}','{self.bkPress}','{self.bkDatePress}','{self.bkISBN}','{self.bkCatalog}',{self.bkLanguage},{self.bkPages},{self.bkPrice},GETDATE(),'{self.bkBrief}','{self.bkCover}','{self.bkStatus}')")
        else:
            self.bkID = QueryList[len(QueryList)-1][0]
            self.bkID +=1
            Library.ExecNonQuery(
                f"INSERT INTO TB_Book VALUES({self.bkID},'{self.bkCode}','{self.bkName}','{self.bkAuthor}','{self.bkPress}','{self.bkDatePress}','{self.bkISBN}','{self.bkCatalog}',{self.bkLanguage},{self.bkPages},{self.bkPrice},GETDATE(),'{self.bkBrief}','{self.bkCover}','{self.bkStatus}')")

    def EditBookInfo(self,bkID,EditDict):
        self.bkID = bkID
        self.EditDict = EditDict
        Library = MSSQL('Library')
        Library.ExecNonQuery("UPDATE TB_Book SET bkName = '新的测试名称' WHERE bkID = {self.bkID}")

    def BookDestroyOrSell(self,bkID,bkStatus):
        Library = MSSQL('Library')
        self.bkID = bkID
        self.bkStatus = bkStatus
        bkNowStatus = Library.ExecQuery(f"SELECT bkStatus FROM TB_Book WHERE bkID = {self.bkID}")
        bkNowStatus = bkNowStatus[0][0]
        #借出，遗失
        if bkNowStatus == '在馆':
            Library.ExecNonQuery(f"UPDATE TB_Book SET bkStatus = '{self.bkStatus}' WHERE bkID = {self.bkID}")
            return '执行成功'
        else:
            return '图书已不在馆, 操作无法完成!'
            

if __name__ == '__main__':
    #BM = BookManagement()
    #BM.BookDestroyOrSell(2,'遗失')
    pass
