from PyQt5.QtWidgets import QFrame

from .base import Widget
from .ui import diagnostics_ui


class Diagnostics(Widget):
    # TODO: Create a label for each one

    def __init__(self, gfa):
        super(Diagnostics, self).__init__()
        self._gfa = gfa

        self._diagnostics_frame = QFrame()
        self._diagnostics = diagnostics_ui.Ui_Frame()
        self._diagnostics.setupUi(self._diagnostics_frame)

        self._diagnostics.update.clicked.connect(self.show)

    def _get_geometry(self):
        return str(self._gfa.get_geom_conf())

    def _get_clk_timings(self):
        return str(self._gfa.get_clk_timings())

    def _get_reg_info(self):
        info = self._gfa.get_reg_info()
        string = str(info.status) + "\n"
        string += str(info) + "\n"
        return string

    def _get_dac_voltages(self):
        return str(self._gfa.get_dac_voltages())

    def _get_expctrl_info(self):
        return str(self._gfa.get_expctrl_info())

    def _get_vlt_enables(self):
        return str(self._gfa.get_vlt_enables())

    def _get_phase_timings(self):
        return str(self._gfa.get_phase_timings())

    def _get_configured_channels(self):
        return str(self._gfa.get_configured_channels())

    def _get_irq_status(self):
        return str(self._gfa.get_irq_status())

    def _get_buffers_status(self):
        return str(self._gfa.get_buffers_status())

    def show(self):
        d = self._diagnostics
        d.geometry.setPlainText(self._get_geometry())
        d.clk_timings.setPlainText(self._get_clk_timings())
        d.reg_info.setPlainText(self._get_reg_info())
        d.dac_voltages.setPlainText(self._get_dac_voltages())
        d.expctrl_info.setPlainText(self._get_expctrl_info())
        d.vlt_enables.setPlainText(self._get_vlt_enables())
        d.phase_timings.setPlainText(self._get_phase_timings())
        d.configured_channels.setPlainText(self._get_configured_channels())
        d.irq_status.setPlainText(self._get_irq_status())
        d.buffers_status.setPlainText(self._get_buffers_status())

        self._diagnostics_frame.show()
