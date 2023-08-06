import json
from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame

from pyqt_tools.plot_utils import build_plot, Axis, CurveTime

from .base import Widget
from .ui import alarms_ui


class AlarmsPlots:

    def __init__(self, widget, gfa):
        self._w = widget
        self._gfa = gfa

        curve_names = ["Temperature", "Threshold"]
        x = Axis("Time", "s")
        y = Axis("Temperature", "ºC")
        args = ["Threshold", x, y, curve_names]
        self._fpga = build_plot(self._w.fpga_plot, *args, curve=CurveTime)
        self._s0 = build_plot(self._w.s0_plot, *args, curve=CurveTime)
        self._s1 = build_plot(self._w.s1_plot, *args, curve=CurveTime)
        self._s2 = build_plot(self._w.s2_plot, *args, curve=CurveTime)
        self._s3 = build_plot(self._w.s3_plot, *args, curve=CurveTime)

    def update(self, data):
        threshold = self._gfa.telemetry.remote_get_alarm_thresholds().answer
        self._update_plot(self._fpga, data["xadc_temp"], threshold["fpga"])
        self._update_plot(self._s0, data["sensor0t_value"], threshold["hotpeltier"])
        self._update_plot(self._s1, data["sensor1t_value"], threshold["coldpeltier"])
        self._update_plot(self._s2, data["sensor2t_value"], threshold["ambient"])
        self._update_plot(self._s3, data["sensor3t_value"], threshold["filter"])

    def _update_plot(self, plot, temperature, threshold):
        s = [temperature, threshold]

        for c, val in zip(plot[1], s):
            c.append(val)

        plot[0]._plot.get_plot().set_scales("lin", "lin")


class Alarms(Widget):
    update_plot_signal = QtCore.pyqtSignal(dict)
    update_alarms_signal = QtCore.pyqtSignal(dict)

    def __init__(self, gfa):
        super(Alarms, self).__init__()
        self._gfa = gfa._gfa

        self.update_plot_signal.connect(self._on_signal_update)
        self.update_alarms_signal.connect(self._on_signal_alarms)

        self._alarms_frame = QFrame()
        self._alarms = alarms_ui.Ui_Frame()
        self._alarms.setupUi(self._alarms_frame)
        self._alarms.set.clicked.connect(self._set)
        self._alarms.get.clicked.connect(self._get)

        self._alarms.fpga_triggered.nextCheckState = lambda: None
        self._alarms.s0_triggered.nextCheckState = lambda: None
        self._alarms.s1_triggered.nextCheckState = lambda: None
        self._alarms.s2_triggered.nextCheckState = lambda: None
        self._alarms.s3_triggered.nextCheckState = lambda: None

        self._plots = AlarmsPlots(self._alarms, self._gfa)

        self._gfa.async_manager.add_sensors_reading_callback(self._sensors_callback)
        self._gfa.async_manager.add_alarms_callback(self._alarms_callback)

        self._start = datetime.now()

    def show(self):
        self._update_values()
        self._alarms_frame.show()

    @QtCore.pyqtSlot(dict)
    def _on_signal_update(self, data):
        #self._update_values()
        return self._plots.update(data)

    def _sensors_callback(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')

        j = json.loads(data)

        self.update_plot_signal.emit(j)

    def _on_signal_alarms(self, t):
        self._alarms.fpga_triggered.setChecked(t["fpga"])
        self._alarms.s0_triggered.setChecked(t["hotpeltier"])
        self._alarms.s1_triggered.setChecked(t["coldpeltier"])
        self._alarms.s2_triggered.setChecked(t["ambient"])
        self._alarms.s3_triggered.setChecked(t["filter"])

    def _alarms_callback(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')

        j = json.loads(data)

        self.update_alarms_signal.emit(j)

    def _set(self):
        fpga_t = self._alarms.fpga_threshold.value()
        s0_t = self._alarms.s0_threshold.value()
        s1_t = self._alarms.s1_threshold.value()
        s2_t = self._alarms.s2_threshold.value()
        s3_t = self._alarms.s3_threshold.value()
        hold = self._alarms.alarm_hold.value()
        interlock_delay = self._alarms.interlock_delay.value()

        self._gfa.telemetry.remote_alarm_thresholds(fpga_t, s0_t, s1_t, s2_t, s3_t, hold, interlock_delay)

        fpga = self._alarms.fpga_enabled.isChecked()
        s0 = self._alarms.s0_enabled.isChecked()
        s1 = self._alarms.s1_enabled.isChecked()
        s2 = self._alarms.s2_enabled.isChecked()
        s3 = self._alarms.s3_enabled.isChecked()

        self._gfa.telemetry.remote_enable_alarms(fpga, s0, s1, s2, s3)

    def _get(self):
        self._update_values()

    def _update_values(self):
        alarms = self._gfa.telemetry.remote_get_enabled_alarms().answer
        fpga = alarms["fpga"]
        s0 = alarms["hotpeltier"]
        s1 = alarms["coldpeltier"]
        s2 = alarms["ambient"]
        s3 = alarms["filter"]

        thresholds = self._gfa.telemetry.remote_get_alarm_thresholds().answer
        hold = thresholds["hold_ms"]
        interlock_delay =  thresholds["interlock_delay_ms"]

        self._alarms.fpga_enabled.setChecked(fpga)
        self._alarms.s0_enabled.setChecked(s0)
        self._alarms.s1_enabled.setChecked(s1)
        self._alarms.s2_enabled.setChecked(s2)
        self._alarms.s3_enabled.setChecked(s3)
        self._alarms.alarm_hold.setValue(hold)
        self._alarms.interlock_delay.setValue(interlock_delay)

        self._alarms.fpga_threshold.setValue(thresholds["fpga"])
        self._alarms.s0_threshold.setValue(thresholds["hotpeltier"])
        self._alarms.s1_threshold.setValue(thresholds["coldpeltier"])
        self._alarms.s2_threshold.setValue(thresholds["ambient"])
        self._alarms.s3_threshold.setValue(thresholds["filter"])

        t = self._gfa.telemetry.remote_get_triggered_alarms().answer
        self._alarms.fpga_triggered.setChecked(t["fpga"])
        self._alarms.s0_triggered.setChecked(t["hotpeltier"])
        self._alarms.s1_triggered.setChecked(t["coldpeltier"])
        self._alarms.s2_triggered.setChecked(t["ambient"])
        self._alarms.s3_triggered.setChecked(t["filter"])


