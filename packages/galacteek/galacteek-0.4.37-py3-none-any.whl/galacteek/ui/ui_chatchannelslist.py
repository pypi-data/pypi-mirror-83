# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/chatchannelslist.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChannelsListDialog(object):
    def setupUi(self, ChannelsListDialog):
        ChannelsListDialog.setObjectName("ChannelsListDialog")
        ChannelsListDialog.resize(481, 401)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ChannelsListDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(ChannelsListDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.searchLine = QtWidgets.QLineEdit(ChannelsListDialog)
        self.searchLine.setObjectName("searchLine")
        self.horizontalLayout_2.addWidget(self.searchLine)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.channelsView = QtWidgets.QTreeView(ChannelsListDialog)
        self.channelsView.setObjectName("channelsView")
        self.channelsView.header().setDefaultSectionSize(200)
        self.channelsView.header().setMinimumSectionSize(150)
        self.verticalLayout.addWidget(self.channelsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancelButton = QtWidgets.QPushButton(ChannelsListDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.joinButton = QtWidgets.QPushButton(ChannelsListDialog)
        self.joinButton.setObjectName("joinButton")
        self.horizontalLayout.addWidget(self.joinButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ChannelsListDialog)
        QtCore.QMetaObject.connectSlotsByName(ChannelsListDialog)

    def retranslateUi(self, ChannelsListDialog):
        _translate = QtCore.QCoreApplication.translate
        ChannelsListDialog.setWindowTitle(_translate("ChannelsListDialog", "Join channel"))
        self.label_2.setText(_translate("ChannelsListDialog", "Search"))
        self.cancelButton.setText(_translate("ChannelsListDialog", "Cancel"))
        self.joinButton.setText(_translate("ChannelsListDialog", "Join"))
