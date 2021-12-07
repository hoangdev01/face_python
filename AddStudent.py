from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from imutils import paths
import pickle
import cv2
import face_recognition
import sqlite3 as mdb
import numpy as np
import warnings
import sys
import datetime
from datetime import date
from database import Database
from render import Render

class UI_AddStudent(QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 450)
        
        self.label_name = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_name.setFont(font)
        self.label_name.setGeometry(QtCore.QRect(50, 100, 170, 30))
        self.label_name.setObjectName("label_name")

        self.text_editname = QtWidgets.QLineEdit(Dialog)
        self.text_editname.setGeometry(QtCore.QRect(210, 100, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.text_editname.setFont(font)



        self.label_idclass = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_idclass.setFont(font)
        self.label_idclass.setGeometry(QtCore.QRect(50, 170, 170, 30))
        self.label_idclass.setObjectName("label_idclass")

        self.text_editclass = QtWidgets.QLineEdit(Dialog)
        self.text_editclass.setGeometry(QtCore.QRect(210, 170, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.text_editclass.setFont(font)


        
        self.label_phonenumber = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_phonenumber.setFont(font)
        self.label_phonenumber.setGeometry(QtCore.QRect(50, 240, 170, 30))
        self.label_phonenumber.setObjectName("label_phonenumber")

        self.text_editphonenumber = QtWidgets.QLineEdit(Dialog)
        self.text_editphonenumber.setGeometry(QtCore.QRect(210, 240, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.text_editphonenumber.setFont(font)



        self.btn_add = QtWidgets.QPushButton(Dialog)
        self.btn_add.setGeometry(QtCore.QRect(100, 350, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_add.setFont(font)
        self.btn_add.setObjectName("btn_them")

        self.btn_update = QtWidgets.QPushButton(Dialog)
        self.btn_update.setGeometry(QtCore.QRect(300, 350, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_update.setFont(font)
        self.btn_update.setObjectName("btn_sua")


        if self.btn_add.clicked.connect(self.insertDB):
            self.btn_add.clicked.connect(self.text_editname.clear)
            self.btn_add.clicked.connect(self.text_editclass.clear)
            self.btn_add.clicked.connect(self.text_editphonenumber.clear)

        if self.btn_update.clicked.connect(self.updateDB):
            self.btn_update.clicked.connect(self.text_editname.clear)
            self.btn_update.clicked.connect(self.text_editclass.clear)
            self.btn_update.clicked.connect(self.text_editphonenumber.clear)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def insertDB(self):
        con = mdb.connect('FaceBase.db')
        cursor = con.cursor()
        name = self.text_id2.text()
        class_id = self.text_id3.text()
        phone = self.text_id4.text()
        cmd = "INSERT INTO STUDENT(name, class_id,phone_number) VALUES('"+str(name)+"', "+str(class_id)+", '"+str(phone)+"')"
        cursor.execute(cmd)
        con.commit()
    
    def updateDB(self):
        con = mdb.connect('FaceBase.db')
        cursor = con.cursor()
        name = self.text_id2.text()
        class_id = self.text_id3.text()
        phone = self.text_id4.text()
        cmd = "UPDATE STUDENT SET class_id = "+str(class_id)+", phone_number = "+str(phone)+" WHERE name = '"+str(name)+"'"
        cursor.execute(cmd)
        con.commit()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Thêm sinh viên"))
        self.btn_add.setText(_translate("Dialog", "Thêm"))
        self.btn_update.setText(_translate("Dialog", "Sửa"))
        self.label_name.setText(_translate("Dialog", "Tên sinh viên:"))
        self.label_idclass.setText(_translate("Dialog", "ID Lớp:"))
        self.label_phonenumber.setText(_translate("Dialog", "Số điện thoại:"))
ui=UI_AddStudent()
ui.setupUi()

