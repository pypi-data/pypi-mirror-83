from PyQt5.QtWidgets import QFrame

from pyqt_tools import table_operations

from .base import Widget
from .ui import show_logs_ui


class Logs(Widget):

    def __init__(self, gfa):
        super(Logs, self).__init__()
        self._gfa = gfa

        self._show_logs_frame = QFrame()
        self._show_logs = show_logs_ui.Ui_Frame()
        self._show_logs.setupUi(self._show_logs_frame)

    def _reload(self):
        table = self._show_logs.table_log

        log = open(self._gfa.log_file_name)
        for idx, line in enumerate(log):
            table.insertRow(idx)
            fields = line.split(" - ", 3)
            table_operations.create_item(table, idx, *fields)

    def show(self):
        self._reload()
        self._show_logs_frame.show()
