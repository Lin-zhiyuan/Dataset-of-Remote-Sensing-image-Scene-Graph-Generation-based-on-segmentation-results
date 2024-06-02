import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 窗体设置
        self.setWindowTitle("关闭窗口")
        # 菜单动作
        self.exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip("Exit application")
        self.exitAct.triggered.connect(self.quitAction)
        # 菜单栏
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False)
        self.fileMenu = self.menu.addMenu('File')
        self.fileMenu.addAction(self.exitAct)
        # 中心窗口嵌入widget布局
        self.label1 = QLabel('label1')
        self.label2 = QLabel('label2')
        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.textEdit1 = QTextEdit()
        self.textEdit2 = QTextEdit()
        # self.textEdit2.setCursor(Qt.PointingHandCursor)
        self.formlayout1 = QFormLayout()
        self.formlayout2 = QFormLayout()
        self.formlayout1.addRow(self.label1, self.lineEdit1)
        self.formlayout2.addRow(self.label2, self.lineEdit2)
        self.vbox1 = QVBoxLayout()
        self.vbox1.addLayout(self.formlayout1)
        self.vbox1.addWidget(self.textEdit1)
        self.vbox2 = QVBoxLayout()
        self.vbox2.addLayout(self.formlayout2)
        self.vbox2.addWidget(self.textEdit2)
        self.gridlayout = QGridLayout()
        self.gridlayout.addItem(self.vbox1, 0, 0)
        self.gridlayout.addItem(self.vbox2, 0, 1)
        self.widGet = QWidget()
        self.widGet.setLayout(self.gridlayout)
        self.setCentralWidget(self.widGet)
        self.center()

    # 窗口居中
    def center(self):
        self.size = QDesktopWidget().screenGeometry()
        self.resize = self.geometry()
        self.move((self.size.width() - self.resize.width()) / 2, (self.size.height() - self.resize.height()) / 2)

    def quitAction(self):
        QApplication.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QLabel, QMainWindow, QLineEdit, QTextEdit, QGridLayout, QApplication



# class GripLayout2(QWidget):
#     def __init__(self, parent=None):
#         super(GripLayout2, self).__init__(parent)
#         self.initUI()
#
#     def initUI(self):
#         title = QLabel('Title')
#         author = QLabel('Author')
#         review = QLabel('Review')
#         titleEdit = QLineEdit()
#         authorEdit = QLineEdit()
#         reviewEdit = QTextEdit()
#         reviewEdit.setCursor(Qt.PointingHandCursor)
#         grid = QGridLayout()
#         grid.setSpacing(10)
#         grid.addWidget(title, 1, 0)
#         grid.addWidget(titleEdit, 1, 1)
#         grid.addWidget(author, 2, 0)
#         grid.addWidget(authorEdit, 2, 1)
#         grid.addWidget(review, 3, 0)
#         grid.addWidget(reviewEdit, 3, 1, 5, 1)
#         self.setLayout(grid)
#         self.setWindowTitle('grid layout')
#         self.resize(350, 300)
#         # self.setCursor(Qt.PointingHandCursor)
#
#
# class Mainwindows(QMainWindow):
#     def __init__(self):
#         super(Mainwindows, self).__init__()
#         self.resize(1024, 768)
#
#         self.subwidget = GripLayout2(self)
#         self.setCentralWidget(self.subwidget)
#
#
# app = QApplication(sys.argv)
# ui = Mainwindows()
# ui.show()
# sys.exit(app.exec_())