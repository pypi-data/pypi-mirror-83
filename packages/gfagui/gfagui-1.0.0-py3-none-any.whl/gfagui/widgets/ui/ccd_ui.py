# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/ccd.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.move_lines = QtWidgets.QSpinBox(Frame)
        self.move_lines.setObjectName("move_lines")
        self.gridLayout.addWidget(self.move_lines, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.clear_button = QtWidgets.QPushButton(Frame)
        self.clear_button.setObjectName("clear_button")
        self.gridLayout.addWidget(self.clear_button, 1, 0, 1, 1)
        self.dump_lines = QtWidgets.QSpinBox(Frame)
        self.dump_lines.setObjectName("dump_lines")
        self.gridLayout.addWidget(self.dump_lines, 3, 1, 1, 1)
        self.dump_button = QtWidgets.QPushButton(Frame)
        self.dump_button.setObjectName("dump_button")
        self.gridLayout.addWidget(self.dump_button, 3, 2, 1, 1)
        self.move_button = QtWidgets.QPushButton(Frame)
        self.move_button.setObjectName("move_button")
        self.gridLayout.addWidget(self.move_button, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "CCD"))
        self.label.setText(_translate("Frame", "Number of lines:"))
        self.clear_button.setText(_translate("Frame", "CLEAR CCD"))
        self.dump_button.setText(_translate("Frame", "DUMP"))
        self.move_button.setText(_translate("Frame", "MOVE"))
        self.label_2.setText(_translate("Frame", "Number of lines:"))

