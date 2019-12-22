import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import datetime
from PyQt5.QtSql import *
from lib.SQLQuery import MSSQL


class borrowBookDialog(QDialog):
    borrow_book_success_signal = pyqtSignal()

    def __init__(self, StudentId, StudentName ,parent=None):
        super(borrowBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.studentName = StudentName
        #self.studentId = '1'
        #self.studentName = '宋道源'
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("借阅/续借书籍")

    def setUpUI(self):
        BookCategory = ["自动化技术/计算机技术","计算技术/计算机技术","计算机软件","程序设计/软件工程","程序语言/算法语言","数据库理论与系统","数据库理论"]
        self.resize(350, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.borrowStudentLabel = QLabel("借阅人ID:")
        self.borrowStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  借阅/续借书籍")
        self.processTypeLable = QLabel("操作类型")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authorNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.IsbnLabel = QLabel("出版日期:")

        # button控件
        self.borrowBookButton = QPushButton("确认借阅")

        # lineEdit控件
        self.processTypeComboBox = QComboBox()
        self.processTypeComboBox.addItems(['借书','续借'])
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authorNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.Isbn = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(6)
        self.authorNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.borrowStudentLabel, self.borrowStudentIdLabel)
        self.layout.addRow(self.processTypeLable, self.processTypeComboBox)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authorNameLabel, self.authorNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.IsbnLabel, self.Isbn)
        self.layout.addRow("", self.borrowBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.processTypeLable.setFont(font)
        self.borrowStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.borrowStudentLabel.setFont(font)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authorNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.IsbnLabel.setFont(font)

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
        self.Isbn.setFont(font)
        self.Isbn.setStyleSheet("background-color:#363636")
        self.categoryComboBox.setFont(font)
        self.categoryComboBox.setStyleSheet("background-color:#363636")

        # button设置
        font.setPixelSize(16)
        self.borrowBookButton.setFont(font)
        self.borrowBookButton.setFixedHeight(32)
        self.borrowBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.borrowBookButton.clicked.connect(self.borrowButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.bookIdEdit.returnPressed.connect(self.borrowButtonClicked)

    def borrowButtonClicked(self):
        BookId = self.bookIdEdit.text()
        rdID = int(self.studentId)
        processType = self.processTypeComboBox.currentText()
        if (BookId == ""):
                print(QMessageBox.warning(self, "警告", "输入的ID不能为空, 请检查输入", QMessageBox.Yes, QMessageBox.Yes))
                return
        # 打开数据库
        Library = MSSQL('Library')
        bookResult = Library.ExecQuery(f"SELECT bkStatus FROM TB_Book WHERE bkID={BookId}") #查询图书状态

        borrowQtyAndrdTypeResult = Library.ExecQuery(f"SELECT * FROM TB_Reader WHERE rdID={rdID}") #查询借阅者属性
        borrowQty = borrowQtyAndrdTypeResult[0][10]
        rdType = borrowQtyAndrdTypeResult[0][3]
        
        #查询可借阅/续借数量, 天数
        CanLendQtyAndCanLendDayAndCanContinueTimes = Library.ExecQuery(f"SELECT CanLendQty,CanLendDay,CanContinueTimes FROM TB_ReaderType WHERE rdType={rdType}")
        CanLendQty = CanLendQtyAndCanLendDayAndCanContinueTimes[0][0]
        CanLendDay = CanLendQtyAndCanLendDayAndCanContinueTimes[0][1]
        CanContinueTimes = CanLendQtyAndCanLendDayAndCanContinueTimes[0][2]
        if processType == '借书':

            
            #获取新书的借阅ID
            BorrowID = Library.ExecQuery("SELECT COUNT(BorrowID) FROM TB_Borrow")
            BorrowID = BorrowID[0][0] + 1
            
            IsHaveBorrowed = Library.ExecQuery(f"SELECT * FROM TB_Borrow WHERE rdID={rdID} AND bkID={BookId} AND IsHasReturn=0")
            print(IsHaveBorrowed!= [])
            if borrowQty >= CanLendQty: #判断借书先决条件, 借书数目和可借数目
                print(QMessageBox.warning(self, "警告", "已借书数目超过可借书上限，无法继续借书，请先还书", QMessageBox.Yes, QMessageBox.Yes)) 
            elif bookResult == []: #判断书存不存在
                print(QMessageBox.warning(self, "警告", "你所要借的书不存在, 请检查输入", QMessageBox.Yes, QMessageBox.Yes))
            elif bookResult[0][0] == '借出' and IsHaveBorrowed == []:
                print(QMessageBox.warning(self, "警告", "所借的书已借出，请借阅其它图书", QMessageBox.Yes, QMessageBox.Yes))
            elif bookResult[0][0] in ['销毁','遗失','变卖']: #判断书是否被处理掉了
                print(QMessageBox.warning(self, "警告", "所借的书已遗失/销毁/变卖，请联系图书管理员", QMessageBox.Yes, QMessageBox.Yes))
            elif IsHaveBorrowed != []:
                print(QMessageBox.warning(self, "警告", "您已经借过这本书了", QMessageBox.Yes, QMessageBox.Yes))
            else: 
                Library.ExecNonQuery(f"INSERT INTO TB_Borrow (BorrowID,rdID,bkID,ldContinueTimes,ldDateOut,ldDateRetPlan,IsHasReturn,OperatorLend) VALUES ({BorrowID},{rdID},{BookId},0,GETDATE(),GETDATE()+{CanLendDay},0,'{self.studentName}')")
                Library.ExecNonQuery(f"UPDATE TB_Reader SET rdBorrowQty=rdBorrowQty+1 WHERE rdID = {rdID}")
                Library.ExecNonQuery(f"UPDATE TB_Book SET bkStatus = '借出' WHERE bkID = {BookId}")
                print(QMessageBox.warning(self, "提示", "借书成功, 请注意按期归还", QMessageBox.Yes, QMessageBox.Yes))
                self.bookIdEdit.clear()
        else: #续借
            print('续借')
            result = Library.ExecQuery(f"SELECT * FROM TB_Borrow WHERE bkID = {BookId} AND rdID = {rdID}")
            if result == []:
                print(QMessageBox.warning(self, "警告", "您未借阅这本书，请借阅后重试", QMessageBox.Yes, QMessageBox.Yes)) 
                return
            print('here1')
            BorrowInfo = Library.ExecQuery(f"SELECT rdID,ldContinueTimes,ldDateRetPlan,IsHasReturn FROM TB_Borrow WHERE bkID = {BookId}")
            bkID2rdID = BorrowInfo[0][0]
            ldContinueTimes = BorrowInfo[0][1]
            ldDateRetPlan = BorrowInfo[0][2]
            IsHasReturn = BorrowInfo[0][3]
            print('here')
            if ldContinueTimes >= CanContinueTimes:
                print(QMessageBox.warning(self, "警告", "超过续借次数上限, 无法续借, 请先归还后再借书", QMessageBox.Yes, QMessageBox.Yes))
            elif ldDateRetPlan < datetime.datetime.now():
                print(QMessageBox.warning(self, "警告", "已逾期, 无法续借, 请先归还后再借书", QMessageBox.Yes, QMessageBox.Yes))
            else:
                Library.ExecNonQuery(f"UPDATE TB_Borrow SET ldContinueTimes=ldContinueTimes+1, ldDateRetPlan=GETDATE()+{CanLendDay}")
                print(QMessageBox.warning(self, "提示", "续借成功! ", QMessageBox.Yes, QMessageBox.Yes))
                self.bookIdEdit.clear()
        

    def bookIdEditChanged(self):
        BookCategoryDict = {'TP':'自动化技术/计算机技术','TP3':'计算技术/计算机技术','TP31':'计算机软件','TP311':'程序设计/软件工程','TP312':'程序语言/算法语言','TP311.13':'数据库理论与系统','TP311.131':'数据库理论'}
        bookId = self.bookIdEdit.text()
        if (bookId == ""):
            self.bookNameEdit.clear()
            self.publisherEdit.clear()
            self.authorNameEdit.clear()
            self.Isbn.clear()
        # 查询对应书号，如果存在就更新form
        else:
            Library = MSSQL('Library')
            result = Library.ExecQuery(f"SELECT * FROM TB_Book WHERE bkID={bookId}")
            if not result == []:
                self.bookNameEdit.setText(result[0][2])
                self.authorNameEdit.setText(result[0][3])
                self.categoryComboBox.setCurrentText(BookCategoryDict[result[0][7]])
                self.publisherEdit.setText(result[0][4])
                self.Isbn.setText(result[0][6])
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    #mainMindow = borrowBookDialog('1','宋道源')
    #mainMindow.show()
    sys.exit(app.exec_())
