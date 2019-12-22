import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *

from lib.SQLQuery import MSSQL
from lib.ReaderManagement import ReaderManagement

class destoryLibraryCard(QDialog):
    destory_LibraryCard_successful_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(destoryLibraryCard, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("注销借书证")

    def setUpUI(self):
        typeList = ['教师','本科生','专科生','博士研究生','硕士研究生']
        rdDeptList = ["CS","PE","ART","ECONOMICS","GEOGRAPHY","MEDICINE","MATH","Philosophy"]
        self.resize(350, 700)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.idLable = QLabel("用户ID:")
        self.titleLable = QLabel('删除用户')
        self.nameLable = QLabel("姓名:")
        self.sexLabel = QLabel("性别:")
        self.typeLabel = QLabel("学历:")
        self.deptLabel = QLabel("系别:")
        self.phoneLabel = QLabel("电话号码:")
        self.emailLable = QLabel("邮箱:")
        self.photoLabel = QLabel("照片:")
        self.statusLabel = QLabel("状态:")
        self.passwordLabel = QLabel('密码:')
        self.adminRolesLable = QLabel('权限:')

        # button控件
        self.destoryLibraryCardButton = QPushButton("确定")

        # lineEdit控件
        self.idEdit = QLineEdit()
        self.nameEdit = QLineEdit()
        self.sexComboBox = QComboBox()
        self.sexComboBox.addItems(['男','女'])
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItems(typeList)
        #----------------------------------------------
        self.deptComboBox = QComboBox()
        self.deptComboBox.addItems(rdDeptList)
        #----------------------------------------------
        self.phoneEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.photoEdit = QLineEdit()
        #----------------------------------------------
        self.statusComboBox = QComboBox()
        self.statusComboBox.addItems(['注销'])
        #----------------------------------------------
        self.passwordEdit = QLineEdit()
        self.adminRolesEdit = QLineEdit()
        self.nameEdit.setMaxLength(10)
        self.phoneEdit.setMaxLength(11)
        #self.phoneEdit.setValidator(QIntValidator())

        # 添加进formlayout
        self.layout.addRow("", self.titleLable)
        self.layout.addRow(self.idLable, self.idEdit)
        self.layout.addRow(self.nameLable, self.nameEdit)
        self.layout.addRow(self.sexLabel, self.sexComboBox)
        self.layout.addRow(self.typeLabel, self.typeComboBox)
        self.layout.addRow(self.deptLabel, self.deptComboBox)
        self.layout.addRow(self.phoneLabel, self.phoneEdit)
        self.layout.addRow(self.emailLable, self.emailEdit)
        self.layout.addRow(self.photoLabel, self.photoEdit)
        self.layout.addRow(self.statusLabel, self.statusComboBox)
        self.layout.addRow(self.passwordLabel, self.passwordEdit)
        self.layout.addRow(self.adminRolesLable, self.adminRolesEdit)
        self.layout.addRow("", self.destoryLibraryCardButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titleLable.setFont(font)
        font.setPixelSize(14)
        self.idLable.setFont(font)
        self.nameLable.setFont(font)
        self.sexLabel.setFont(font)
        self.typeLabel.setFont(font)
        self.deptLabel.setFont(font)
        self.phoneLabel.setFont(font)
        self.emailLable.setFont(font)
        self.statusLabel.setFont(font)
        self.passwordLabel.setFont(font)
        self.adminRolesLable.setFont(font)

        self.idEdit.setFont(font)
        self.nameEdit.setFont(font)
        self.nameEdit.setStyleSheet("background-color:#363636")
        #self.typeComboBox.setFont(font)
        self.phoneEdit.setFont(font)
        self.phoneEdit.setStyleSheet("background-color:#363636")
        self.emailEdit.setFont(font)
        self.emailEdit.setStyleSheet("background-color:#363636")
        self.photoEdit.setFont(font)
        self.phoneEdit.setStyleSheet("background-color:#363636")
        self.passwordEdit.setFont(font)
        self.passwordEdit.setStyleSheet("background-color:#363636")
        self.adminRolesEdit.setFont(font)
        self.adminRolesEdit.setStyleSheet("background-color:#363636")

        self.statusComboBox.setCurrentText('注销')

        # button设置
        font.setPixelSize(16)
        self.destoryLibraryCardButton.setFont(font)
        self.destoryLibraryCardButton.setFixedHeight(32)
        self.destoryLibraryCardButton.setFixedWidth(140)

        # 设置间距
        self.titleLable.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.destoryLibraryCardButton.clicked.connect(self.destoryLibraryCardButtonCicked)
        self.idEdit.textChanged.connect(self.idEditChanged)
    def idEditChanged(self):
        rdID = self.idEdit.text()
        if (rdID == ""):
            self.nameEdit.clear()
            self.phoneEdit.clear()
            self.emailEdit.clear()
            self.passwordEdit.clear()
        # 查询对应ID，如果存在就更新form
        Library = MSSQL('Library')
        self.result = Library.ExecQuery(f"SELECT * FROM TB_Reader WHERE rdId='{rdID}'")
        if not self.result == []:
            rdTypeDIct = {10:'教师',20:'本科生',21:'专科生',30:'博士研究生',31:'硕士研究生'}
            self.nameEdit.setText(self.result[0][1])
            self.sexComboBox.setCurrentText(self.result[0][2])
            self.typeComboBox.setCurrentText(rdTypeDIct[self.result[0][3]])
            self.deptComboBox.setCurrentText(self.result[0][4])
            self.phoneEdit.setText(self.result[0][5])
            self.emailEdit.setText(self.result[0][6])
            self.passwordEdit.setText(self.result[0][11])
            self.adminRolesEdit.setText(str(self.result[0][12]))
        return

    def destoryLibraryCardButtonCicked(self):
        rdTypeDIct = {'教师':10,'本科生':20,'专科生':21,'博士研究生':30,'硕士研究生':31}

        rdID = self.idEdit.text()
        rdName = self.nameEdit.text()
        rdSex = self.sexComboBox.currentText()
        rdType = self.typeComboBox.currentText()
        rdType = rdTypeDIct[rdType]
        rdDept = self.deptComboBox.currentText()
        rdPhone = self.phoneEdit.text()
        rdEmail = self.emailEdit.text()
        rdPhoto = self.photoEdit.text()
        rdStatus = self.statusComboBox.currentText()
        rdPassword = self.passwordEdit.text()
        rdAdminRoles = self.adminRolesEdit.text()
        rdAdminRoles = int(rdAdminRoles)
        
        Library = MSSQL('Library')
        result = Library.ExecQuery(f"SELECT * FROM TB_Reader WHERE rdID = '{rdID}'")
        BorrowResult = Library.ExecQuery(f"SELECT ldDateRetPlan FROM TB_Borrow WHERE rdID={rdID} AND IsHasReturn=0")
        if result == []:
            print(QMessageBox.warning(self, "警告", "该用户不存在，请检查ID输入!", QMessageBox.Yes, QMessageBox.Yes))
            self.clearEdit()
            return
        elif BorrowResult !=[]:
            print(QMessageBox.warning(self, "警告", "用户存在为归还图书，请归还所有图书后再注销!", QMessageBox.Yes, QMessageBox.Yes))
        else:
            Library.ExecNonQuery(f"UPDATE TB_Reader SET rdName='{rdName}',rdSex='{rdSex}',rdType={rdType},rdDept='{rdDept}',rdPhone='{rdPhone}',rdPhoto='{rdPhoto}',rdStatus='注销',rdPwd='{rdPassword}',rdAdminRoles='{rdAdminRoles}' WHERE rdID = {rdID}")
            print(QMessageBox.warning(self, "提示", "借书证注销成功!", QMessageBox.Yes, QMessageBox.Yes))
            self.clearEdit()
            return
    def clearEdit(self):
        self.idEdit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = destoryLibraryCard()
    mainMindow.show()
    sys.exit(app.exec_())
