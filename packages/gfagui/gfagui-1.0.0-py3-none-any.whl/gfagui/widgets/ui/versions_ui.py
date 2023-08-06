# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/versions.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(546, 180)
        self.gridLayout = QtWidgets.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.server_version = QtWidgets.QLabel(Frame)
        self.server_version.setObjectName("server_version")
        self.gridLayout.addWidget(self.server_version, 4, 1, 1, 1)
        self.api_version = QtWidgets.QLabel(Frame)
        self.api_version.setObjectName("api_version")
        self.gridLayout.addWidget(self.api_version, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.firmware_version = QtWidgets.QLabel(Frame)
        self.firmware_version.setObjectName("firmware_version")
        self.gridLayout.addWidget(self.firmware_version, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.module_version = QtWidgets.QLabel(Frame)
        self.module_version.setObjectName("module_version")
        self.gridLayout.addWidget(self.module_version, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.modulelib_version = QtWidgets.QLabel(Frame)
        self.modulelib_version.setObjectName("modulelib_version")
        self.gridLayout.addWidget(self.modulelib_version, 3, 1, 1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Versions"))
        self.label_2.setText(_translate("Frame", "API VERSION:"))
        self.label.setText(_translate("Frame", "GFASERVER VERSION:"))
        self.server_version.setText(_translate("Frame", "server_version"))
        self.api_version.setText(_translate("Frame", "api_version"))
        self.label_4.setText(_translate("Frame", "FIRMWARE VERSION:"))
        self.firmware_version.setText(_translate("Frame", "firmware_version"))
        self.label_3.setText(_translate("Frame", "GFAMODULE VERSION:"))
        self.module_version.setText(_translate("Frame", "module_version"))
        self.label_5.setText(_translate("Frame", "GFAMODULELIB VERSION:"))
        self.modulelib_version.setText(_translate("Frame", "modulelib_version"))

