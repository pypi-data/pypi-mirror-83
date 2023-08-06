from PyQt5.QtWidgets import QCheckBox


class QCheckBoxReadOnly(QCheckBox):

    def __init__(self, parent):
        super(QCheckBoxReadOnly, self).__init__(parent)

        self.nextCheckState = lambda: None
