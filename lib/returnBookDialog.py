import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *
from lib.SQLQuery import MSSQL
import datetime


class returnBookDialog(QDialog):
    return_book_success_signal=pyqtSignal()
    def __init__(self, StudentId, StudentName, parent=None):
        super(returnBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.studentName = StudentName
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("归还书籍")

    def setUpUI(self):
        BookCategory = ["自动化技术/计算机技术","计算技术/计算机技术","计算机软件","程序设计/软件工程","程序语言/算法语言","数据库理论与系统","数据库理论"]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.returnStudentLabel = QLabel("还 书 人:")
        self.returnStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  归还书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authorNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")

        # button控件
        self.returnBookButton = QPushButton("确认归还")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authorNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTimeEdit = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(6)
        self.authorNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.returnStudentLabel, self.returnStudentIdLabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authorNameLabel, self.authorNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTimeEdit)
        self.layout.addRow("", self.returnBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.returnStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.returnStudentLabel.setFont(font)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authorNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)

        self.bookNameEdit.setFont(font)
        self.bookNameEdit.setReadOnly(True)
        self.bookNameEdit.setStyleSheet("background-color:#363636")
        self.bookIdEdit.setFont(font)
        self.authorNameEdit.setFont(font)
        self.authorNameEdit.setReadOnly(True)
        self.authorNameEdit.setStyleSheet("background-color:#363636")
        self.publisherEdit.setFont(font)
        self.publisherEdit.setReadOnly(True)
        self.publisherEdit.setStyleSheet("background-color:#363636")
        self.publishTimeEdit.setFont(font)
        self.publishTimeEdit.setStyleSheet("background-color:#363636")
        self.categoryComboBox.setFont(font)
        self.categoryComboBox.setStyleSheet("background-color:#363636")

        # button设置
        font.setPixelSize(16)
        self.returnBookButton.setFont(font)
        self.returnBookButton.setFixedHeight(32)
        self.returnBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.returnBookButton.clicked.connect(self.returnButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)

    def returnButtonClicked(self):
        # 获取书号，书号为空或并未借阅，则弹出错误
        BookId = self.bookIdEdit.text()
        rdID = int(self.studentId)
        # BookId为空的处理
        if (BookId == ""):
            print(QMessageBox.warning(self, "警告", "你所要还的书不存在，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库
        Library = MSSQL('Library')
        BorrowResult = Library.ExecQuery(f"SELECT ldDateRetPlan FROM TB_Borrow WHERE bkID={BookId} AND rdID={rdID} AND IsHasReturn=0")
        print(BorrowResult)
        if BorrowResult == []:
            print(QMessageBox.information(self, "提示", "您并未借阅此书，故无需归还", QMessageBox.Yes, QMessageBox.Yes))
        else:
            ldDateRetPlan = BorrowResult[0][0]
            #还书语句块, 判断是否逾期
            if (ldDateRetPlan > datetime.datetime.now()): #未逾期
                Library.ExecNonQuery(f"UPDATE TB_Borrow SET ldDateRetAct=GETDATE(),IsHasReturn=1,OperatorRet='{self.studentName}'")
                Library.ExecNonQuery(f"UPDATE TB_Reader SET rdBorrowQty=rdBorrowQty-1 WHERE rdID = {rdID}")
                Library.ExecNonQuery(f"UPDATE TB_Book SET bkStatus = '在馆' WHERE bkID = {BookId}")
                print(QMessageBox.information(self, "提示", "归还成功!", QMessageBox.Yes, QMessageBox.Yes))
                return
            else:
                rdType = Library.ExecQuery(f"SELECT rdType FROM TB_Reader WHERE rdID={rdID}")
                rdType = rdType[0][0]
                OverMoneyRate = Library.ExecQuery(f"SELECT PunishRate FROM TB_ReaderType WHERE rdType={rdType}")
                OverMoneyRate = OverMoneyRate[0][0]
                dt = (ldDateRetPlan-datetime.datetime.now())
                for seq,char in enumerate(str(dt)):
                    if char==' ':
                        break
                ldOverDay = int(str(dt)[0:seq])
                ldOverMoney = ldOverDay * OverMoneyRate
                Library.ExecNonQuery(f"UPDATE TB_Borrow SET ldDateRetAct=GETDATE(),IsHasReturn=1,OperatorRet='{self.studentName}',ldOverDay={ldOverDay},ldOverMoney={ldOverMoney}")
                Library.ExecNonQuery(f"UPDATE TB_Reader SET rdBorrowQty=rdBorrowQty-1 WHERE rdID = {rdID}")
                Library.ExecNonQuery(f"UPDATE TB_Book SET bkStatus = '在馆' WHERE bkID = {BookId}")
                print(QMessageBox.warning(self, "警告", f"您已逾期{ldOverDay}天, 按规定需要交纳罚金{ldOverMoney}元", QMessageBox.Yes, QMessageBox.Yes))
                return

    def bookIdEditChanged(self):
        BookCategoryDict = {'TP':'自动化技术/计算机技术','TP3':'计算技术/计算机技术','TP31':'计算机软件','TP311':'程序设计/软件工程','TP312':'程序语言/算法语言','TP311.13':'数据库理论与系统','TP311.131':'数据库理论'}
        bookId = self.bookIdEdit.text()
        if (bookId == ""):
            self.bookNameEdit.clear()
            self.publisherEdit.clear()
            self.authorNameEdit.clear()
            self.publishTimeEdit.clear()
        # 查询对应书号，如果存在就更新form
        else:
            Library = MSSQL('Library')
            result = Library.ExecQuery(f"SELECT * FROM TB_Book WHERE bkID={bookId}")
            if not result == []:
                self.bookNameEdit.setText(result[0][2])
                self.authorNameEdit.setText(result[0][3])
                self.categoryComboBox.setCurrentText(BookCategoryDict[result[0][7]])
                self.publisherEdit.setText(result[0][4])
                self.publishTimeEdit.setText(str(result[0][5]))
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    #mainMindow = returnBookDialog('1','宋道源')
    #mainMindow.show()
    sys.exit(app.exec_())
