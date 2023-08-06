from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame

from .base import Widget
from .ui import pwm_ui


class PWM(Widget):

    def __init__(self, gfa):
        super(PWM, self).__init__()
        self._gfa = gfa

        self._pwm_frame = QFrame()
        self._pwm_widget = pwm_ui.Ui_Frame()
        self._pwm_widget.setupUi(self._pwm_frame)

        self._pwm_widget.set_vals.clicked.connect(self._on_push_set_vals)
        self._pwm_widget.set_clocks.clicked.connect(self._on_push_set_clocks)
        self._pwm_widget.get.clicked.connect(self._on_push_get)

    def show(self):
        self._on_push_get()
        self._pwm_frame.show()

    @QtCore.pyqtSlot()
    def _on_push_set_vals(self):
        duty = self._pwm_widget.duty_cycle.value()
        freq = self._pwm_widget.frequency.value()
        self._gfa._gfa.telemetry.remote_force_pwm(duty, freq)
        self._on_push_get()

    @QtCore.pyqtSlot()
    def _on_push_set_clocks(self):
        high = self._pwm_widget.high_clocks.value()
        low = self._pwm_widget.low_clocks.value()
        self._gfa._gfa.telemetry.remote_force_pwm_raw(high, low)
        self._on_push_get()

    @QtCore.pyqtSlot()
    def _on_push_get(self):
        pwm = self._gfa._gfa.telemetry.remote_get_pwm().answer
        self._pwm_widget.frequency.setValue(pwm["freq"])
        self._pwm_widget.duty_cycle.setValue(pwm["percentage"])

        pwm = self._gfa._gfa.telemetry.remote_get_pwm_registers().answer
        self._pwm_widget.high_clocks.setValue(pwm["high_clocks"])
        self._pwm_widget.low_clocks.setValue(pwm["low_clocks"])

