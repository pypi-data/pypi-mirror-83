# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/show_logs.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.setWindowModality(QtCore.Qt.WindowModal)
        Frame.resize(904, 686)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Frame)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table_log = QtWidgets.QTableWidget(Frame)
        self.table_log.setRowCount(0)
        self.table_log.setObjectName("table_log")
        self.table_log.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.table_log.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_log.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_log.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_log.setHorizontalHeaderItem(3, item)
        self.table_log.horizontalHeader().setStretchLastSection(True)
        self.table_log.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout.addWidget(self.table_log)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Logs"))
        self.table_log.setSortingEnabled(True)
        item = self.table_log.horizontalHeaderItem(0)
        item.setText(_translate("Frame", "DATE"))
        item = self.table_log.horizontalHeaderItem(1)
        item.setText(_translate("Frame", "MODULE"))
        item = self.table_log.horizontalHeaderItem(2)
        item.setText(_translate("Frame", "LEVEL"))
        item = self.table_log.horizontalHeaderItem(3)
        item.setText(_translate("Frame", "MESSAGE"))

