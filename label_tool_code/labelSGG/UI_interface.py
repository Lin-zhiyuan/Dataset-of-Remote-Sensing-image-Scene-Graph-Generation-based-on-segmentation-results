# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import sys
import os
from PIL import Image
import numpy as np
import cv2 as cv
import json


class MyTextBrowser(QTextBrowser):
    SelectPicSignal = pyqtSignal(str, name='SelectedPicName')
    ClearObjectName = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Pre_Cursor = None
        self.Curr_Cursor = None
        self.selected_img = ''

    def mousePressEvent(self, e):
        self.ClearObjectName.emit()
        pos = e.pos()
        self.Curr_Cursor = self.cursorForPosition(pos)
        tcf = QTextCharFormat()
        if self.Pre_Cursor is not None:
            tcf.setBackground(Qt.white)
            tcf.setForeground(Qt.black)
            self.Pre_Cursor.movePosition(QTextCursor.EndOfLine)
            self.Pre_Cursor.select(QTextCursor.LineUnderCursor)
            self.Pre_Cursor.setCharFormat(tcf)
        self.Pre_Cursor = self.Curr_Cursor

        if e.type() == QEvent.MouseButtonPress:
            tcf.setBackground(Qt.blue)
            tcf.setForeground(Qt.white)
            self.Curr_Cursor.movePosition(QTextCursor.EndOfLine)
            self.Curr_Cursor.select(QTextCursor.LineUnderCursor)
            self.Curr_Cursor.setCharFormat(tcf)
            if self.Curr_Cursor.selectedText() == '':
                self.Curr_Cursor = None
                return
            self.selected_img = self.Curr_Cursor.selectedText()
            self.SelectPicSignal.emit(self.selected_img)

    def keyPressEvent(self, e):
        key = e.key()
        tcf = QTextCharFormat()
        if self.Curr_Cursor is None:
            return
        else:
            if key == Qt.Key_Up:
                tcf.setBackground(Qt.white)
                tcf.setForeground(Qt.black)
                self.Curr_Cursor.setCharFormat(tcf)
                self.Curr_Cursor.movePosition(QTextCursor.Up)
                self.Curr_Cursor.movePosition(QTextCursor.EndOfLine)
                self.Curr_Cursor.select(QTextCursor.LineUnderCursor)
                tcf.setBackground(Qt.blue)
                tcf.setForeground(Qt.white)
                self.Curr_Cursor.setCharFormat(tcf)
                self.selected_img = self.Curr_Cursor.selectedText()
                self.SelectPicSignal.emit(self.selected_img)

            elif key == Qt.Key_Down:
                tcf.setBackground(Qt.white)
                tcf.setForeground(Qt.black)
                self.Curr_Cursor.setCharFormat(tcf)
                self.Curr_Cursor.movePosition(QTextCursor.Down)
                self.Curr_Cursor.movePosition(QTextCursor.EndOfLine)
                self.Curr_Cursor.select(QTextCursor.LineUnderCursor)
                tcf.setBackground(Qt.blue)
                tcf.setForeground(Qt.white)
                self.Curr_Cursor.setCharFormat(tcf)
                self.selected_img = self.Curr_Cursor.selectedText()
                self.SelectPicSignal.emit(self.selected_img)


class PaintBoard(QLabel):
    enterImageboard = pyqtSignal()
    drawSelectedObject = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__('Image panel')
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignCenter)

        self.SelectedPath = ''
        self.img_name = ''
        self.mask_path = ''

        self.img_board = QPixmap()
        self.img_mask = ''
        self.curr_img = ''
        self.img_and = None

        self.last_x = ''
        self.last_y = ''
        self.curr_x = ''
        self.curr_y = ''
        self.left_flag = False
        self.img_flag = False

        self.label_H = self.size().height()
        self.label_W = self.size().width()
        self.img_H = 0
        self.img_W = 0

    def DrawPic(self, pic):
        print(self.SelectedPath + pic)
        # if self.img_flag is False:
        self.img_name = pic
        self.img_board.load(self.SelectedPath + self.img_name)
        self.img_H = self.img_board.size().height()
        self.img_W = self.img_board.size().width()

        self.setPixmap(self.img_board)

        self.img_flag = True

        self.curr_img = cv.imdecode(np.fromfile(self.SelectedPath + self.img_name, dtype=np.uint8), -1)
        self.img_mask = np.zeros((self.curr_img.shape), dtype=np.uint8)

    def ResetPic(self):
        if self.img_flag:
            self.setPixmap(self.img_board)
            self.img_mask = np.zeros((self.curr_img.shape), dtype=np.uint8)

    def mousePressEvent(self, e):
        self.enterImageboard.emit()
        if e.buttons() == Qt.LeftButton:
            self.left_flag = True

    def mouseReleaseEvent(self, e):
        self.left_flag = False
        self.last_x = ''
        self.last_y = ''
        if self.img_flag and self.img_and is not None:
            self.drawSelectedObject.emit(self.img_and)

    def mouseMoveEvent(self, e):
        if self.left_flag and self.img_flag:
            self.curr_x = e.x()
            self.curr_y = e.y()
            self.label_H = self.size().height()
            self.label_W = self.size().width()
            mv_x = self.curr_x - int(self.label_W / 2 - self.img_W / 2)
            mv_y = self.curr_y - int(self.label_H / 2 - self.img_H / 2)
            cv.circle(self.img_mask, (mv_x, mv_y), 5, (0, 0, 255), 5)

            if self.last_x != '' and self.last_y != '':
                cv.line(self.img_mask, (mv_x, mv_y), (self.last_x, self.last_y), (0, 0, 255), 15)

            img_add = cv.addWeighted(self.curr_img, 1, self.img_mask, 1, 0)
            self.last_x = mv_x
            self.last_y = mv_y
            img = cv.cvtColor(img_add, cv.COLOR_BGR2RGB)
            QImage = QtGui.QImage(img, self.curr_img.shape[1], self.curr_img.shape[0], 3 * self.curr_img.shape[1],
                                  QtGui.QImage.Format_RGB888)
            pixmap = QPixmap(QImage)
            self.setPixmap(pixmap)

            B, G, R = cv.split(self.img_mask)
            image_r = cv.merge([R, R, R])
            self.img_and = cv.bitwise_and(image_r, self.curr_img)


class SelectObject(QLabel):
    getObjectSubjectName = pyqtSignal(str)

    def __init__(self):
        super().__init__('Selected Object')
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setCursor(Qt.CrossCursor)
        self.setAlignment(Qt.AlignCenter)

        self.imgSelected = ''
        self.img_name = ''
        self.object = None
        self.drawSelectedObject_flag = False

        self.label_H = 0
        self.label_W = 0
        self.img_H = 0
        self.img_W = 0

        self.objectName = ''
        self.objectID = ''
        self.maskSavePath = ''

        self.labelPath = ''
        self.ObImg = None
        self.ObjectName = ''
        self.SubjcetName = ''
        self.PreName = None
        self.PreID = None

    def drawSelectedObject(self, img):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.imgSelected = img
        self.img_H = self.imgSelected.shape[0]
        self.img_W = self.imgSelected.shape[1]

        QImage = QtGui.QImage(img, img.shape[1], img.shape[0], 3 * img.shape[1],
                              QtGui.QImage.Format_RGB888)
        pix = QPixmap(QImage)
        self.setPixmap(pix)
        self.drawSelectedObject_flag = True

    def mousePressEvent(self, e):
        self.label_H = self.size().height()
        self.label_W = self.size().width()
        mh = e.y() - int(self.label_H / 2 - self.img_H / 2)
        mw = e.x() - int(self.label_W / 2 - self.img_W / 2)

        if self.drawSelectedObject_flag and mh in range(0, self.img_H) and mw in range(0, self.img_W):
            img_mask_HSV = cv.cvtColor(self.imgSelected, cv.COLOR_RGB2HSV)
            th = img_mask_HSV[mh, mw]
            low_hsv = np.array(th, dtype=np.uint8)
            upper_hsv = np.array(th, dtype=np.uint8)
            object_mask = cv.inRange(img_mask_HSV, low_hsv, upper_hsv)
            object_mask = cv.merge([object_mask, object_mask, object_mask])
            self.object = cv.bitwise_and(object_mask, self.imgSelected)
            object_QImage = QtGui.QImage(self.object, self.object.shape[1], self.object.shape[0], 3 * self.object.shape[1],
                                  QtGui.QImage.Format_RGB888)
            pix = QPixmap(object_QImage)
            self.setPixmap(pix)
            self.drawSelectedObject_flag = False

    def getimgname(self, pic_name):
        self.img_name = pic_name
        self.objectCount = {}

    def getONOID(self, ON, OID):
        self.objectName = ON
        self.objectID = OID
        if ON in self.objectCount:
            self.objectCount[ON] = self.objectCount[ON] + 1
        else:
            self.objectCount.update({ON: 0})

    def getPredicationNId(self, PN, PID):
        self.PreName = PN
        self.PreID = PID

    def saveObject(self):
        objectsDict = {}
        if self.img_name is not '':
            if self.maskSavePath is '':
                labePath = os.path.exists(self.img_name[:-4])
            else:
                labePath = os.path.exists(self.maskSavePath + '/' + self.img_name[:-4])

            if not labePath:
                if self.maskSavePath is not '':
                    os.makedirs(self.maskSavePath + '/' + self.img_name[:-4])
                    self.labelPath = self.maskSavePath + '/' + self.img_name[:-4]
                else:
                    os.makedirs(os.getcwd() + '/' + self.img_name[:-4])
                    self.labelPath = os.getcwd() + '/' + self.img_name[:-4]

                item_dict = {'image_id': self.img_name}
                item_dict.update({'objects':[]})
                item_dict.update({'relationships':[]})
                objectsDict.update({'object_id': str(self.objectCount[self.objectName]) + '_' + str(self.objectID)})
                objectsDict.update({'mask': str(self.objectCount[self.objectName]) + '_' + str(self.objectID) + '.png'})
                objectsDict.update({'name': self.objectName})

                item_dict['objects'].append(objectsDict)
                jsonfile = json.dumps(item_dict, indent=4, separators=(',', ': '))
                f = open(self.labelPath + '/' + self.img_name[:-4] + '.json', 'w')
                f.write(jsonfile)
                f.close()
                self.getObjectSubjectName.emit(objectsDict['object_id'] + ' ' + self.objectName)
            else:
                objectsDict.update({'object_id': str(self.objectCount[self.objectName]) + '_' + str(self.objectID)})
                objectsDict.update({'mask': str(self.objectCount[self.objectName]) + '_' + str(self.objectID) + '.png'})
                objectsDict.update({'name': self.objectName})

                f = open(self.labelPath + '/' + self.img_name[:-4] + '.json', 'r')
                old_data = json.load(f)
                f.close()

                old_data['objects'].append(objectsDict)
                jsonfile = json.dumps(old_data, indent=4, separators=(',', ':'))
                f = open(self.labelPath + '/' + self.img_name[:-4] + '.json', 'w')
                f.write(jsonfile)
                f.close()
                self.getObjectSubjectName.emit(objectsDict['object_id'] + ' ' + self.objectName)

        if self.object is not None:
            mask = Image.fromarray(self.object)
            mask.save(self.labelPath + '/' + str(self.objectCount[self.objectName]) + '_' + str(self.objectID) + '.png')

    def setObjectImg(self, OName):
        self.ObjectName = OName.split(' ')[0]
        ObimgName = self.ObjectName + '.png'
        self.ObImg = cv.imdecode(np.fromfile(self.labelPath + '/' + ObimgName, dtype=np.uint8), -1)
        img = cv.cvtColor(self.ObImg, cv.COLOR_BGR2RGB)
        QImage = QtGui.QImage(img, self.ObImg.shape[1], self.ObImg.shape[0], 3 * self.ObImg.shape[1],
                              QtGui.QImage.Format_RGB888)
        pixmap = QPixmap(QImage)
        self.setPixmap(pixmap)

    def setSubjectImg(self, SuName):
        self.SubjcetName = SuName.split(' ')[0]
        SuimgName = self.SubjcetName + '.png'
        SuImg = cv.imdecode(np.fromfile(self.labelPath + '/' + SuimgName, dtype=np.uint8), -1)
        SumImg = cv.addWeighted(self.ObImg, 1, SuImg, 1, 0)
        img = cv.cvtColor(SumImg, cv.COLOR_BGR2RGB)
        QImage = QtGui.QImage(img, SuImg.shape[1], SuImg.shape[0], 3 * SuImg.shape[1],
                              QtGui.QImage.Format_RGB888)
        pixmap = QPixmap(QImage)
        self.setPixmap(pixmap)

    def savePredication(self):
        if self.objectName is not '' and self.SubjcetName is not '' and self.PreName is not None:
            relationships = {}
            relationships.update({'relationship_id': self.PreID})
            relationships.update({'predicate': self.PreName})
            relationships.update({'subject_id': self.SubjcetName})
            relationships.update({'object_id': self.ObjectName})
            f = open(self.labelPath + '/' + self.img_name[:-4] + '.json', 'r')
            old_data = json.load(f)
            f.close()

            old_data['relationships'].append(relationships)
            jsonfile = json.dumps(old_data, indent=4, separators=(',', ':'))
            f = open(self.labelPath + '/' + self.img_name[:-4] + '.json', 'w')
            f.write(jsonfile)
            f.close()


class LabelBoard(QFrame):
    GetClassName = pyqtSignal(str, int)
    GetPreNameId = pyqtSignal(str, int)
    GetObName = pyqtSignal(str)
    GetSubName = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initLabelBoard()

    def initLabelBoard(self):
        LB_layout = QGridLayout()

        self.selectedobject = SelectObject()
        LB_layout.addWidget(self.selectedobject, 0, 0, 3, 3)

        self.savepathlabel = QLabel('重置标签：')
        LB_layout.addWidget(self.savepathlabel, 3, 0, 1, 1)
        self.ResetB = QPushButton('Reset Mask')
        LB_layout.addWidget(self.ResetB, 3, 1, 1, 1)

        self.savepathlabel = QLabel('设置标签保存路径：')
        LB_layout.addWidget(self.savepathlabel, 4, 0, 1, 1)
        self.savePath = QPushButton('Mask Path')
        LB_layout.addWidget(self.savePath, 4, 1, 1, 1)

        self.savemaskB = QLabel('保存标签：')
        LB_layout.addWidget(self.savemaskB, 5, 0, 1, 1)
        self.saveMask = QPushButton('Save Mask')
        LB_layout.addWidget(self.saveMask, 5, 1, 1, 1)

        self.classList = QLabel('类别列表：')
        LB_layout.addWidget(self.classList, 6, 0, 1, 1)
        self.allClass = QComboBox()
        LB_layout.addWidget(self.allClass, 6, 1, 1, 1)

        self.objectList = QLabel('Object List: ')
        LB_layout.addWidget(self.objectList, 7, 0, 1, 1)
        self.allObjects = QComboBox()
        LB_layout.addWidget(self.allObjects, 8, 0, 1, 1)

        self.subjectList = QLabel('Subject List: ')
        LB_layout.addWidget(self.subjectList, 9, 1, 1, 1)
        self.allSubjects = QComboBox()
        LB_layout.addWidget(self.allSubjects, 10, 1, 1, 1)

        self.predicationList = QLabel('关系列表：')
        LB_layout.addWidget(self.predicationList, 9, 0, 1, 1)
        self.allPredication = QComboBox()
        LB_layout.addWidget(self.allPredication, 10, 0, 1, 1)

        self.savePre = QLabel('保存关系: ')
        LB_layout.addWidget(self.savePre, 7, 1, 1, 1)
        self.savePreB = QPushButton('Save Predication')
        LB_layout.addWidget(self.savePreB, 8, 1, 1, 1)

        self.setLayout(LB_layout)
        self.savePath.clicked.connect(self.setSavePath)
        self.saveMask.clicked.connect(self.selectedobject.saveObject)
        self.savePreB.clicked.connect(self.selectedobject.savePredication)
        self.allClass.activated.connect(self.getClassNameID)
        self.allObjects.activated.connect(self.getObjectName)
        self.allSubjects.activated.connect(self.getSubjectName)
        self.allPredication.activated.connect(self.getPredicationNameID)
        self.selectedobject.getObjectSubjectName.connect(self.getOSbjectName)
        self.GetClassName.connect(self.selectedobject.getONOID)
        self.GetObName.connect(self.selectedobject.setObjectImg)
        self.GetSubName.connect(self.selectedobject.setSubjectImg)
        self.GetPreNameId.connect(self.selectedobject.getPredicationNId)

        self.maskPath = ''

    def setSavePath(self):
        self.maskPath = QFileDialog.getExistingDirectory(self, 'set mask save path')
        self.selectedobject.maskSavePath = self.maskPath

    def getClassNameID(self):
        objectName = self.allClass.currentText()
        objectID = self.allClass.currentIndex()
        self.GetClassName.emit(objectName, objectID)

    def getPredicationNameID(self):
        predicationName = self.allPredication.currentText()
        predicationID = self.allPredication.currentIndex()
        self.GetPreNameId.emit(predicationName, predicationID)

    def getOSbjectName(self, OSbjectName):
        self.allObjects.addItem(OSbjectName)
        self.allSubjects.addItem(OSbjectName)

    def getObjectName(self):
        self.GetObName.emit(self.allObjects.currentText())

    def getSubjectName(self):
        self.GetSubName.emit(self.allSubjects.currentText())

    def clearObName(self):
        self.allObjects.clear()
        self.allSubjects.clear()


class CenterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textBrowser = MyTextBrowser()
        self.textBrowser.setFixedWidth(170)

        leftlayout = QGridLayout()
        leftlayout.addWidget(self.textBrowser, 0, 0, 5, 1)

        self.PixMap = PaintBoard()
        leftlayout.addWidget(self.PixMap, 0, 2, 5, 5)

        self.LBoard = LabelBoard()
        leftlayout.addWidget(self.LBoard, 0, 7, 3, 2)

        self.PixMap.mask_path = self.LBoard.maskPath

        self.textBrowser.SelectPicSignal.connect(self.PixMap.DrawPic)
        self.textBrowser.SelectPicSignal.connect(self.LBoard.selectedobject.getimgname)
        self.textBrowser.ClearObjectName.connect(self.LBoard.clearObName)
        self.PixMap.enterImageboard.connect(self.EnterImgBoard)
        self.PixMap.drawSelectedObject.connect(self.LBoard.selectedobject.drawSelectedObject)
        self.LBoard.ResetB.clicked.connect(self.PixMap.ResetPic)

        main_layout = QHBoxLayout()
        main_layout.addLayout(leftlayout)

        self.setLayout(main_layout)

    def EnterImgBoard(self):
        self.setFocus(Qt.MouseFocusReason)
        if self.textBrowser.Curr_Cursor is not None:
            tcf = QTextCharFormat()
            tcf.setBackground(Qt.gray)
            tcf.setForeground(Qt.black)
            self.textBrowser.Curr_Cursor.setCharFormat(tcf)


class Ui_Form(QMainWindow):
    def __init__(self):
        super().__init__()
        # 菜单栏
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('file')

        self.opendataset = QAction('&OpenDateset', self)
        self.opendataset.setShortcut('Ctrl+O')
        self.opendataset.setStatusTip('Open Dataset direction')
        self.opendataset.triggered.connect(self.Readdata)
        self.fileMenu.addAction(self.opendataset)

        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        self.statusBar()
        self.fileMenu.addAction(self.exitAction)

        self.saveImage = QAction('&Save', self)
        self.saveImage.setShortcut('Ctrl+S')
        self.saveImage.setStatusTip('Save image mask')
        self.saveImage.triggered.connect(self.SaveImg)
        self.statusBar()
        self.fileMenu.addAction(self.saveImage)

        self.readClassList = QAction('&read class list', self)
        self.readClassList.setStatusTip('select class list file')
        self.readClassList.triggered.connect(self.readClassFile)
        self.statusBar()
        self.fileMenu.addAction(self.readClassList)

        self.readPredicateList = QAction('&read predication list', self)
        self.readPredicateList.setStatusTip('select predication list file')
        self.readPredicateList.triggered.connect(self.readPredicateFile)
        self.statusBar()
        self.fileMenu.addAction(self.readPredicateList)

        # 全局布局
        self.cw = CenterWidget()
        self.pic_names = self.cw.textBrowser
        self.setCentralWidget(self.cw)

        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('LabelSG')

    def Readdata(self):
        self.cw.textBrowser.clear()
        if self.cw.textBrowser.Curr_Cursor is not None:
            tcf = QTextCharFormat()
            tcf.setBackground(Qt.white)
            tcf.setForeground(Qt.black)
            self.cw.textBrowser.Curr_Cursor.setCharFormat(tcf)

        img_path = QFileDialog.getExistingDirectory(self, 'select dataset directory')
        if img_path == '':
            return
        self.cw.PixMap.SelectedPath = img_path + '/'
        all_imgs = os.listdir(img_path)
        for img_name in all_imgs:
            self.pic_names.append(img_name)
        self.pic_names.moveCursor(QTextCursor.Start)

    def SaveImg(self):
        self.cw.PixMap.img_mask.save('aa.png')

    def readClassFile(self):
        self.cw.LBoard.allClass.clear()
        classList = []
        fileName = QFileDialog.getOpenFileName(self, '选择文件', '', 'txt files(*.txt)')
        if fileName == '':
            return
        else:
            with open(fileName[0], 'r') as f:
                data = f.readlines()
                for c in data:
                    classList.append(c.strip('\n'))
            self.cw.LBoard.allClass.addItems(classList)

    def readPredicateFile(self):
        self.cw.LBoard.allPredication.clear()
        PredicationList = []
        fileName = QFileDialog.getOpenFileName(self, '选择文件', '', 'txt files(*.txt)')
        if fileName == '':
            return
        else:
            with open(fileName[0], 'r') as f:
                data = f.readlines()
                for c in data:
                    PredicationList.append(c.strip('\n'))
            self.cw.LBoard.allPredication.addItems(PredicationList)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Form()
    ui.show()
    sys.exit(app.exec_())