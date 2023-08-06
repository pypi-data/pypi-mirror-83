# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/chatchannelnew.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChatChannelNewDialog(object):
    def setupUi(self, ChatChannelNewDialog):
        ChatChannelNewDialog.setObjectName("ChatChannelNewDialog")
        ChatChannelNewDialog.resize(400, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ChatChannelNewDialog.sizePolicy().hasHeightForWidth())
        ChatChannelNewDialog.setSizePolicy(sizePolicy)
        ChatChannelNewDialog.setMaximumSize(QtCore.QSize(16777215, 200))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ChatChannelNewDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ChatChannelNewDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.channelName = QtWidgets.QLineEdit(ChatChannelNewDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channelName.sizePolicy().hasHeightForWidth())
        self.channelName.setSizePolicy(sizePolicy)
        self.channelName.setMaxLength(64)
        self.channelName.setObjectName("channelName")
        self.verticalLayout.addWidget(self.channelName)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChatChannelNewDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ChatChannelNewDialog)
        QtCore.QMetaObject.connectSlotsByName(ChatChannelNewDialog)

    def retranslateUi(self, ChatChannelNewDialog):
        _translate = QtCore.QCoreApplication.translate
        ChatChannelNewDialog.setWindowTitle(_translate("ChatChannelNewDialog", "Add chat channel"))
        self.label.setText(_translate("ChatChannelNewDialog", "Channel name (use #channel)"))
