# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\coding\python\chat_advanced\recode\Websocket Test\fillprofile.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
        self.bgwidget = QtWidgets.QWidget(Dialog)
        self.bgwidget.setGeometry(QtCore.QRect(0, 0, 1201, 801))
        self.bgwidget.setStyleSheet("QWidget#bgwidget{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(100, 203, 255, 255), stop:1 rgba(184, 255, 118, 255));}")
        self.bgwidget.setObjectName("bgwidget")
        self.label = QtWidgets.QLabel(self.bgwidget)
        self.label.setGeometry(QtCore.QRect(80, 50, 471, 71))
        self.label.setStyleSheet("font: 36pt \"MS Shell Dlg 2\"; color:rgb(255, 255, 255)")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.bgwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 140, 761, 41))
        self.label_2.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";color:rgb(255, 255, 255)")
        self.label_2.setObjectName("label_2")
        self.signup = QtWidgets.QPushButton(self.bgwidget)
        self.signup.setGeometry(QtCore.QRect(430, 650, 341, 51))
        self.signup.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(170, 255, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.signup.setObjectName("signup")
        self.username = QtWidgets.QLineEdit(self.bgwidget)
        self.username.setGeometry(QtCore.QRect(180, 370, 341, 51))
        self.username.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.username.setObjectName("username")
        self.firstname = QtWidgets.QLineEdit(self.bgwidget)
        self.firstname.setGeometry(QtCore.QRect(180, 450, 341, 51))
        self.firstname.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.firstname.setObjectName("firstname")
        self.label_3 = QtWidgets.QLabel(self.bgwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 370, 81, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.bgwidget)
        self.label_4.setGeometry(QtCore.QRect(80, 450, 81, 20))
        self.label_4.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        self.error = QtWidgets.QLabel(self.bgwidget)
        self.error.setGeometry(QtCore.QRect(440, 456, 341, 20))
        self.error.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color:red;")
        self.error.setText("")
        self.error.setObjectName("error")
        self.label_5 = QtWidgets.QLabel(self.bgwidget)
        self.label_5.setGeometry(QtCore.QRect(580, 450, 81, 20))
        self.label_5.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.lastname = QtWidgets.QLineEdit(self.bgwidget)
        self.lastname.setGeometry(QtCore.QRect(680, 450, 341, 51))
        self.lastname.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.lastname.setObjectName("lastname")
        self.birthday = QtWidgets.QDateEdit(self.bgwidget)
        self.birthday.setGeometry(QtCore.QRect(180, 530, 341, 51))
        self.birthday.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.birthday.setObjectName("birthday")
        self.label_6 = QtWidgets.QLabel(self.bgwidget)
        self.label_6.setGeometry(QtCore.QRect(80, 530, 81, 20))
        self.label_6.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_6.setObjectName("label_6")
        self.image = QtWidgets.QLabel(self.bgwidget)
        self.image.setGeometry(QtCore.QRect(80, 190, 151, 141))
        self.image.setStyleSheet("border-radius:50%;")
        self.image.setText("")
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.pushButton = QtWidgets.QPushButton(self.bgwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 200, 93, 28))
        self.pushButton.setStyleSheet("border-color: rgb(85, 0, 255);\n"
"background-color: rgb(170, 170, 255);")
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self.bgwidget)
        self.comboBox.setGeometry(QtCore.QRect(680, 530, 111, 51))
        self.comboBox.setStyleSheet("border-color: rgb(0, 0, 127);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_8 = QtWidgets.QLabel(self.bgwidget)
        self.label_8.setGeometry(QtCore.QRect(580, 530, 81, 20))
        self.label_8.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Fill in your profile"))
        self.label_2.setText(_translate("Dialog", "Now that you\'ve created an account, please fill in your profile."))
        self.signup.setText(_translate("Dialog", "Continue"))
        self.label_3.setText(_translate("Dialog", "Username"))
        self.label_4.setText(_translate("Dialog", "First Name"))
        self.label_5.setText(_translate("Dialog", "Last Name"))
        self.label_6.setText(_translate("Dialog", "Birthday"))
        self.pushButton.setText(_translate("Dialog", "Upload "))
        self.comboBox.setItemText(0, _translate("Dialog", "Man"))
        self.comboBox.setItemText(1, _translate("Dialog", "Woman"))
        self.comboBox.setItemText(2, _translate("Dialog", "Non-binary"))
        self.comboBox.setItemText(3, _translate("Dialog", "Other"))
        self.label_8.setText(_translate("Dialog", "Gender"))
import placeholder_rc