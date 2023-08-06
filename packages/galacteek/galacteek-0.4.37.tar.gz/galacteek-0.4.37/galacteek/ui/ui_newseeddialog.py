# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/newseeddialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewSeedDialog(object):
    def setupUi(self, NewSeedDialog):
        NewSeedDialog.setObjectName("NewSeedDialog")
        NewSeedDialog.resize(497, 427)
        self.gridLayout_2 = QtWidgets.QGridLayout(NewSeedDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(NewSeedDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.bLayout = QtWidgets.QVBoxLayout()
        self.bLayout.setObjectName("bLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fromClipboardButton = QtWidgets.QToolButton(NewSeedDialog)
        self.fromClipboardButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/share/icons/clipboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fromClipboardButton.setIcon(icon)
        self.fromClipboardButton.setObjectName("fromClipboardButton")
        self.horizontalLayout.addWidget(self.fromClipboardButton)
        self.labelDrop = QtWidgets.QLabel(NewSeedDialog)
        font = QtGui.QFont()
        font.setFamily("Lucida")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelDrop.setFont(font)
        self.labelDrop.setTextFormat(QtCore.Qt.RichText)
        self.labelDrop.setObjectName("labelDrop")
        self.horizontalLayout.addWidget(self.labelDrop, 0, QtCore.Qt.AlignHCenter)
        self.bLayout.addLayout(self.horizontalLayout)
        self.files = QtWidgets.QTreeWidget(NewSeedDialog)
        self.files.setAcceptDrops(True)
        self.files.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.files.setColumnCount(5)
        self.files.setObjectName("files")
        self.files.header().setMinimumSectionSize(50)
        self.files.header().setStretchLastSection(True)
        self.bLayout.addWidget(self.files)
        self.gridLayout_2.addLayout(self.bLayout, 2, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(NewSeedDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtWidgets.QLineEdit(NewSeedDialog)
        self.name.setMaxLength(128)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(NewSeedDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(NewSeedDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.description = QtWidgets.QLineEdit(NewSeedDialog)
        self.description.setMaxLength(128)
        self.description.setObjectName("description")
        self.gridLayout.addWidget(self.description, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(NewSeedDialog)
        QtCore.QMetaObject.connectSlotsByName(NewSeedDialog)

    def retranslateUi(self, NewSeedDialog):
        _translate = QtCore.QCoreApplication.translate
        NewSeedDialog.setWindowTitle(_translate("NewSeedDialog", "New seed"))
        self.fromClipboardButton.setToolTip(_translate("NewSeedDialog", "Load file from clipboard"))
        self.labelDrop.setText(_translate("NewSeedDialog", "<html><head/><body><p>Drag-and-drop files from the filemanager</p></body></html>"))
        self.files.headerItem().setText(0, _translate("NewSeedDialog", "Filename"))
        self.files.headerItem().setText(1, _translate("NewSeedDialog", "Pin (min)"))
        self.files.headerItem().setText(2, _translate("NewSeedDialog", "Pin (target)"))
        self.files.headerItem().setText(4, _translate("NewSeedDialog", "*"))
        self.label.setText(_translate("NewSeedDialog", "Seed name"))
        self.label_4.setText(_translate("NewSeedDialog", "Description"))
        self.label_3.setText(_translate("NewSeedDialog", "Icon"))
from . import galacteek_rc
