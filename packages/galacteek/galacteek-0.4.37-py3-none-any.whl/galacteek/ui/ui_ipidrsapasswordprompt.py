# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/ipidrsapasswordprompt.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PasswordPrompt(object):
    def setupUi(self, PasswordPrompt):
        PasswordPrompt.setObjectName("PasswordPrompt")
        PasswordPrompt.resize(669, 228)
        self.gridLayout_2 = QtWidgets.QGridLayout(PasswordPrompt)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.password = QtWidgets.QLineEdit(PasswordPrompt)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(PasswordPrompt)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(PasswordPrompt)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.forgotPwdButton = QtWidgets.QPushButton(PasswordPrompt)
        self.forgotPwdButton.setObjectName("forgotPwdButton")
        self.gridLayout.addWidget(self.forgotPwdButton, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(PasswordPrompt)
        QtCore.QMetaObject.connectSlotsByName(PasswordPrompt)

    def retranslateUi(self, PasswordPrompt):
        _translate = QtCore.QCoreApplication.translate
        PasswordPrompt.setWindowTitle(_translate("PasswordPrompt", "IPID password prompt"))
        self.label_2.setText(_translate("PasswordPrompt", "Your RSA private key is password-protected"))
        self.label.setText(_translate("PasswordPrompt", "RSA passphrase"))
        self.forgotPwdButton.setText(_translate("PasswordPrompt", "I forgot my password"))
from . import galacteek_rc
