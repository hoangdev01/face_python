from os import name
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from imutils import paths
from tkinter import Tk
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

class UI_AddClass(QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 300)


        self.label_classname = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_classname.setFont(font)
        self.label_classname.setGeometry(QtCore.QRect(10, 110, 120, 30))
        self.label_classname.setObjectName("label_classname")

        self.text_editclassname = QtWidgets.QLineEdit(Dialog)
        self.text_editclassname.setGeometry(QtCore.QRect(100, 110, 180, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.text_editclassname.setFont(font)
        self.text_editclassname.setObjectName("text_editclassname")

        self.btn_ok = QtWidgets.QPushButton(Dialog)
        self.btn_ok.setGeometry(QtCore.QRect(130, 210, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_ok.setFont(font)
        self.btn_ok.setObjectName("btn_ok")

    
        
        self.btn_ok.clicked.connect(self.insertDB)
        if self.btn_ok.clicked :   
            self.btn_ok.clicked.connect(self.text_editclassname.clear)
            
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def insertDB(self,name):
        con = mdb.connect('FaceBase.db')
        cursor = con.cursor()
        name = self.text_editclassname.text()
        cmd = "INSERT INTO CLASS_INFO(name) VALUES('"+str(name)+"')"
        cursor.execute(cmd)
        con.commit()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Thêm lớp"))
        self.btn_ok.setText(_translate("Dialog", "Thêm"))
        # self.label_1.setText(_translate("Dialog", "ID Lớp:"))
        self.label_classname.setText(_translate("Dialog", "Tên Lớp:"))

