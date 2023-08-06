import json

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame

from pyqt_tools.plot_utils import build_plot, Axis, CurveTime

from gfagui.data_logger import PIDDataLog
from .base import Widget
from .ui import pid_ui


class PIDPlot:

    def __init__(self, stacked):
        x = Axis("Time", "s")
        y = Axis("Temperature", "ºC")
        curve_names = ["Cold", "Hot", "Setpoint"]
        self._plot, self._curves = build_plot(stacked, "PID", x, y, curve_names, curve=CurveTime)

    def clear(self):
        for c in self._curves:
            c.clear()

    def new_read(self, data):
        if data["sensor1t_crc_error"] or data["sensor0t_crc_error"]:
            return

        s = ["sensor1t_value", "sensor0t_value", "setpoint"]
        for c, t in zip(self._curves, s):
            c.append(data[t])
        self._plot._plot.get_plot().set_scales("lin", "lin")


class OutputPlot:

    def __init__(self, stacked):
        x = Axis("Time", "s")
        y = Axis("Output", "%")
        curve_names = ["Output"]
        self._plot, self._curves = build_plot(stacked, "Output", x, y, curve_names, curve=CurveTime)

    def clear(self):
        for c in self._curves:
            c.clear()

    def new_read(self, data):
        self._curves[0].append(data)
        self._plot._plot.get_plot().set_scales("lin", "lin")


class PID(Widget):

    def __init__(self, gfa, signal_manager, cfg):
        super(PID, self).__init__()
        self._gfa = gfa._gfa
        self._cfg = cfg
        self._data_log = PIDDataLog()

        self._pid_frame = QFrame()
        self._pid = pid_ui.Ui_Frame()
        self._pid.setupUi(self._pid_frame)

        self._enabled_pid = None
        self._pid.enable_pid.clicked.connect(self._enable_pid)

        self._enabled_fixed_duty = None
        self._pid.enable_fixed_duty.clicked.connect(self._enable_fixed_duty)

        self._pid.get.clicked.connect(self._on_push_get)
        self._pid.set.clicked.connect(self._on_push_set)
        self._pid.clear.clicked.connect(self._on_push_clear)

        self._pid_plot = PIDPlot(self._pid.pid_plot)
        self._output_plot = OutputPlot(self._pid.output_plot)

        signal_manager.sensors.add_cb(self._pid_plot.new_read)
        signal_manager.pid.add_cb(self._pid_signal_cb)

    def show(self):
        self._refresh_status()
        self._pid_frame.show()

    def _on_push_clear(self):
        self._pid_plot.clear()
        self._output_plot.clear()

    def _pid_signal_cb(self, j):
        perc = round(j["percentage"], 3)
        error = round(j["error"], 3)
        p = round(j["p"], 3)
        i = round(j["i"], 3)
        d = round(j["d"], 3)
        last_temp = round(j["sensor1t_value"], 3)

        self._pid.percentage.setText(str(perc))
        self._pid.error.setText(str(error))
        self._pid.p_val.setText(str(p))
        self._pid.i_val.setText(str(i))
        self._pid.d_val.setText(str(d))
        self._pid.last_temp.setText(str(last_temp))

        self._pid.high_clocks.setText(str(j["high_clocks"]))
        self._pid.low_clocks.setText(str(j["low_clocks"]))

        freq = round(j["freq"], 3)
        perc = round(j["percentage"], 3)
        self._pid.frequency.setText(str(freq))
        self._pid.duty_cycle.setText(str(perc))

        hot = round(j["sensor0t_value"], 3)
        self._data_log.add_row([last_temp, hot, perc])

        self._output_plot.new_read(perc)

    def _enable_pid(self):
        if self._enabled_pid == True:
            self._gfa.pid.remote_disable()
            self._gfa.telemetry.remote_set_pwm(0)

            # Reset values
            self._pid.percentage.setText("0")
            self._pid.error.setText("0")
            self._pid.i_val.setText("0")
            self._pid.p_val.setText("0")
            self._pid.d_val.setText("0")
            self._pid.last_temp.setText("0")
        elif self._enabled_pid == False:
            self._gfa.pid.remote_enable()

        self._refresh_status()

    def _enable_fixed_duty(self):
        if self._enabled_fixed_duty == True:
            self._gfa.pid.remote_disable_fixed_duty_cycle()
        elif self._enabled_fixed_duty == False:
            self._gfa.pid.remote_enable_fixed_duty_cycle()
        self._refresh_status()

    def _on_push_get(self):
        self._refresh_status()

    def _on_push_set(self):
        self._gfa.telemetry.remote_configure_sensors_autoupdate(int(10*self._pid.auto_update_period.value()))
        self._gfa.pid.remote_set_setpoint(self._pid.setpoint.value())

        kp = self._pid.kp.value()
        ki = self._pid.ki.value()
        kd = self._pid.kd.value()
        self._gfa.pid.remote_set_components(kp, ki, kd)

        self._gfa.pid.remote_fix_duty_cycle(self._pid.fixed_duty_value.value())

        self._gfa.pid.remote_set_max_duty_cycle(self._pid.max_duty.value())

        max = self._pid.max_integral_error.value()
        min = self._pid.min_integral_error.value()
        self._gfa.pid.remote_set_integral_error_limits(max, min)

        self._refresh_status()

    def _refresh_status(self):
        pid_k = self._gfa.pid.remote_get_components().answer
        self._pid.kp.setValue(pid_k["kp"])
        self._pid.ki.setValue(pid_k["ki"])
        self._pid.kd.setValue(pid_k["kd"])

        self._pid.fixed_duty_value.setValue(self._gfa.pid.remote_get_fixed_duty_cycle().answer["duty"])

        self._pid.max_duty.setValue(self._gfa.pid.remote_get_max_duty_cycle().answer["max_duty"])

        limits = self._gfa.pid.remote_get_integral_error_limits().answer
        self._pid.max_integral_error.setValue(limits["max_error"])
        self._pid.min_integral_error.setValue(limits["min_error"])

        self._pid.setpoint.setValue(self._gfa.pid.remote_get_setpoint().answer["setpoint"])
        self._pid.auto_update_period.setValue(self._gfa.telemetry.remote_get_configured_autoupdate().answer["period"]/10)

        if self._gfa.pid.remote_is_enabled().answer["enabled"]:
            self._pid.enable_pid.setText("DISABLE")
            self._enabled_pid = True
            t = "TRUE"
        else:
            self._pid.enable_pid.setText("ENABLE")
            self._enabled_pid = False
            t = "FALSE"
        self._pid.enabled_label.setText(t)

        if self._gfa.pid.remote_is_duty_cycle_fixed().answer["fixed"]:
            self._pid.enable_fixed_duty.setText("DISABLE")
            self._enabled_fixed_duty = True
            t = "TRUE"
        else:
            self._pid.enable_fixed_duty.setText("ENABLE")
            self._enabled_fixed_duty = False
            t = "FALSE"
        self._pid.is_fixed_duty.setText(t)

        high, low = self._gfa.telemetry.remote_get_pwm_registers().answer.values()
        self._pid.high_clocks.setText(str(high))
        self._pid.low_clocks.setText(str(low))

        pwm_vals = self._gfa.telemetry.remote_get_pwm().answer
        self._pid.frequency.setText(str(pwm_vals["freq"]))
        self._pid.duty_cycle.setText(str(pwm_vals["percentage"]))

