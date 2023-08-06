import json

from PyQt5.QtWidgets import QFrame
from PyQt5 import QtCore

from pyqt_tools.plot_utils import build_plot, Axis, CurveTime

from .base import Widget
from .ui import monitor_sensors_ui


class TemperaturePlot:

    def __init__(self, stacked):
        x = Axis("Time", "s")
        y = Axis("Temperature", "ºC")
        curve_names = ["Hotpeltier", "Coldpeltier", "Ambient", "Filter", "FPGA"]
        self._plot, self._curves = build_plot(stacked, "Temperatures", x, y, curve_names, curve=CurveTime)

    def new_read(self, data):
        s = ["sensor0t_value", "sensor1t_value", "sensor2t_value", "sensor3t_value", "xadc_temp"]
        for c, t in zip(self._curves, s):
            c.append(data[t])
        self._plot._plot.get_plot().set_scales("lin", "lin")


class HumidityPlot:

    def __init__(self, stacked):
        x = Axis("Time", "s")
        y = Axis("Humidity", "%")
        curve_names = ["Ambient", "Filter"]
        self._plot, self._curves= build_plot(stacked, "Humidity", x, y, curve_names, curve=CurveTime)

    def new_read(self, data):
        s = ["sensor2h_value", "sensor3h_value"]
        for c, t in zip(self._curves, s):
            c.append(data[t])
        self._plot._plot.get_plot().set_scales("lin", "lin")


class MonitorSensors(Widget):
    update_temperature_plot_signal = QtCore.pyqtSignal(dict)

    def __init__(self, gfa):
        super(MonitorSensors, self).__init__()
        self._gfa = gfa._gfa

        self._ms_frame = QFrame()
        self._ms = monitor_sensors_ui.Ui_Frame()
        self._ms.setupUi(self._ms_frame)

        self.update_temperature_plot_signal.connect(self._on_signal_update)

        self._plot_temperature = TemperaturePlot(self._ms.sensors)
        self._plot_humidity = HumidityPlot(self._ms.humidity)

        self._gfa.async_manager.add_sensors_reading_callback(self._sensors_callback)

    def _sensors_callback(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')

        j = json.loads(data)

        self.update_temperature_plot_signal.emit(j)

    @QtCore.pyqtSlot(dict)
    def _on_signal_update(self, data):
        self._plot_temperature.new_read(data)
        self._plot_humidity.new_read(data)

    def show(self):
        self._ms_frame.show()
