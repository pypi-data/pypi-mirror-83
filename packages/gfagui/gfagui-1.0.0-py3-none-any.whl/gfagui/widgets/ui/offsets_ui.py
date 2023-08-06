# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/offsets.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(264, 147)
        self.gridLayout = QtWidgets.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.pwr_check = QtWidgets.QCheckBox(Frame)
        self.pwr_check.setObjectName("pwr_check")
        self.gridLayout.addWidget(self.pwr_check, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.g_box = QtWidgets.QSpinBox(Frame)
        self.g_box.setMaximum(4096)
        self.g_box.setObjectName("g_box")
        self.gridLayout.addWidget(self.g_box, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.h_box = QtWidgets.QSpinBox(Frame)
        self.h_box.setMaximum(4096)
        self.h_box.setObjectName("h_box")
        self.gridLayout.addWidget(self.h_box, 1, 3, 1, 1)
        self.e_box = QtWidgets.QSpinBox(Frame)
        self.e_box.setMaximum(4096)
        self.e_box.setObjectName("e_box")
        self.gridLayout.addWidget(self.e_box, 0, 1, 1, 1)
        self.f_box = QtWidgets.QSpinBox(Frame)
        self.f_box.setMaximum(4096)
        self.f_box.setObjectName("f_box")
        self.gridLayout.addWidget(self.f_box, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.spd_check = QtWidgets.QCheckBox(Frame)
        self.spd_check.setObjectName("spd_check")
        self.gridLayout.addWidget(self.spd_check, 2, 3, 1, 1)
        self.write_button = QtWidgets.QPushButton(Frame)
        self.write_button.setObjectName("write_button")
        self.gridLayout.addWidget(self.write_button, 3, 1, 1, 3)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Offsets"))
        self.label_3.setText(_translate("Frame", "G:"))
        self.pwr_check.setText(_translate("Frame", "PWR"))
        self.label_2.setText(_translate("Frame", "F:"))
        self.label.setText(_translate("Frame", "E:"))
        self.label_4.setText(_translate("Frame", "H:"))
        self.spd_check.setText(_translate("Frame", "SPD"))
        self.write_button.setText(_translate("Frame", "WRITE"))

