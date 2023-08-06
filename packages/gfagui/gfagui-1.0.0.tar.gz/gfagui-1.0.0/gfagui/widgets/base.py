import abc

from PyQt5.QtCore import QObject


class Widget(QObject):

    @abc.abstractclassmethod
    def show(self):
        pass
