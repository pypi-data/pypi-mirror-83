# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/monitor_sensors.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(739, 531)
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Frame)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sensors = QtWidgets.QStackedWidget(self.frame)
        self.sensors.setObjectName("sensors")
        self.horizontalLayout_3.addWidget(self.sensors)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.humidity = QtWidgets.QStackedWidget(self.frame_2)
        self.humidity.setObjectName("humidity")
        self.horizontalLayout.addWidget(self.humidity)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))

