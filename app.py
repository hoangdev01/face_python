from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from imutils import paths
import pickle
import cv2
import sqlite3
import numpy as np
import warnings
import sys
import datetime
from datetime import date
from database import Database
from render import Render
import api

FACE_DISTANCE_THRESHOLE = 0.35
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

class VideoThread(QThread):

    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self, ui):
        self.ui=ui
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        render = Render("dataSet", "FaceBase.db")
        known_face_encodings = []
        known_face_names = []
        known_face_ID = []
        known_face_ID, known_face_names = render.getInfo()
        known_face_encodings=render.renderInfo()

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while self._run_flag:
            ret, cv_img = cap.read()
            small_frame = cv2.resize(cv_img, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if ret:
                if process_this_frame:
                    face_locations = api.face_locations(rgb_small_frame)
                    face_encodings = api.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        matches = api.compare_faces(known_face_encodings, face_encoding)
                        face_distances = api.face_distance(known_face_encodings, face_encoding)
                        name = "Unknown"
                        id=""
                        face_distances = api.face_distance(known_face_encodings, face_encoding)
                        if(np.amin(face_distances)>FACE_DISTANCE_THRESHOLE): continue
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            id = known_face_ID[best_match_index]
                        # face_names.append(name)
                        face_names.append(name)
                        ui.updateTable(ui,id)

                process_this_frame = not process_this_frame
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(cv_img, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(cv_img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(cv_img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                #---------------------------------
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class Ui_Dialog(QWidget):
    def setupUi(self, Dialog):
        self.camStatus=False
        self.windowWidth=691
        self.windowHeight=693
        self.dateDelay=0
        Dialog.setObjectName("Dialog")
        Dialog.resize(1228, 834)
        self.lb_openCv = QtWidgets.QLabel(Dialog)
        self.lb_openCv.setGeometry(QtCore.QRect(20, 70, 691, 631))
        self.lb_openCv.setObjectName("lb_openCv")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(740, 70, 461, 631))
        self.tableWidget.setMaximumSize(QtCore.QSize(511, 16777215))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(154)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.btn_prev = QtWidgets.QPushButton(Dialog)
        self.btn_prev.setGeometry(QtCore.QRect(690, 720, 141, 30))
        self.btn_prev.setObjectName("btn_prev")
        self.btn_next = QtWidgets.QPushButton(Dialog)
        self.btn_next.setGeometry(QtCore.QRect(1090, 720, 108, 30))
        self.btn_next.setObjectName("btn_next")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(240, 30, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lb_date = QtWidgets.QLabel(Dialog)
        self.lb_date.setGeometry(QtCore.QRect(900, 30, 331, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.lb_date.setFont(font)
        self.lb_date.setObjectName("lb_date")
        self.btn_exit = QtWidgets.QPushButton(Dialog)
        self.btn_exit.setGeometry(QtCore.QRect(1090, 780, 108, 30))
        self.btn_exit.setObjectName("btn_exit")
        # self.btn_camControl = QtWidgets.QPushButton(Dialog)
        # self.btn_camControl.setGeometry(QtCore.QRect(240, 730, 108, 30))
        # self.btn_camControl.setObjectName("btn_camControl")
        self.lb_className = QtWidgets.QLabel(Dialog)
        self.lb_className.setGeometry(QtCore.QRect(300, 30, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.lb_className.setFont(font)
        self.lb_className.setObjectName("lb_className")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.updateTable(self,0)
        self.thread = VideoThread(self)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ĐIỂM DANH"))
        self.lb_openCv.setText(_translate("Dialog", "Camera đang khởi động, vui lòng đợi trong giây lát..."))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Mã số sinh viên"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Tên"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Số điện thoại"))
        self.btn_prev.setText(_translate("Dialog", "Ngày trước"))
        self.btn_next.setText(_translate("Dialog", "Ngày sau"))
        self.label_2.setText(_translate("Dialog", "Lớp: "))
        self.lb_date.setText(_translate("Dialog", str(date.today())))
        self.btn_exit.setText(_translate("Dialog", "Thoát"))
        # self.btn_camControl.setText(_translate("Dialog", "Bật/tắt cam"))
        self.lb_className.setText(_translate("Dialog", "class name"))
        # self.btn_camControl.clicked.connect(self.btn_camControlClick)
        self.btn_prev.clicked.connect(self.prev_date)
        self.btn_next.clicked.connect(self.next_date)

    def prev_date(self):
        self.dateDelay-=1
        date = datetime.datetime.today() + datetime.timedelta(days=self.dateDelay)
        self.lb_date.setText(str(date.strftime ('%Y-%m-%d')))
        self.updateTable(self,0)
    def next_date(self):
        self.dateDelay+=1
        date = datetime.datetime.today() + datetime.timedelta(days=self.dateDelay)
        self.lb_date.setText(str(date.strftime ('%Y-%m-%d')))
        self.updateTable(self,0)

    def btn_camControlClick(self):
        if(self.camStatus==False):
            self.camStatus=True
        else:
            self.camStatus=False
        if(self.camStatus):
            self.thread = VideoThread(self)
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()
        else:
            self.thread.stop()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.lb_openCv.setPixmap(qt_img)
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.windowWidth, self.windowHeight, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @staticmethod
    def updateTable(self,id):
        db = Database("FaceBase.db")
        if id != 0:
            if id in db.getAttendanceList(0):
                return
            db.insertAttendance(id)
        class_id=1
        
        self.lb_className.setText(str(db.getClassName(class_id)))
        absent = True
        data = db.getClassTable(class_id)
        numrows = len(data)  # 6 rows in your example
        numcols = len(data[0])
        self.tableWidget.setColumnCount(numcols)
        self.tableWidget.setRowCount(numrows)
        for row in range(numrows):
            if data[row][0] in db.getAttendanceList(self.dateDelay):
                absent=False
            else: absent = True
            for column in range(numcols):
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(data[row][column]))
                if absent:
                    self.tableWidget.item(row,column).setBackground(QtGui.QColor(255,0,0))

# render=Render("dataSet","FaceBase")
# render.renderInfo()
app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())
