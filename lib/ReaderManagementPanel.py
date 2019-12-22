import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from lib.addLibraryCard import addLibraryCard
from lib.editLibraryCard import editLibraryCard
from lib.destoryLibraryCard import destoryLibraryCard
from lib.UserListViewer import UserListViewer
#QWidget
#妥协的结果QDialog
class ReaderManagementPanel(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        self.resize(1200, 800)
        self.setWindowTitle("借书证管理")
        self.layout = QHBoxLayout()
        self.buttonlayout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setPixelSize(16)
        self.addLibraryCardButtion = QPushButton("办理借书证")
        self.editLibraryCardButtion = QPushButton("变更借书证")
        self.destoryLibraryCardButton = QPushButton("销毁借书证")
        self.destoryLibraryCardButton.setFont(font)
        self.addLibraryCardButtion.setFont(font)
        self.editLibraryCardButtion.setFont(font)
        self.destoryLibraryCardButton.setFixedWidth(130)
        self.destoryLibraryCardButton.setFixedHeight(42)
        self.addLibraryCardButtion.setFixedWidth(130)
        self.addLibraryCardButtion.setFixedHeight(42)
        self.editLibraryCardButtion.setFixedWidth(130)
        self.editLibraryCardButtion.setFixedHeight(42)
        self.buttonlayout.addWidget(self.addLibraryCardButtion)
        self.buttonlayout.addWidget(self.editLibraryCardButtion)
        self.buttonlayout.addWidget(self.destoryLibraryCardButton)
        self.layout.addLayout(self.buttonlayout)
        self.userView = UserListViewer()
        self.layout.addWidget(self.userView)

        self.addLibraryCardButtion.clicked.connect(self.addLibraryCardButtionClicked)
        self.editLibraryCardButtion.clicked.connect(self.editLibraryCardButtionClicked)
        self.destoryLibraryCardButton.clicked.connect(self.destoryLibraryCardButtionClicked)

    def addLibraryCardButtionClicked(self):
        addLC = addLibraryCard(self)
        addLC.add_LibraryCard_success_signal.connect(self.userView.searchButtonClicked) 
        addLC.show()
        addLC.exec_()

    def editLibraryCardButtionClicked(self):
        editLC = editLibraryCard(self)
        editLC.edit_LibraryCard_successful_signal.connect(self.userView.searchButtonClicked)
        editLC.show()
        editLC.exec_()

    def destoryLibraryCardButtionClicked(self):
        destoryLC=destoryLibraryCard(self)
        destoryLC.destory_LibraryCard_successful_signal.connect(self.userView.searchButtonClicked)
        destoryLC.show()
        destoryLC.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = ReaderManagementPanel()
    mainMindow.show()
    sys.exit(app.exec_())