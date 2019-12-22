import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *

from lib.SQLQuery import MSSQL
from lib.ReaderManagement import ReaderManagement

class addLibraryCard(QDialog):
    add_LibraryCard_success_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(addLibraryCard, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("办理借书证")

    def setUpUI(self):
        typeList = ['教师','本科生','专科生','博士研究生','硕士研究生']
        rdDeptList = ["CS","PE","ART","ECONOMICS","GEOGRAPHY","MEDICINE","MATH","Philosophy"]
        self.resize(350, 700)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
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
        self.titleLable = QLabel('信息录入')
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
        self.addLibraryCardButton = QPushButton("办理")

        # lineEdit控件
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
        self.statusComboBox.addItems(['有效','挂失','注销'])
        #----------------------------------------------
        self.passwordEdit = QLineEdit()
        self.adminRolesEdit = QLineEdit()
        self.nameEdit.setMaxLength(10)
        self.phoneEdit.setMaxLength(11)
        #self.phoneEdit.setValidator(QIntValidator())

        # 添加进formlayout
        self.layout.addRow("", self.titleLable)
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
        self.layout.addRow("", self.addLibraryCardButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titleLable.setFont(font)
        font.setPixelSize(14)
        self.nameLable.setFont(font)
        self.sexLabel.setFont(font)
        self.typeLabel.setFont(font)
        self.deptLabel.setFont(font)
        self.phoneLabel.setFont(font)
        self.emailLable.setFont(font)
        self.statusLabel.setFont(font)
        self.passwordLabel.setFont(font)
        self.adminRolesLable.setFont(font)

        self.nameEdit.setFont(font)
        #self.typeComboBox.setFont(font)
        self.phoneEdit.setFont(font)
        self.emailEdit.setFont(font)
        self.photoEdit.setFont(font)
        self.passwordEdit.setFont(font)
        self.adminRolesEdit.setFont(font)

        self.statusComboBox.setCurrentText('有效')
        self.passwordEdit.setText('123')

        # button设置
        font.setPixelSize(16)
        self.addLibraryCardButton.setFont(font)
        self.addLibraryCardButton.setFixedHeight(32)
        self.addLibraryCardButton.setFixedWidth(140)

        # 设置间距
        self.titleLable.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.addLibraryCardButton.clicked.connect(self.addLibraryCardButtonCicked)

    def addLibraryCardButtonCicked(self):
        rdTypeDIct = {'教师':10,'本科生':20,'专科生':21,'博士研究生':30,'硕士研究生':31}
        #rdInfoList = ['朱晨光','男',21,'CS','13349745060','841102344@qq.com','','有效',0,'123',15]
        
        rdName = self.nameEdit.text()
        rdSex = self.sexComboBox.currentText()
        rdType = self.typeComboBox.currentText()
        rdType = rdTypeDIct[rdType]
        print(rdType)
        rdDept = self.deptComboBox.currentText()
        rdPhone = self.phoneEdit.text()
        rdEmail = self.emailEdit.text()
        rdPhoto = self.photoEdit.text()
        rdStatus = self.statusComboBox.currentText()
        rdPassword = self.passwordEdit.text()
        rdAdminRoles = self.adminRolesEdit.text()
        
        Library = MSSQL('Library')
        result = Library.ExecQuery(f"SELECT * FROM TB_Reader WHERE rdName = '{rdName}' AND rdPhone = '{rdPhone}'")
        if (rdName=='' or rdPhone==''):
            print(QMessageBox.warning(self, "警告", "关键字段为空，添加失败", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            rdInfoList = [rdName,rdSex,rdType,rdDept,rdPhone,rdEmail,rdPhoto,rdStatus,0,rdPassword,rdAdminRoles]
            RM = ReaderManagement()
            result = RM.NewLibraryCard(rdInfoList)
            print(QMessageBox.warning(self, "通知", result, QMessageBox.Yes, QMessageBox.Yes))
            self.clearEdit()
            
    def clearEdit(self):
        self.nameEdit.clear()
        self.phoneEdit.clear()
        self.emailEdit.clear()
        self.passwordEdit.clear()
        self.adminRolesEdit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = addLibraryCard()
    mainMindow.show()
    sys.exit(app.exec_())
