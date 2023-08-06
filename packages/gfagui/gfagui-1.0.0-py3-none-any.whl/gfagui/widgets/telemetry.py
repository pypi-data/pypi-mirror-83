import json

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QLabel

from .base import Widget
from .ui import telemetry_ui


class Telemetry(Widget):
    update_telemetry_signal = QtCore.pyqtSignal(dict)

    def __init__(self, gfa):
        super(Telemetry, self).__init__()
        self._gfa = gfa
        self._text = ""

        self.update_telemetry_signal.connect(self._on_signal_update)

        self._telemetry_frame = QFrame()
        self._telemetry = telemetry_ui.Ui_Frame()
        self._telemetry.setupUi(self._telemetry_frame)

        self._telemetry.get_telemetry.clicked.connect(
            self._gfa.request_telemetry)

        self._telemetry.get_settings.clicked.connect(self._get_settings)
        self._telemetry.set_settings.clicked.connect(self._set_settings)

        self._gfa._gfa.async_manager.add_telemetry_callback(self._telemetry_callback)

    def _get_settings(self):
        answer = self._gfa._gfa.telemetry.remote_get_voltage_telem_settings().answer
        self._telemetry.udelay.setValue(answer["delay_us"])
        self._telemetry.reference.setChecked(answer["reference_enabled"])

        ans = self._gfa._gfa.telemetry.remote_get_voltage_telem_spi_settings().answer
        self._telemetry.half_sclk_period.setValue(ans["half_sclk_period"])
        self._telemetry.before_spi_access.setValue(ans["before_spi_access"])

    def _set_settings(self):
        d = self._telemetry.udelay.value()
        r = self._telemetry.reference.isChecked()
        self._gfa._gfa.telemetry.remote_set_voltage_telem_settings(d, r)

        h = self._telemetry.half_sclk_period.value()
        b = self._telemetry.before_spi_access.value()
        self._gfa._gfa.telemetry.remote_set_voltage_telem_spi_settings(h, b)

    def _get_vlt(self, name):
        vlt = self._gfa._gfa.telemetry.ccd_voltages
        if not vlt:
            return vlt

        t = vlt.get(name)
        if not t:
            return t

        voltage = t.value
        return round(voltage, 3)

    @QtCore.pyqtSlot(dict)
    def _on_signal_update(self, data):
        self._gfa._gfa.telemetry.ccd_voltages.update(data, True)

        def update_voltage(name):
            vlt_val = self._get_vlt(name)
            if vlt_val:
                getattr(self._telemetry, name).setText(str(vlt_val))

        for l in self._telemetry.frame.findChildren(QLabel):
            update_voltage(l.objectName())

        """
        return

        self._telemetry.vss.setText(self._get_vlt("vss"))
        self._telemetry.rd.setText(self._get_vlt("rd"))
        self._telemetry.dd.setText(self._get_vlt("dd"))
        self._telemetry.og.setText(self._get_vlt("og"))
        self._telemetry.ode.setText(self._get_vlt("ode"))
        self._telemetry.odf.setText(self._get_vlt("odf"))
        self._telemetry.odg.setText(self._get_vlt("odg"))
        self._telemetry.odh.setText(self._get_vlt("odh"))

        self._telemetry.a1_high.setText(self._get_vlt("a1_high"))
        self._telemetry.a1_low.setText(self._get_vlt("a1_low"))

        self._telemetry.a2_high.setText(self._get_vlt("a2_high"))
        self._telemetry.a2_low.setText(self._get_vlt("a2_low"))

        self._telemetry.a3_high.setText(self._get_vlt("a3_high"))
        self._telemetry.a3_low.setText(self._get_vlt("a3_low"))

        self._telemetry.a4_high.setText(self._get_vlt("a4_high"))
        self._telemetry.a4_low.setText(self._get_vlt("a4_low"))

        self._telemetry.b1_high.setText(self._get_vlt("b1_high"))
        self._telemetry.b1_low.setText(self._get_vlt("b1_low"))

        self._telemetry.b2_high.setText(self._get_vlt("b2_high"))
        self._telemetry.b2_low.setText(self._get_vlt("b2_low"))

        self._telemetry.b3_high.setText(self._get_vlt("b3_high"))
        self._telemetry.b3_low.setText(self._get_vlt("b3_low"))

        self._telemetry.b4_high.setText(self._get_vlt("b4_high"))
        self._telemetry.b4_low.setText(self._get_vlt("b4_low"))

        self._telemetry.c1_high.setText(self._get_vlt("c1_high"))
        self._telemetry.c1_low.setText(self._get_vlt("c1_low"))

        self._telemetry.c2_high.setText(self._get_vlt("c2_high"))
        self._telemetry.c2_low.setText(self._get_vlt("c2_low"))

        self._telemetry.c3_high.setText(self._get_vlt("c3_high"))
        self._telemetry.c3_low.setText(self._get_vlt("c3_low"))

        self._telemetry.c4_high.setText(self._get_vlt("c4_high"))
        self._telemetry.c4_low.setText(self._get_vlt("c4_low"))

        self._telemetry.d1_high.setText(self._get_vlt("d1_high"))
        self._telemetry.d1_low.setText(self._get_vlt("d1_low"))

        self._telemetry.d2_high.setText(self._get_vlt("d2_high"))
        self._telemetry.d2_low.setText(self._get_vlt("d2_low"))

        self._telemetry.d3_high.setText(self._get_vlt("d3_high"))
        self._telemetry.d3_low.setText(self._get_vlt("d3_low"))

        self._telemetry.d4_high.setText(self._get_vlt("d4_high"))
        self._telemetry.d4_low.setText(self._get_vlt("d4_low"))

        self._telemetry.e1_high.setText(self._get_vlt("e1_high"))
        self._telemetry.e1_low.setText(self._get_vlt("e1_low"))

        self._telemetry.e2_high.setText(self._get_vlt("e2_high"))
        self._telemetry.e2_low.setText(self._get_vlt("e2_low"))

        self._telemetry.e3f3_high.setText(self._get_vlt("e3f3_high"))
        self._telemetry.e3f3_low.setText(self._get_vlt("e3f3_low"))

        self._telemetry.f1_high.setText(self._get_vlt("f1_high"))
        self._telemetry.f1_low.setText(self._get_vlt("f1_low"))

        self._telemetry.f2_high.setText(self._get_vlt("f2_high"))
        self._telemetry.f2_low.setText(self._get_vlt("f2_low"))

        self._telemetry.g1_high.setText(self._get_vlt("g1_high"))
        self._telemetry.g1_low.setText(self._get_vlt("g1_low"))

        self._telemetry.g2_high.setText(self._get_vlt("g2_high"))
        self._telemetry.g2_low.setText(self._get_vlt("g2_low"))

        self._telemetry.g3h3_high.setText(self._get_vlt("g3h3_high"))
        self._telemetry.g3h3_low.setText(self._get_vlt("g3h3_low"))

        self._telemetry.h1_high.setText(self._get_vlt("h1_high"))
        self._telemetry.h1_low.setText(self._get_vlt("h1_low"))
        """
        """
        self._text = ""
        for key, value in data.items():
            if key.endswith("_value"):
                self._text += "{: <20}\t{}\n".format(key + ":", value)

        self._telemetry.textEdit.setPlainText(self._text)
        """

    def _telemetry_callback(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')

        j = json.loads(data)

        self.update_telemetry_signal.emit(j)

    def show(self):
        self._telemetry_frame.show()
