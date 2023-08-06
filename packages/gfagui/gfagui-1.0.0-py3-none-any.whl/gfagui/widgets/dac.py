from PyQt5.QtWidgets import QFrame

from .base import Widget
from .ui import dac_ui


class DAC(Widget):

    def __init__(self, gfa):
        super(DAC, self).__init__()
        self._gfa = gfa

        self._dac_frame = QFrame()
        self._dac = dac_ui.Ui_Frame()
        self._dac.setupUi(self._dac_frame)

        self._dac.get_button.clicked.connect(self._on_push_get)
        self._dac.set_button.clicked.connect(self._on_push_set)

    def show(self):
        self._update_values()
        self._dac_frame.show()

    def _update_values(self):

        def set_val(obj_name, dac_name):
            dac = self._gfa._gfa.powercontroller.voltages.get_by_name(dac_name)
            getattr(self._dac, obj_name).setValue(dac.volts)

        set_val("rd", "RD")
        set_val("dd", "DD")
        set_val("vss", "VSS")
        set_val("og", "OG")
        set_val("od_eh", "OD_EH")
        set_val("od_fg", "OD_FG")
        set_val("rg_hi", "RG_hi")
        set_val("rg_low", "RG_low")
        set_val("dg_hi", "DG_hi")
        set_val("dg_low", "DG_low")
        set_val("r01_hi", "R01_hi")
        set_val("r01_low", "R01_low")
        set_val("r02_hi", "R02_hi")
        set_val("r02_low", "R02_low")
        set_val("r03_hi", "R03_hi")
        set_val("r03_low", "R03_low")
        set_val("i01_im_hi", "I01_IM_hi")
        set_val("i01_im_low", "I01_IM_low")
        set_val("i02_im_hi", "I02_IM_hi")
        set_val("i02_im_low", "I02_IM_low")
        set_val("i03_im_hi", "I03_IM_hi")
        set_val("i04_im_low", "I04_IM_low")
        set_val("i01_st_hi", "I01_ST_hi")
        set_val("i01_st_low", "I01_ST_low")
        set_val("i02_st_hi", "I02_ST_hi")
        set_val("i02_st_low", "I02_ST_low")
        set_val("i03_st_hi", "I03_ST_hi")
        set_val("i03_st_low", "I03_ST_low")
        set_val("i04_st_hi", "I04_ST_hi")
        set_val("i04_st_low", "I04_ST_low")

    def _on_push_get(self):
        self._gfa._gfa.powercontroller.remote_update_hw_conf()
        self._gfa._gfa.powercontroller.remote_get_configured_voltages()
        self._update_values()

    def _on_push_set(self):
        def set_val(obj_name, dac_name):
            self._gfa._gfa.powercontroller.voltages.get_by_name(dac_name).volts = getattr(self._dac, obj_name).value()

        set_val("rd", "RD")
        set_val("dd", "DD")
        set_val("vss", "VSS")
        set_val("og", "OG")
        set_val("od_eh", "OD_EH")
        set_val("od_fg", "OD_FG")
        set_val("rg_hi", "RG_hi")
        set_val("rg_low", "RG_low")
        set_val("dg_hi", "DG_hi")
        set_val("dg_low", "DG_low")
        set_val("r01_hi", "R01_hi")
        set_val("r01_low", "R01_low")
        set_val("r02_hi", "R02_hi")
        set_val("r02_low", "R02_low")
        set_val("r03_hi", "R03_hi")
        set_val("r03_low", "R03_low")
        set_val("i01_im_hi", "I01_IM_hi")
        set_val("i01_im_low", "I01_IM_low")
        set_val("i02_im_hi", "I02_IM_hi")
        set_val("i02_im_low", "I02_IM_low")
        set_val("i03_im_hi", "I03_IM_hi")
        set_val("i04_im_low", "I04_IM_low")
        set_val("i01_st_hi", "I01_ST_hi")
        set_val("i01_st_low", "I01_ST_low")
        set_val("i02_st_hi", "I02_ST_hi")
        set_val("i02_st_low", "I02_ST_low")
        set_val("i03_st_hi", "I03_ST_hi")
        set_val("i03_st_low", "I03_ST_low")
        set_val("i04_st_hi", "I04_ST_hi")
        set_val("i04_st_low", "I04_ST_low")

        self._gfa._gfa.powercontroller.remote_set_voltages()