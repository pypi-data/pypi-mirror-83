# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/mfsoptionsdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MFSImportOptionsDialog(object):
    def setupUi(self, MFSImportOptionsDialog):
        MFSImportOptionsDialog.setObjectName("MFSImportOptionsDialog")
        MFSImportOptionsDialog.resize(555, 380)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(MFSImportOptionsDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(MFSImportOptionsDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.wrap = QtWidgets.QCheckBox(self.groupBox)
        self.wrap.setObjectName("wrap")
        self.gridLayout_2.addWidget(self.wrap, 0, 0, 1, 1)
        self.hiddenFiles = QtWidgets.QCheckBox(self.groupBox)
        self.hiddenFiles.setObjectName("hiddenFiles")
        self.gridLayout_2.addWidget(self.hiddenFiles, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.filestore = QtWidgets.QCheckBox(self.groupBox)
        self.filestore.setObjectName("filestore")
        self.gridLayout_3.addWidget(self.filestore, 1, 0, 1, 1)
        self.rawLeaves = QtWidgets.QCheckBox(self.groupBox)
        self.rawLeaves.setObjectName("rawLeaves")
        self.gridLayout_3.addWidget(self.rawLeaves, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(MFSImportOptionsDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gitignore = QtWidgets.QCheckBox(self.groupBox_2)
        self.gitignore.setObjectName("gitignore")
        self.gridLayout_4.addWidget(self.gitignore, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(MFSImportOptionsDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tsMetadata = QtWidgets.QCheckBox(self.groupBox_3)
        self.tsMetadata.setObjectName("tsMetadata")
        self.gridLayout_7.addWidget(self.tsMetadata, 0, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(MFSImportOptionsDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(MFSImportOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(MFSImportOptionsDialog)

    def retranslateUi(self, MFSImportOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        MFSImportOptionsDialog.setWindowTitle(_translate("MFSImportOptionsDialog", "Import options"))
        self.groupBox.setTitle(_translate("MFSImportOptionsDialog", "General options"))
        self.wrap.setToolTip(_translate("MFSImportOptionsDialog", "<html><head/><body><p>Wrap added files/directories with a directory</p></body></html>"))
        self.wrap.setText(_translate("MFSImportOptionsDialog", "Wrap with directory"))
        self.hiddenFiles.setToolTip(_translate("MFSImportOptionsDialog", "<html><head/><body><p>Import hidden files from the directory</p></body></html>"))
        self.hiddenFiles.setText(_translate("MFSImportOptionsDialog", "Import hidden files"))
        self.filestore.setToolTip(_translate("MFSImportOptionsDialog", "<html><head/><body><p>Use the IPFS filestore (avoids duplicating files)</p></body></html>"))
        self.filestore.setText(_translate("MFSImportOptionsDialog", "Use filestore"))
        self.rawLeaves.setToolTip(_translate("MFSImportOptionsDialog", "<html><head/><body><p>Use raw blocks for leaf nodes</p></body></html>"))
        self.rawLeaves.setText(_translate("MFSImportOptionsDialog", "Use raw leaves"))
        self.groupBox_2.setTitle(_translate("MFSImportOptionsDialog", "Misc"))
        self.gitignore.setToolTip(_translate("MFSImportOptionsDialog", "<html><head/><body><p>Load the git ignore rules file if present</p></body></html>"))
        self.gitignore.setText(_translate("MFSImportOptionsDialog", "Use gitignore rules file"))
        self.groupBox_3.setTitle(_translate("MFSImportOptionsDialog", "MFS"))
        self.tsMetadata.setToolTip(_translate("MFSImportOptionsDialog", "<html><head/><body><p>Store timestamp metadata in the MFS link</p></body></html>"))
        self.tsMetadata.setText(_translate("MFSImportOptionsDialog", "MFS: use timestamp metadata"))
