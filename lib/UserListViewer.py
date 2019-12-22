# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *
from lib.SQLQuery import MSSQL


class UserListViewer(QWidget):
    def __init__(self):
        super(UserListViewer, self).__init__()
        self.resize(2000, 860)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        # 查询模型
        self.queryModel = None
        # 数据表
        self.tableView = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecord = 0
        # 每页数据数
        self.pageRecord = 10
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        # Hlayout1控件的初始化
        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)
        font = QFont()
        font.setPixelSize(15)
        self.searchEdit.setFont(font)

        self.searchButton = QPushButton("查询")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(font)
        self.searchButton.setIcon(QIcon(QPixmap("./images/search.png")))

        self.condisionComboBox = QComboBox()
        searchCondision = ['按ID查询', '按姓名查询', '按性别查询', '按学历查询', '按系别查询']
        self.condisionComboBox.setFixedHeight(32)
        self.condisionComboBox.setFont(font)
        self.condisionComboBox.addItems(searchCondision)

        self.Hlayout1.addWidget(self.searchEdit)
        self.Hlayout1.addWidget(self.searchButton)
        self.Hlayout1.addWidget(self.condisionComboBox)

        # Hlayout2初始化
        self.jumpToLabel = QLabel("跳转到第")
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        s = "/" + str(self.totalPage) + "页"
        self.pageLabel = QLabel(s)
        self.jumpToButton = QPushButton("跳转")
        self.prevButton = QPushButton("前一页")
        self.prevButton.setFixedWidth(100)
        self.backButton = QPushButton("后一页")
        self.backButton.setFixedWidth(100)

        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.jumpToLabel)
        Hlayout.addWidget(self.pageEdit)
        Hlayout.addWidget(self.pageLabel)
        Hlayout.addWidget(self.jumpToButton)
        Hlayout.addWidget(self.prevButton)
        Hlayout.addWidget(self.backButton)
        widget = QWidget()
        widget.setLayout(Hlayout)
        widget.setFixedWidth(700)
        self.Hlayout2.addWidget(widget)

        # tableView
        # 序号，书名，书号，作者，分类，出版社，出版时间，库存，剩余可借
        #self.db = QSqlDatabase.addDatabase("QODBC",'UserListViewerConn')
        #self.db.setDatabaseName("Driver={Sql Server};Server=localhost;Database=Library;")#Uid=sa;Pwd=123456
        #self.db.open()

        
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.queryModel = QStandardItemModel(12,10)
        self.searchButtonClicked()
        self.tableView.setModel(self.queryModel)

        self.queryModel.setHeaderData(0, Qt.Horizontal, "ID")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "姓名")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "性别")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "学历")
        self.queryModel.setHeaderData(4, Qt.Horizontal, "系别")
        self.queryModel.setHeaderData(5, Qt.Horizontal, "电话号码")
        self.queryModel.setHeaderData(6, Qt.Horizontal, "邮箱")
        self.queryModel.setHeaderData(7, Qt.Horizontal, "注册时间")
        self.queryModel.setHeaderData(8, Qt.Horizontal, "照片")
        self.queryModel.setHeaderData(9, Qt.Horizontal, "借书证状态")
        self.queryModel.setHeaderData(10, Qt.Horizontal, "已借书数量")
        self.queryModel.setHeaderData(11, Qt.Horizontal, "密码")
        self.queryModel.setHeaderData(12, Qt.Horizontal, "权限码")


        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)
        self.searchEdit.returnPressed.connect(self.searchButtonClicked)

    def setButtonStatus(self):
        if(self.currentPage==self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        if(self.currentPage==1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        if(self.currentPage<self.totalPage and self.currentPage>1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)

    # 得到记录数
    def getTotalRecordCount(self):
        #self.queryModel.setQuery("SELECT COUNT(rdID) FROM TB_Reader")
        #self.totalRecord = self.queryModel.rowCount()
        Library = MSSQL('Library')
        countResult = Library.ExecQuery('SELECT COUNT(rdID) FROM TB_Reader')
        if countResult != []:
            self.totalRecord = countResult[0][0]
        return

    # 得到总页数
    def getPageCount(self):
        self.getTotalRecordCount()
        # 上取整
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        return

    # 分页记录查询
    def recordQuery(self, index):
        Library = MSSQL('Library')
        #searchCondision = ['按ID查询', '按姓名查询', '按性别查询', '按学历查询', '按系别查询']
        queryCondition = ""
        conditionChoice = self.condisionComboBox.currentText()
        if (conditionChoice == "按ID查询"):
            conditionChoice = 'rdID'
        elif (conditionChoice == "按姓名查询"):
            conditionChoice = 'rdName'
        elif (conditionChoice == "按性别查询"):
            conditionChoice = 'rdSex'
        elif (conditionChoice == '按学历查询'):
            conditionChoice = 'rdType'
        else:
            conditionChoice = 'rdDept'

        if (self.searchEdit.text() == ""):
            queryCondition = "select * from TB_Reader"
            countQueryCondition = "select COUNT(*) from TB_Reader"
            #self.queryModel.setQuery(queryCondition,self.db)
            #self.totalRecord = self.queryModel.rowCount()
            result = Library.ExecQuery(queryCondition)
            countResult = Library.ExecQuery(countQueryCondition)
            if result != []:
                self.totalRecord = countResult[0][0]
            self.queryModel.removeRows(0,self.queryModel.rowCount())
            for i in range(0,len(result)):
                for j in range(0,len(result[0])):
                    self.queryModel.setItem(i, j, QStandardItem(str(result[i][j])))

            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            queryCondition = (f"select top ({self.pageRecord}) * from TB_Reader  where rdID not in(select top ({index}) rdID from TB_Reader) ORDER BY {conditionChoice}")
            #self.queryModel.setQuery(queryCondition,self.db)
            result = Library.ExecQuery(queryCondition)

            self.queryModel.removeRows(0,self.queryModel.rowCount())
            for i in range(0,len(result)):
                for j in range(0,len(result[0])):
                    self.queryModel.setItem(i, j, QStandardItem(str(result[i][j])))

            self.setButtonStatus()
            return

        # 得到模糊查询条件
        temp = self.searchEdit.text()
        s = f"%{temp}%"
        queryCondition = (f"SELECT * FROM TB_Reader WHERE {conditionChoice} LIKE '%{temp}%' ORDER BY {conditionChoice} ")
        countQueryCondition = (f"SELECT COUNT(*) FROM TB_Reader WHERE {conditionChoice} LIKE '%{temp}%' ORDER BY {conditionChoice} ")
        print(queryCondition)
        #self.queryModel.setQuery(queryCondition,self.db)
        #self.totalRecord = self.queryModel.rowCount()
        result = Library.ExecQuery(queryCondition)
        countResult = Library.ExecQuery(countQueryCondition)
        if result != []:
            self.totalRecord = countResult[0][0]
        self.queryModel.removeRows(0,self.queryModel.rowCount())
        for i in range(0,len(result)):
            for j in range(0,len(result[0])):
                self.queryModel.setItem(i, j, QStandardItem(str(result[i][j])))

        print(self.totalRecord)
        # 当查询无记录时的操作
        #if(self.totalRecord==0):
        if (result == []):
            print(QMessageBox.information(self,"提醒","查询无记录",QMessageBox.Yes,QMessageBox.Yes))
            queryCondition = "select * from TB_Reader"
            countQueryCondition = "Select COUNT(*) from TB_Reader"
            #self.queryModel.setQuery(queryCondition,self.db)
            #self.totalRecord = self.queryModel.rowCount()
            result = Library.ExecQuery(queryCondition)
            countResult = Library.ExecQuery(countQueryCondition)
            if result != []:
                self.totalRecord = countResult[0][0]
            self.queryModel.removeRows(0,self.queryModel.rowCount())
            for i in range(0,len(result)):
                for j in range(0,len(result[0])):
                    self.queryModel.setItem(i, j, QStandardItem(str(result[i][j])))


            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            #queryCondition = ("select * from TB_Book ORDER BY %s  limit %d,%d " % (conditionChoice,index, self.pageRecord))
            queryCondition = (f"select top ({self.pageRecord}) * from TB_Reader  where rdID not in(select top ({index}) rdID from TB_Reader) ORDER BY {conditionChoice}")
            #self.queryModel.setQuery(queryCondition,self.db)
            result = Library.ExecQuery(queryCondition)
            self.queryModel.removeRows(0,self.queryModel.rowCount())
            for i in range(0,len(result)):
                for j in range(0,len(result[0])):
                    self.queryModel.setItem(i, j, QStandardItem(str(result[i][j])))
            self.setButtonStatus()
            return
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        label = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(label)
        queryCondition = (f"select top ({self.pageRecord}) * from TB_Reader  where {conditionChoice} LIKE '{s}' and rdID not in (select top ({index}) rdID from TB_Reader where {conditionChoice} LIKE '{s}') ORDER BY {conditionChoice}")
        #self.queryModel.setQuery(queryCondition,self.db)
        result = Library.ExecQuery(queryCondition)
        self.queryModel.removeRows(0,self.queryModel.rowCount())
        for i in range(0,len(result)):
            for j in range(0,len(result[0])):
                self.queryModel.setItem(i, j, QStandardItem(str(result[i][j])))
        self.setButtonStatus()
        return

    # 点击查询
    def searchButtonClicked(self):
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount()
        s = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向前翻页
    def prevButtonClicked(self):
        self.currentPage -= 1
        if (self.currentPage <= 1):
            self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向后翻页
    def backButtonClicked(self):
        self.currentPage += 1
        if (self.currentPage >= int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 点击跳转
    def jumpToButtonClicked(self):
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if (self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if (self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        index = (self.currentPage - 1) * self.pageRecord
        self.pageEdit.setText(str(self.currentPage))
        self.recordQuery(index)
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = UserListViewer()
    mainMindow.show()
    sys.exit(app.exec_())
