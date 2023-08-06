# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/peersmgr.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PeersManager(object):
    def setupUi(self, PeersManager):
        PeersManager.setObjectName("PeersManager")
        PeersManager.resize(639, 422)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PeersManager)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.hLayoutTop = QtWidgets.QHBoxLayout()
        self.hLayoutTop.setObjectName("hLayoutTop")
        self.label = QtWidgets.QLabel(PeersManager)
        self.label.setObjectName("label")
        self.hLayoutTop.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hLayoutTop.addItem(spacerItem)
        self.verticalLayout.addLayout(self.hLayoutTop)
        self.peersMgrView = QtWidgets.QTreeView(PeersManager)
        self.peersMgrView.setObjectName("peersMgrView")
        self.peersMgrView.header().setVisible(False)
        self.verticalLayout.addWidget(self.peersMgrView)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(PeersManager)
        QtCore.QMetaObject.connectSlotsByName(PeersManager)

    def retranslateUi(self, PeersManager):
        _translate = QtCore.QCoreApplication.translate
        PeersManager.setWindowTitle(_translate("PeersManager", "Form"))
        self.label.setText(_translate("PeersManager", "Right-click/double-click on a peer to discover IP services"))
