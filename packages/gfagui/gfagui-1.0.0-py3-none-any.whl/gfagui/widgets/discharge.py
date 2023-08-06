from PyQt5.QtWidgets import QFrame

from .base import Widget
from .ui import discharge_ui


class Discharge(Widget):

    def __init__(self, gfa, conf, status):
        super(Discharge, self).__init__()
        self._gfa = gfa
        self._conf = conf
        self._status = status

        self._discharge_frame = QFrame()
        self._discharge = discharge_ui.Ui_Frame()
        self._discharge.setupUi(self._discharge_frame)

        self._discharge.duration_spin.setValue(self._conf.discharge.duration)
        self._discharge.reset_check.setChecked(self._conf.discharge.reset)
        self._discharge.pixel_check.setChecked(self._conf.discharge.pixel)

        self._discharge.enable_button.clicked.connect(self._on_push_enable)
        self._discharge.disable_button.clicked.connect(self._on_push_disable)

        self._discharge.enabled.nextCheckState = lambda: None

    def show(self):
        self._discharge_frame.show()

    def set_checkbox(self, e):
        self._discharge.enabled.setChecked(e)

    def _on_push_enable(self):
        duration = self._discharge.duration_spin.value()
        reset = self._discharge.reset_check.isChecked()
        pixel = self._discharge.pixel_check.isChecked()
        self._gfa.enable_discharge(duration, pixel, reset)
        self._discharge.enabled.setChecked(True)
        self._status.discharge(True)

    def _on_push_disable(self):
        self._gfa.disable_discharge()
        self._discharge.enabled.setChecked(False)
        self._status.discharge(False)
