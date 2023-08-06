from PyQt5.QtWidgets import QFrame

from gfafunctionality.raws import RawImageMetadata

import gfagui.gfa

from .base import Widget
from .ui import ccd_ui


class CCD(Widget):

    def __init__(self, gfa):
        super(CCD, self).__init__()
        self._gfa = gfa

        self._ccd_frame = QFrame()
        self._ccd = ccd_ui.Ui_Frame()
        self._ccd.setupUi(self._ccd_frame)

        self._ccd.clear_button.clicked.connect(self._on_push_clear)
        self._ccd.dump_button.clicked.connect(self._on_push_dump)
        self._ccd.move_button.clicked.connect(self._on_push_move)

    def show(self):
        self._ccd_frame.show()

    def _on_push_clear(self):
        metadata = RawImageMetadata(1024, 1024, 32, 5, 0, 0, "NONE")
        conf = gfa.Config(metadata, is_save=False, is_clear=False, storage=gfa.Storage.dump, show_plot=False)
        self._gfa.set_config(conf)
        self._gfa.expose()

    def _on_push_dump(self):
        metadata = RawImageMetadata(1024, self._ccd.dump_lines.value(), 32, 5, 0, 0, "NONE")
        conf = gfa.Config(metadata, is_save=False, is_clear=False, storage=gfa.Storage.dump, show_plot=False)
        self._gfa.set_config(conf)
        self._gfa.expose()

    def _on_push_move(self):
        metadata = RawImageMetadata(1024, self._ccd.move_lines.value(), 32, 5, 0, 0, "NONE")
        conf = gfa.Config(metadata, is_save=False, is_clear=False, storage=gfa.Storage.move, show_plot=False)
        self._gfa.set_config(conf)
        self._gfa.expose()

