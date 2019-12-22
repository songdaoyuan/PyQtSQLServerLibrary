# -*- coding:utf-8 -*-
#此项权限非常危险，仅授权于借书证管理员和系统管理员
#IsReaderAdmin OR IsSystemAdmin == True`

from lib.SQLQuery import MSSQL
'''
1.办理借书证
2.变更借书证
3.解除挂失*   ---->变更借书证状态
4.补办借书证*
5.注销借书证*
6.批量办理新生借书证*
'''
class ReaderManagement():
    def __init__(self):
        pass

    def NewLibraryCard(self,rdInfoList):
        '''
        [rdName]
        [rdSex]
        [rdType]
        [rdDept]
        [rdPhone]
        [rdEmail]
        [rdPhoto]
        [rdStatus]
        [rdBorrowQty]
        [rdPwd]
        [rdAdminRoles]
        '''
        self.rdName = rdInfoList[0]
        self.rdSex = rdInfoList[1]
        self.rdType = rdInfoList[2]
        self.rdDept = rdInfoList[3]
        self.rdPhone = rdInfoList[4]
        self.rdEmail = rdInfoList[5]
        self.rdPhoto = rdInfoList[6]
        self.rdStatus = rdInfoList[7]
        self.rdBorrowQty = rdInfoList[8]
        self.rdPwd = rdInfoList[9]
        self.rdAdminRoles = rdInfoList[10]
        Library = MSSQL('Library')
        result = Library.ExecQuery(f"SELECT * FROM TB_Reader WHERE rdName='{self.rdName}' AND rdType={self.rdType} AND rdDept = '{self.rdDept}'")
        if not result == []:
            return '该借书证已存在!'
        else:
            result = Library.ExecQuery("SELECT rdID FROM TB_Reader")
            self.rdID = result[len(result)-1][0] + 1
            a = f"INSERT INTO TB_Reader VALUES({self.rdID},'{self.rdName}','{self.rdSex}',{self.rdType},'{self.rdDept}','{self.rdPhone}','{self.rdEmail}',GETDATE(),'{self.rdPhoto}','{self.rdStatus}',{self.rdBorrowQty},'{self.rdPwd}',{self.rdAdminRoles})"
            Library.ExecNonQuery(f"INSERT INTO TB_Reader VALUES({self.rdID},'{self.rdName}','{self.rdSex}',{self.rdType},'{self.rdDept}','{self.rdPhone}','{self.rdEmail}',GETDATE(),'{self.rdPhoto}','{self.rdStatus}',{self.rdBorrowQty},'{self.rdPwd}',{self.rdAdminRoles})")
            return '借书证添加成功'
    def EditLibraryCard(self):
        pass

    def CancelLibraryCardReport(self):
        pass

    def DestoryLibraryCard(self):
        pass

    def BatchNewLibraryCard(self):
        pass

if __name__ == '__main__':
    '''rm = ReaderManagement()
    rdInfoList = ['朱晨光','男',21,'CS','13349745060','841102344@qq.com','','有效',0,'123',15]
    rm.NewLibraryCard(rdInfoList)'''
    pass