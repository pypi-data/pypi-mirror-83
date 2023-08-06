# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/adc.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(327, 224)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_3 = QtWidgets.QGridLayout(Frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.button_write = QtWidgets.QPushButton(Frame)
        self.button_write.setObjectName("button_write")
        self.gridLayout_3.addWidget(self.button_write, 2, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.line_address = QtWidgets.QLineEdit(Frame)
        self.line_address.setText("")
        self.line_address.setObjectName("line_address")
        self.gridLayout_4.addWidget(self.line_address, 0, 1, 1, 1)
        self.line_value = QtWidgets.QLineEdit(Frame)
        self.line_value.setObjectName("line_value")
        self.gridLayout_4.addWidget(self.line_value, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "ADC"))
        self.button_write.setText(_translate("Frame", "WRITE"))
        self.label_2.setText(_translate("Frame", "VALUE (hex):"))
        self.label.setText(_translate("Frame", "ADDRESS (hex):"))
        self.line_address.setInputMask(_translate("Frame", "Hhhhhhhhhhh"))
        self.line_value.setInputMask(_translate("Frame", "Hhhhhhhhhhh"))
        self.label_3.setText(_translate("Frame", "<html><head/><body><p>This widget is used to write to ADC. More information about it can be found at<br/><a href=\"http://www.ti.com/lit/ds/symlink/ads5263.pdf\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.ti.com/lit/ds/symlink/ads5263.pdf</span></a></p></body></html>"))

