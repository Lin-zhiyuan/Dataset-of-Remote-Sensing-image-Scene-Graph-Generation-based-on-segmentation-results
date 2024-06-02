#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:31:19 2018

@author: sia-403
"""

from PyQt5 import QtWidgets, QtGui
from prediction import Ui_Form
import test_read_graph


class mywindow(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.selectPic.clicked.connect(self.myprint)
        image = QtGui.QPixmap("./w10.png")
        image = image.scaled(200, 200)
        self.PicShow.setPixmap(image)
        self.PicShow.show()

    def myprint(self):
        pic_path, pic_type = QtWidgets.QFileDialog.getOpenFileName(self, 'select picture', ".", "Image Files(*);;Image Files(*bmp);;Image Files(*jpg);;Image Files(*png);;Image Files(*jpeg)")
        print(pic_path)
        #              image = QtGui.QImage(pic_path)
        image = QtGui.QPixmap(pic_path)
        image = image.scaled(200, 200)
        self.PicShow.setPixmap(image)
        self.PicShow.show()
        prediction_result = test_read_graph.PrePic(pic_path)
        if prediction_result == 0:
            result = "is ball"
        elif prediction_result == 1:
            result = "is block"
        elif prediction_result == 2:
            result = "is coal"
        else:
            result = "is backdrop"
        self.PreResult.setText("%s" % result)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    #    myapp = MyForm()   #MyForm是自己的窗体类名
    #    myapp.show()
    sys.exit(app.exec_())
