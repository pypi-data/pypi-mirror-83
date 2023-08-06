#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

from .widgets.ui.mainwindow_ui import Ui_MainWindow


class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
