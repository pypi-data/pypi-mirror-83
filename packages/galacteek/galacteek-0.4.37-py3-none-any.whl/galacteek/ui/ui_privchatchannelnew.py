# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/privchatchannelnew.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewPrivateChatChannelDialog(object):
    def setupUi(self, NewPrivateChatChannelDialog):
        NewPrivateChatChannelDialog.setObjectName("NewPrivateChatChannelDialog")
        NewPrivateChatChannelDialog.resize(486, 313)
        self.gridLayout_2 = QtWidgets.QGridLayout(NewPrivateChatChannelDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.channelDescription = QtWidgets.QLineEdit(NewPrivateChatChannelDialog)
        self.channelDescription.setObjectName("channelDescription")
        self.gridLayout.addWidget(self.channelDescription, 1, 1, 1, 1)
        self.channelName = QtWidgets.QLineEdit(NewPrivateChatChannelDialog)
        self.channelName.setObjectName("channelName")
        self.gridLayout.addWidget(self.channelName, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(NewPrivateChatChannelDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(NewPrivateChatChannelDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(NewPrivateChatChannelDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(NewPrivateChatChannelDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.channelTopic = QtWidgets.QLineEdit(NewPrivateChatChannelDialog)
        self.channelTopic.setObjectName("channelTopic")
        self.gridLayout.addWidget(self.channelTopic, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewPrivateChatChannelDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(NewPrivateChatChannelDialog)
        QtCore.QMetaObject.connectSlotsByName(NewPrivateChatChannelDialog)

    def retranslateUi(self, NewPrivateChatChannelDialog):
        _translate = QtCore.QCoreApplication.translate
        NewPrivateChatChannelDialog.setWindowTitle(_translate("NewPrivateChatChannelDialog", "Dialog"))
        self.label_3.setText(_translate("NewPrivateChatChannelDialog", "Icon"))
        self.label.setText(_translate("NewPrivateChatChannelDialog", "Channel name"))
        self.label_2.setText(_translate("NewPrivateChatChannelDialog", "Description"))
        self.label_4.setText(_translate("NewPrivateChatChannelDialog", "Topic"))
