import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *

from lib.BookManagement import BookManagement


class addBookDialog(QDialog):
    add_book_success_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(addBookDialog, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("添加书籍")

    def setUpUI(self):
        
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["自动化技术/计算机技术","计算技术/计算机技术","计算机软件","程序设计/软件工程","程序语言/算法语言","数据库理论与系统","数据库理论"]
        BookLanguage = ["0-中文","1-英文","2-日文","3-俄文","4-德文","5-法文"]
        self.resize(350, 700)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titleLable = QLabel("添加书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.authorNameLabel = QLabel("作    者:")
        self.bookPressLabel = QLabel("出 版 社:")
        self.publishTimeLabel = QLabel("出版日期:")
        self.languageLable = QLabel("语  言:")
        self.pageLabel = QLabel("页    数:")
        self.priceLabel = QLabel("单   价:")
        self.ISBNLabel = QLabel("I S B N:")
        self.categoryLabel = QLabel('分  类:')
        self.briefLable = QLabel('内容简介:')

        # button控件
        self.addBookButton = QPushButton("添 加")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.authorNameEdit = QLineEdit()
        self.bookPressEdit = QLineEdit()
        #----------------------------------------------
        self.publishTimeEdit = QDateTimeEdit()
        self.publishTimeEdit.setDisplayFormat("yyyy-MM-dd")
        #----------------------------------------------
        #----------------------------------------------
        self.languageComboBox = QComboBox()
        self.languageComboBox.addItems(BookLanguage)
        #----------------------------------------------
        self.pageEdit = QLineEdit()
        self.priceEdit = QLineEdit()
        self.ISBNEdit = QLineEdit()
        #----------------------------------------------
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        #----------------------------------------------
        self.briefTextEdit = QTextEdit()

        self.bookNameEdit.setMaxLength(10)
        self.authorNameEdit.setMaxLength(10)
        self.bookPressEdit.setMaxLength(10)
        self.ISBNEdit.setMaxLength(13)
        self.ISBNEdit.setValidator(QIntValidator())

        # 添加进formlayout
        self.layout.addRow("", self.titleLable)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.authorNameLabel, self.authorNameEdit)
        self.layout.addRow(self.bookPressLabel, self.bookPressEdit)
        self.layout.addRow(self.publishTimeLabel, self.publishTimeEdit)
        self.layout.addRow(self.languageLable, self.languageComboBox)
        self.layout.addRow(self.pageLabel, self.pageEdit)
        self.layout.addRow(self.priceLabel, self.priceEdit)
        self.layout.addRow(self.ISBNLabel, self.ISBNEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.briefLable, self.briefTextEdit)
        self.layout.addRow("", self.addBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titleLable.setFont(font)
        font.setPixelSize(14)
        self.bookNameLabel.setFont(font)
        self.authorNameLabel.setFont(font)
        self.bookPressLabel.setFont(font)
        self.publishTimeLabel.setFont(font)
        self.languageLable.setFont(font)
        self.pageLabel.setFont(font)
        self.priceLabel.setFont(font)
        self.ISBNLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.briefLable.setFont(font)

        self.bookNameEdit.setFont(font)
        self.authorNameEdit.setFont(font)
        self.bookPressEdit.setFont(font)
        self.publishTimeEdit.setFont(font)
        self.pageEdit.setFont(font)
        self.priceEdit.setFont(font)
        self.ISBNEdit.setFont(font)
        self.briefTextEdit.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.addBookButton.setFont(font)
        self.addBookButton.setFixedHeight(32)
        self.addBookButton.setFixedWidth(140)

        # 设置间距
        self.titleLable.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.addBookButton.clicked.connect(self.addBookButtonCicked)

    def addBookButtonCicked(self):
        BookCategoryDict = {'自动化技术/计算机技术':'TP','计算技术/计算机技术':'TP3','计算机软件':'TP31','程序设计/软件工程':'TP311','程序语言/算法语言':'TP312','数据库理论与系统':'TP311.13','数据库理论':'TP311.131'}
        BookLanguageDict = {'0-中文':'0','1-英文':'1','2-日文':'2','3-俄文':'3','4-德文':'4','5-法文':'5'}
        bookName = self.bookNameEdit.text()
        authorName = self.authorNameEdit.text()
        bookPress = self.bookPressEdit.text()
        publishTime = self.publishTimeEdit.text()
        language = self.languageComboBox.currentText()
        page = self.pageEdit.text()
        price = self.priceEdit.text()
        isbn = self.ISBNEdit.text()
        bookCategory = self.categoryComboBox.currentText()
        
        brief = self.briefTextEdit.toPlainText()
        '''
        避免传参过多，将参数打包成一个列表后再传递
        示例：
        BM = BookManagement()
        bkInfoList = ['9787115313980','SQL必知必会','Ben Forta','人民邮电出版社','2013-05-01 00:00:00','9787115313980','TP311.131',0,239,29.00,'畅销全球的数据库入门经典','','在馆']
        BM.NewBookIn(bkInfoList)
        '''
        if (
                bookName == "" or authorName == "" or bookPress == "" or publishTime == "" or language == "" or page == "" or price == "" or isbn == "" or bookCategory ==""):
            print(QMessageBox.warning(self, "警告", "有字段为空，添加失败", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            BM = BookManagement()
            bookCategory = BookCategoryDict[bookCategory]
            language = BookLanguageDict[language]
            bkInfoList=[isbn,bookName,authorName,bookPress,publishTime,isbn,bookCategory,language,page,price,brief,'','在馆']
            BM.NewBookIn(bkInfoList)
            self.clearEdit()
        return

    def clearEdit(self):
        self.bookNameEdit.clear()
        self.authorNameEdit.clear()
        self.bookPressEdit.clear()
        self.publishTimeEdit.clear()
        self.languageComboBox.clear()
        self.pageEdit.clear()
        self.priceEdit.clear()
        self.ISBNEdit.clear()
        self.categoryComboBox.clear()
        self.briefTextEdit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = addBookDialog()
    mainMindow.show()
    sys.exit(app.exec_())
