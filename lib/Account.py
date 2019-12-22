# -*- coding:utf-8 -*-

from lib.SQLQuery import MSSQL

class Account(MSSQL):
    def __init__(self):
        pass
       
    def Login(self,id,pwd):
        self.id = id
        self.pwd = pwd
        result = []
        Library = MSSQL('Library')
        rdAdminRolesCodeAndrdStatus = Library.ExecQuery(f"SELECT rdAdminRoles,rdStatus FROM TB_Reader WHERE rdID={self.id} AND rdPwd='{self.pwd}'")
        if rdAdminRolesCodeAndrdStatus == []:
            print('输入的账号密码有误!')
            result.append(False)
            return result
        elif rdAdminRolesCodeAndrdStatus[0][1] !='有效':
            print('借书证挂失或被注销，无效登录!')
            result.append(False)
            return result
        else:
            print('登录成功!')
            rdAdminRolesCode = rdAdminRolesCodeAndrdStatus[0][0]
            result.append(True)
            PermissionCodeList = self.rdAdminRoles(rdAdminRolesCode)
            result.append(PermissionCodeList)
            return result
            
    
    def rdAdminRoles(self,rdAdminRolesCode):
        '''
        SystemAdmin  = 8   系统管理
        BorrowAdmin  = 4   借阅管理
        BookAdmin    = 2   图书管理
        ReaderAdmin  = 1   借书证管理
        '''
        IsBookAdmin=IsBorrowAdmin=IsSystemAdmin=IsReaderAdmin = False
        if rdAdminRolesCode == 15:
            IsBookAdmin=IsBorrowAdmin=IsSystemAdmin=IsReaderAdmin = True
        elif rdAdminRolesCode == 14:
            IsBookAdmin=IsBorrowAdmin=IsSystemAdmin = True
        elif rdAdminRolesCode == 13:
            IsBorrowAdmin=IsSystemAdmin=IsReaderAdmin = True
        elif rdAdminRolesCode == 12:
            IsBorrowAdmin=IsSystemAdmin=True
        elif rdAdminRolesCode == 11:
            IsBookAdmin=IsSystemAdmin=IsReaderAdmin = True
        elif rdAdminRolesCode == 10:
            IsBookAdmin=IsSystemAdmin= True
        elif rdAdminRolesCode == 9:
            IsSystemAdmin=IsReaderAdmin = True
        elif rdAdminRolesCode == 8:
            IsSystemAdmin = True
        elif rdAdminRolesCode == 7:
            IsBookAdmin=IsBorrowAdmin=IsReaderAdmin = True
        elif rdAdminRolesCode == 6:
            IsBookAdmin=IsBorrowAdmin = True
        elif rdAdminRolesCode == 5:
            IsBorrowAdmin=IsReaderAdmin = True
        elif rdAdminRolesCode == 4:
            IsBorrowAdmin = True
        elif rdAdminRolesCode == 3:
            IsBookAdmin=IsReaderAdmin = True
        elif rdAdminRolesCode == 2:
            IsBookAdmin = True
        elif rdAdminRolesCode == 1:
            IsReaderAdmin = False
        
        return [IsBookAdmin,IsBorrowAdmin,IsSystemAdmin,IsReaderAdmin]

    def ChangePwd(self,NewPwd):
        self.NewPwd = NewPwd
        Library = MSSQL('Library')
        Library.ExecNonQuery(f"UPDATE TB_Reader SET rdPwd='{self.NewPwd}' WHERE rdID={self.id}")


if __name__ == '__main__':
    #实例化自身的测试代码放在这里
    ac = Account()
    r= ac.Login('1','sdy2000317421')
    print(r)
    #ac.ChangePwd('sdy2000317421')