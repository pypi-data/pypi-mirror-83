# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/timeframeselector.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TimeFrameSelector(object):
    def setupUi(self, TimeFrameSelector):
        TimeFrameSelector.setObjectName("TimeFrameSelector")
        TimeFrameSelector.resize(534, 57)
        TimeFrameSelector.setStyleSheet("QLabel {\n"
"    margin-left: 10px;\n"
"    margin-right: 10px;\n"
"}")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(TimeFrameSelector)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mfsTimeMetadata = QtWidgets.QCheckBox(TimeFrameSelector)
        self.mfsTimeMetadata.setObjectName("mfsTimeMetadata")
        self.horizontalLayout_2.addWidget(self.mfsTimeMetadata)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(TimeFrameSelector)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.tfIconLabel = QtWidgets.QLabel(TimeFrameSelector)
        self.tfIconLabel.setText("")
        self.tfIconLabel.setObjectName("tfIconLabel")
        self.horizontalLayout.addWidget(self.tfIconLabel)
        self.label = QtWidgets.QLabel(TimeFrameSelector)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dateFrom = QtWidgets.QDateTimeEdit(TimeFrameSelector)
        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setObjectName("dateFrom")
        self.horizontalLayout.addWidget(self.dateFrom)
        self.label_2 = QtWidgets.QLabel(TimeFrameSelector)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.dateTo = QtWidgets.QDateTimeEdit(TimeFrameSelector)
        self.dateTo.setCalendarPopup(True)
        self.dateTo.setObjectName("dateTo")
        self.horizontalLayout.addWidget(self.dateTo)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)

        self.retranslateUi(TimeFrameSelector)
        QtCore.QMetaObject.connectSlotsByName(TimeFrameSelector)

    def retranslateUi(self, TimeFrameSelector):
        _translate = QtCore.QCoreApplication.translate
        TimeFrameSelector.setWindowTitle(_translate("TimeFrameSelector", "Form"))
        self.mfsTimeMetadata.setToolTip(_translate("TimeFrameSelector", "<html><head/><body><p>Use tmestamp metadata when linking files in the MFS</p></body></html>"))
        self.mfsTimeMetadata.setText(_translate("TimeFrameSelector", "Store timestamp metadata"))
        self.label.setText(_translate("TimeFrameSelector", "Show files from date"))
        self.dateFrom.setDisplayFormat(_translate("TimeFrameSelector", "d/M/yyyy"))
        self.label_2.setText(_translate("TimeFrameSelector", "to"))
        self.dateTo.setDisplayFormat(_translate("TimeFrameSelector", "d/M/yyyy"))
