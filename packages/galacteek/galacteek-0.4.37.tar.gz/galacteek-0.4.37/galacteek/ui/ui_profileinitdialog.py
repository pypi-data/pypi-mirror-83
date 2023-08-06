# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/profileinitdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProfileInitDialog(object):
    def setupUi(self, ProfileInitDialog):
        ProfileInitDialog.setObjectName("ProfileInitDialog")
        ProfileInitDialog.resize(627, 477)
        ProfileInitDialog.setMaximumSize(QtCore.QSize(900, 16777215))
        ProfileInitDialog.setStyleSheet("QLineEdit, QLabel {\n"
"padding: 5px;\n"
"}\n"
"\n"
"QDialog {\n"
"margin-left: 20px;\n"
"margin-right: 20px;\n"
"}")
        self.gridLayout_2 = QtWidgets.QGridLayout(ProfileInitDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ipidRsaPassphraseVerifCheck = QtWidgets.QLabel(ProfileInitDialog)
        self.ipidRsaPassphraseVerifCheck.setText("")
        self.ipidRsaPassphraseVerifCheck.setObjectName("ipidRsaPassphraseVerifCheck")
        self.gridLayout.addWidget(self.ipidRsaPassphraseVerifCheck, 7, 2, 1, 1)
        self.ipidRsaKeySize = QtWidgets.QComboBox(ProfileInitDialog)
        self.ipidRsaKeySize.setObjectName("ipidRsaKeySize")
        self.ipidRsaKeySize.addItem("")
        self.ipidRsaKeySize.addItem("")
        self.gridLayout.addWidget(self.ipidRsaKeySize, 4, 1, 1, 1)
        self.ipidRsaPassphraseCheck = QtWidgets.QLabel(ProfileInitDialog)
        self.ipidRsaPassphraseCheck.setText("")
        self.ipidRsaPassphraseCheck.setObjectName("ipidRsaPassphraseCheck")
        self.gridLayout.addWidget(self.ipidRsaPassphraseCheck, 6, 2, 1, 1)
        self.generateRandom = QtWidgets.QPushButton(ProfileInitDialog)
        self.generateRandom.setObjectName("generateRandom")
        self.gridLayout.addWidget(self.generateRandom, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(ProfileInitDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(ProfileInitDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(ProfileInitDialog)
        self.cancelButton.setMaximumSize(QtCore.QSize(600, 16777215))
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 9, 0, 1, 1)
        self.ipidRsaPassphraseVerifLabel = QtWidgets.QLabel(ProfileInitDialog)
        self.ipidRsaPassphraseVerifLabel.setObjectName("ipidRsaPassphraseVerifLabel")
        self.gridLayout.addWidget(self.ipidRsaPassphraseVerifLabel, 7, 0, 1, 1)
        self.ipidRsaPassphrase = QtWidgets.QLineEdit(ProfileInitDialog)
        self.ipidRsaPassphrase.setObjectName("ipidRsaPassphrase")
        self.gridLayout.addWidget(self.ipidRsaPassphrase, 6, 1, 1, 1)
        self.username = QtWidgets.QLineEdit(ProfileInitDialog)
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 2, 1, 1, 1)
        self.ipidRsaPassphraseLabel = QtWidgets.QLabel(ProfileInitDialog)
        self.ipidRsaPassphraseLabel.setObjectName("ipidRsaPassphraseLabel")
        self.gridLayout.addWidget(self.ipidRsaPassphraseLabel, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 8, 1, 1, 1)
        self.useIpidPassphrase = QtWidgets.QCheckBox(ProfileInitDialog)
        self.useIpidPassphrase.setObjectName("useIpidPassphrase")
        self.gridLayout.addWidget(self.useIpidPassphrase, 5, 0, 1, 1)
        self.ipidRsaPassphraseVerif = QtWidgets.QLineEdit(ProfileInitDialog)
        self.ipidRsaPassphraseVerif.setObjectName("ipidRsaPassphraseVerif")
        self.gridLayout.addWidget(self.ipidRsaPassphraseVerif, 7, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(ProfileInitDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.okButton = QtWidgets.QPushButton(ProfileInitDialog)
        self.okButton.setMaximumSize(QtCore.QSize(300, 16777215))
        self.okButton.setObjectName("okButton")
        self.gridLayout.addWidget(self.okButton, 9, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(ProfileInitDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)

        self.retranslateUi(ProfileInitDialog)
        QtCore.QMetaObject.connectSlotsByName(ProfileInitDialog)

    def retranslateUi(self, ProfileInitDialog):
        _translate = QtCore.QCoreApplication.translate
        ProfileInitDialog.setWindowTitle(_translate("ProfileInitDialog", "IPID generator"))
        self.ipidRsaKeySize.setItemText(0, _translate("ProfileInitDialog", "4096"))
        self.ipidRsaKeySize.setItemText(1, _translate("ProfileInitDialog", "2048"))
        self.generateRandom.setText(_translate("ProfileInitDialog", "Generate random user"))
        self.label_2.setText(_translate("ProfileInitDialog", "Username"))
        self.label_3.setText(_translate("ProfileInitDialog", "Virtual planet"))
        self.cancelButton.setText(_translate("ProfileInitDialog", "Cancel"))
        self.ipidRsaPassphraseVerifLabel.setText(_translate("ProfileInitDialog", "Repeat passphrase"))
        self.ipidRsaPassphraseLabel.setText(_translate("ProfileInitDialog", "Passphrase"))
        self.useIpidPassphrase.setText(_translate("ProfileInitDialog", "Protect RSA key with a passphrase"))
        self.label_4.setText(_translate("ProfileInitDialog", "IPID RSA key size"))
        self.okButton.setText(_translate("ProfileInitDialog", "OK"))
        self.label.setText(_translate("ProfileInitDialog", "<html><head/><body><p><span style=\" font-size:18pt;\">Create your Decentralized Identity (DID)</span></p></body></html>"))
