# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/discharge.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(248, 175)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_2 = QtWidgets.QGridLayout(Frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.enable_button = QtWidgets.QPushButton(Frame)
        self.enable_button.setObjectName("enable_button")
        self.gridLayout_2.addWidget(self.enable_button, 0, 0, 1, 1)
        self.disable_button = QtWidgets.QPushButton(Frame)
        self.disable_button.setObjectName("disable_button")
        self.gridLayout_2.addWidget(self.disable_button, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Frame)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.pixel_check = QtWidgets.QCheckBox(self.groupBox)
        self.pixel_check.setObjectName("pixel_check")
        self.gridLayout.addWidget(self.pixel_check, 3, 1, 1, 1)
        self.duration_spin = QtWidgets.QSpinBox(self.groupBox)
        self.duration_spin.setMaximum(256)
        self.duration_spin.setSingleStep(10)
        self.duration_spin.setObjectName("duration_spin")
        self.gridLayout.addWidget(self.duration_spin, 2, 1, 1, 1)
        self.reset_check = QtWidgets.QCheckBox(self.groupBox)
        self.reset_check.setObjectName("reset_check")
        self.gridLayout.addWidget(self.reset_check, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 2, 0, 1, 2)
        self.enabled = QtWidgets.QCheckBox(Frame)
        self.enabled.setObjectName("enabled")
        self.gridLayout_2.addWidget(self.enabled, 1, 0, 1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Discharge"))
        self.enable_button.setText(_translate("Frame", "ENABLE"))
        self.disable_button.setText(_translate("Frame", "DISABLE"))
        self.groupBox.setTitle(_translate("Frame", "Settings"))
        self.label.setText(_translate("Frame", "Duration (ns):"))
        self.pixel_check.setText(_translate("Frame", "Pixel"))
        self.reset_check.setText(_translate("Frame", "Reset"))
        self.enabled.setText(_translate("Frame", "Is enabled"))

