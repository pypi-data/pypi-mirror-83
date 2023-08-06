# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/pwm.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(458, 178)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Frame)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frequency = QtWidgets.QSpinBox(self.frame)
        self.frequency.setReadOnly(False)
        self.frequency.setMaximum(999999)
        self.frequency.setProperty("value", 5000)
        self.frequency.setObjectName("frequency")
        self.gridLayout_2.addWidget(self.frequency, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.set_vals = QtWidgets.QPushButton(self.frame)
        self.set_vals.setObjectName("set_vals")
        self.gridLayout_2.addWidget(self.set_vals, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.duty_cycle = QtWidgets.QSpinBox(self.frame)
        self.duty_cycle.setMaximum(100)
        self.duty_cycle.setObjectName("duty_cycle")
        self.gridLayout_2.addWidget(self.duty_cycle, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 2, 1)
        self.frame_2 = QtWidgets.QFrame(self.widget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.low_clocks = QtWidgets.QSpinBox(self.frame_2)
        self.low_clocks.setMaximum(9999999)
        self.low_clocks.setObjectName("low_clocks")
        self.gridLayout_3.addWidget(self.low_clocks, 1, 1, 1, 1)
        self.set_clocks = QtWidgets.QPushButton(self.frame_2)
        self.set_clocks.setObjectName("set_clocks")
        self.gridLayout_3.addWidget(self.set_clocks, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.high_clocks = QtWidgets.QSpinBox(self.frame_2)
        self.high_clocks.setMaximum(99999999)
        self.high_clocks.setObjectName("high_clocks")
        self.gridLayout_3.addWidget(self.high_clocks, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 1, 2, 1)
        self.get = QtWidgets.QPushButton(self.widget)
        self.get.setObjectName("get")
        self.gridLayout.addWidget(self.get, 3, 0, 1, 2)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "PWM"))
        self.label_5.setText(_translate("Frame", "Frequency (Hz):"))
        self.set_vals.setText(_translate("Frame", "SET"))
        self.label_3.setText(_translate("Frame", "Duty Cycle(%):"))
        self.label_4.setText(_translate("Frame", "Low clocks:"))
        self.set_clocks.setText(_translate("Frame", "SET"))
        self.label_6.setText(_translate("Frame", "High clock:"))
        self.get.setText(_translate("Frame", "GET"))

