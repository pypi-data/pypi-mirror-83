from PyQt5.QtWidgets import QFrame

from .base import Widget
from .ui import adc_ui


class ADC(Widget):

    def __init__(self, gfa):
        super(ADC, self).__init__()
        self._gfa = gfa

        self._adc_frame = QFrame()
        self._adc_widget = adc_ui.Ui_Frame()
        self._adc_widget.setupUi(self._adc_frame)

        self._adc_widget.button_write.clicked.connect(self._on_push_write)

    def _write_spi(self, addr, value):
        self._gfa.write_spi_adc(addr, value)

    def _on_push_write(self):
        address = int(self._adc_widget.line_address.text(), 16)
        value = int(self._adc_widget.line_value.text(), 16)

        self._write_spi(address, value)

    def show(self):
        self._adc_frame.show()
