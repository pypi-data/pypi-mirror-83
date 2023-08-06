# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(QtWidgets.QWidget):
   def __init__(self, parent=None):
      QtWidgets.QWidget.__init__(self, parent)
      self.setObjectName("Telemetry widget")
