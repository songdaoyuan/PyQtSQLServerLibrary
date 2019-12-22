# -*- coding:utf-8 -*-
#此项权限非常危险，仅授权于借书证管理员和系统管理员
#IsReaderAdmin OR IsSystemAdmin == True

from SQLQuery import MSSQL

class ReaderTypeManagement():
    def __init__(self):
        pass

    def EditReaderType(self,rdID,NewrdType):
        '''
        10  教师
        20  本科生
        21  专科生
        30  硕士研究生
        31  博士研究生
        '''
        self.rdID = rdID
        self.NewrdType =NewrdType
        Library = MSSQL('Library')
        Library.ExecNonQuery(f"UPDATE TB_Reader SET rdType={self.NewrdType} WHERE rdID = {self.rdID}")
        
if __name__ == '__main__':
    pass
