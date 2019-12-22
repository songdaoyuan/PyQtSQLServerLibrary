import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time

from lib.BookManagement import BookManagement
from lib.SQLQuery import MSSQL


class dropBookDialog(QDialog):
    drop_book_successful_signal=pyqtSignal()

    def __init__(self, parent=None):
        super(dropBookDialog, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("变卖/销毁书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        BookCategory = ["自动化技术/计算机技术","计算技术/计算机技术","计算机软件","程序设计/软件工程","程序语言/算法语言","数据库理论与系统","数据库理论"]
        self.resize(400, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("变卖/销毁书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")
        self.destroyedOrSellLable = QLabel('处理类型:')

        # button控件
        self.dropBookButton = QPushButton("执 行")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QLineEdit()
        # self.publishDateEdit = QLineEdit()
        self.destroyedOrSellComboBox = QComboBox()
        self.destroyedOrSellComboBox.addItems(['变卖', '销毁'])

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(6)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow(self.destroyedOrSellLable, self.destroyedOrSellComboBox)
        self.layout.addRow("", self.dropBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(14)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)
        self.destroyedOrSellLable.setFont(font)

        self.bookNameEdit.setFont(font)
        self.bookNameEdit.setReadOnly(True)
        self.bookNameEdit.setStyleSheet("background-color:#363636")
        self.bookIdEdit.setFont(font)
        self.authNameEdit.setFont(font)
        self.authNameEdit.setReadOnly(True)
        self.authNameEdit.setStyleSheet("background-color:#363636")
        self.publisherEdit.setFont(font)
        self.publisherEdit.setReadOnly(True)
        self.publisherEdit.setStyleSheet("background-color:#363636")
        self.publishTime.setFont(font)
        self.publishTime.setStyleSheet("background-color:#363636")
        self.categoryComboBox.setFont(font)
        self.categoryComboBox.setStyleSheet("background-color:#363636")
        self.destroyedOrSellComboBox.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.dropBookButton.setFont(font)
        self.dropBookButton.setFixedHeight(32)
        self.dropBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.dropBookButton.clicked.connect(self.dropBookButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)

    def bookIdEditChanged(self):
        bookId = self.bookIdEdit.text()
        if (bookId == ""):
            self.bookNameEdit.clear()
            self.publisherEdit.clear()
            self.authNameEdit.clear()
            self.publishTime.clear()
        # 查询对应书号，如果存在就更新form
        Library = MSSQL('Library')
        self.result = Library.ExecQuery(f"SELECT * FROM TB_Book WHERE bkId='{bookId}'")
        if not self.result == []:
            BookCategoryDict = {'TP':'自动化技术/计算机技术','TP3':'计算技术/计算机技术','TP31':'计算机软件','TP311':'程序设计/软件工程','TP312':'程序语言/算法语言','TP311.13':'数据库理论与系统','TP311.131':'数据库理论'}
            self.bookNameEdit.setText(self.result[0][2])
            self.authNameEdit.setText(self.result[0][3])
            self.categoryComboBox.setCurrentText(BookCategoryDict[self.result[0][7]])
            self.publisherEdit.setText(self.result[0][4])
            self.publishTime.setText(self.result[0][5].strftime('%Y-%m-%d'))
        return

    def dropBookButtonClicked(self):
        bookId = self.bookIdEdit.text()
        if ((self.result == []) or (bookId == '')):
            print(QMessageBox.warning(self, "警告", "数据库中无对应ID的图书, 删除失败, 请重试!"), QMessageBox.Yes, QMessageBox.Yes)
            return
        BM = BookManagement()
        BMS = BM.BookDestroyOrSell(bookId, self.destroyedOrSellComboBox.currentText())
        print(QMessageBox.warning(self, "警告", BMS), QMessageBox.Yes, QMessageBox.Yes)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = dropBookDialog()
    mainMindow.show()
    sys.exit(app.exec_())
