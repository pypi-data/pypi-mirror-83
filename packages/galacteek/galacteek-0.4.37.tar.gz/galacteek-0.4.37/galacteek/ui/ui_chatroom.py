# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/chatroom.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(531, 422)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.hLayoutTop = QtWidgets.QHBoxLayout()
        self.hLayoutTop.setObjectName("hLayoutTop")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hideUsersButton = QtWidgets.QPushButton(Form)
        self.hideUsersButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/share/icons/left-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideUsersButton.setIcon(icon)
        self.hideUsersButton.setObjectName("hideUsersButton")
        self.horizontalLayout.addWidget(self.hideUsersButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.usersView = QtWidgets.QTreeView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usersView.sizePolicy().hasHeightForWidth())
        self.usersView.setSizePolicy(sizePolicy)
        self.usersView.setMinimumSize(QtCore.QSize(250, 0))
        self.usersView.setObjectName("usersView")
        self.usersView.header().setVisible(False)
        self.verticalLayout_3.addWidget(self.usersView)
        self.hLayoutTop.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.hLayoutTop)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
from . import galacteek_rc
