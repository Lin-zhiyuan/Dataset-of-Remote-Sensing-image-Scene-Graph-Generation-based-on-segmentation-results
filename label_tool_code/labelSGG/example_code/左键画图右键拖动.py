import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import cv2.cv2 as cv


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.path = ""
        self.cur_img = ""
        self.img_w = ""
        self.img_h = ""
        self.left_flag = False
        self.right_flag = False
        self.label_x = 0  # label当前坐标
        self.label_y = 0
        self.mouse_mv_x = ""  # 鼠标移动上一次坐标
        self.mouse_mv_y = ""
        self.x1 = ""
        self.y1 = ""

        self.last_x = ""  # 画画上一个点坐标
        self.last_y = ""
        self.mouse_mv_x1 = ""  # 中转点
        self.mouse_mv_y1 = ""

    def initUI(self):
        self.setGeometry(300, 200, 580, 430)
        self.setWindowTitle('Hello')

        self.pushbutton = QtWidgets.QPushButton(self)
        self.pushbutton.setGeometry(0, 0, 100, 30)
        self.pushbutton.clicked.connect(self.open_pic)
        self.pushbutton.setText("选择图片")

        self.groupbox = QtWidgets.QGroupBox(self)
        self.groupbox.setGeometry(0, 30, 580, 400)

        self.label = QtWidgets.QLabel(self.groupbox)
        self.label.setGeometry(0, 0, 580, 400)

    # 打开一个图片文件
    def open_pic(self):
        self.path = Qt.QFileDialog.getOpenFileName()
        self.cur_img = cv.imread(self.path[0])
        self.img_w = 580
        self.img_h = 400
        # self.cur_img = cv.cvtColor(self.cur_img, cv.COLOR_BGR2RGB)
        self.label.setPixmap(QtGui.QPixmap(self.path[0]).scaled(self.img_w, self.img_h))  # 在label中显示图片

    # 鼠标左击事件
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.left_flag = True
        if event.buttons() == QtCore.Qt.RightButton:
            self.right_flag = True

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.left_flag = False
        self.right_flag = False
        self.mouse_mv_y = ""
        self.mouse_mv_x = ""
        self.last_x = ""
        self.last_y = ""

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.left_flag:  # 鼠标左击
            self.x1 = event.x()
            self.y1 = event.y()
            mv_x = int((self.x1 - self.label_x) * self.cur_img.shape[1] / 580)
            mv_y = int((self.y1 - 30 - self.label_y) * self.cur_img.shape[0] / 400)
            cv.circle(self.cur_img, (mv_x, mv_y), 4, (0, 0, 0), -1)
            if self.last_x != "" and self.last_y != "":
                # if self.mouse_mv_x != "" and self.mouse_mv_y != "":
                cv.line(self.cur_img, (int((self.last_x - self.label_x) * self.cur_img.shape[1] / 580),
                                       int((self.last_y - self.label_y - 30) * self.cur_img.shape[0] / 400)), (
                        int((self.x1 - self.label_x) * self.cur_img.shape[1] / 580),
                        int((self.y1 - self.label_y - 30) * self.cur_img.shape[0] / 400)), (0, 0, 0), 8)
                # elif self.mouse_mv_x == "" and self.mouse_mv_y == "":
                #    cv.line(self.cur_img,(int(self.last_x*self.cur_img.shape[1]/580),int((self.last_y - 30)*self.cur_img.shape[0]/400)),(int(self.x1*self.cur_img.shape[1]/580),int((self.y1-30)*self.cur_img.shape[0]/400)),(0,0,0),8)
            self.last_x = self.x1
            self.last_y = self.y1

            img2 = cv.cvtColor(self.cur_img, cv.COLOR_BGR2RGB)
            QImage = QtGui.QImage(img2, self.cur_img.shape[1], self.cur_img.shape[0], 3 * self.cur_img.shape[1],
                                  QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap(QImage).scaled(self.label.width(), self.label.height())
            self.label.setPixmap(pixmap)

        if self.right_flag:  # 鼠标右击
            self.x1 = event.x()
            self.y1 = event.y()
            if self.mouse_mv_x != "" and self.mouse_mv_y != "":
                self.label_x = self.label_x + (self.x1 - self.mouse_mv_x)
                self.label_y = self.label_y + (self.y1 - self.mouse_mv_y)
            self.mouse_mv_x = self.x1
            self.mouse_mv_y = self.y1
            self.label.setGeometry(self.label_x, self.label_y, 580, 400)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
