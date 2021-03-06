# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\captcha_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 452)
        Dialog.setMinimumSize(QtCore.QSize(453, 452))
        Dialog.setMaximumSize(QtCore.QSize(693, 500))
        Dialog.setStyleSheet("#Dialog{\n"
"background-color: qlineargradient(spread:pad, x1:0.489, y1:0.0113636, x2:0.506, y2:1, stop:0 rgba(72, 72, 72, 255), stop:1 rgba(30, 30, 30, 255));\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_btc_address = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        self.lineEdit_btc_address.setFont(font)
        self.lineEdit_btc_address.setObjectName("lineEdit_btc_address")
        self.gridLayout.addWidget(self.lineEdit_btc_address, 1, 0, 1, 1)
        self.lineEdit_captcha = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        self.lineEdit_captcha.setFont(font)
        self.lineEdit_captcha.setObjectName("lineEdit_captcha")
        self.gridLayout.addWidget(self.lineEdit_captcha, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_submit = QtWidgets.QPushButton(Dialog)
        self.pushButton_submit.setStyleSheet("color: white;\n"
"background-color: maroon;\n"
"font: 10pt \"Montserrat\";")
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.gridLayout.addWidget(self.pushButton_submit, 5, 0, 1, 1)
        self.label_captcha = QtWidgets.QLabel(Dialog)
        self.label_captcha.setStyleSheet("border: 1px solid white;")
        self.label_captcha.setText("")
        self.label_captcha.setObjectName("label_captcha")
        self.gridLayout.addWidget(self.label_captcha, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Type Your BTC Address"))
        self.label.setText(_translate("Dialog", "The account balance will be credited automatically to this bitcoin address when logging out:"))
        self.pushButton_submit.setText(_translate("Dialog", "SUBMIT"))
        self.label_2.setText(_translate("Dialog", "If your session is lost your funds will be credited to this return address automatically after 24 hours.\n"
""))
        self.label_3.setText(_translate("Dialog", "Type the Code"))
