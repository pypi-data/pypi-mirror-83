from PyQt5.QtWidgets import QFrame

from .base import Widget
from .ui import offsets_ui


class Offset(Widget):

    def __init__(self, gfa, conf):
        super(Offset, self).__init__()
        self._gfa = gfa
        self._conf = conf

        self._offset_frame = QFrame()
        self._offset_widget = offsets_ui.Ui_Frame()
        self._offset_widget.setupUi(self._offset_frame)

        self._offset_widget.e_box.setValue(float(self._conf.offsets.value))
        self._offset_widget.f_box.setValue(float(self._conf.offsets.value))
        self._offset_widget.g_box.setValue(float(self._conf.offsets.value))
        self._offset_widget.h_box.setValue(float(self._conf.offsets.value))

        self._offset_widget.pwr_check.setChecked(self._conf.offsets.pwr)
        self._offset_widget.spd_check.setChecked(self._conf.offsets.spd)

        self._offset_widget.write_button.clicked.connect(self._on_push_write)

    def _on_push_write(self):
        self.write_offsets()

    def write_offsets(self):
        spd = self._offset_widget.spd_check.isChecked()
        pwr = self._offset_widget.pwr_check.isChecked()

        offsets = []
        offsets.append(self._offset_widget.e_box.value())
        offsets.append(self._offset_widget.f_box.value())
        offsets.append(self._offset_widget.g_box.value())
        offsets.append(self._offset_widget.h_box.value())

        for addr, value in enumerate(offsets):
            self._gfa.write_spi_offsets(addr, value, spd, pwr)


    def show(self):
        self._offset_frame.show()
