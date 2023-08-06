from PyQt5.QtWidgets import QFrame, QTreeWidget, QTreeWidgetItem

from .base import Widget
from .ui import settings_ui


class Settings(Widget):

    def __init__(self, gfa, config):
        super(Settings, self).__init__()
        self._gfa = gfa
        self._conf = config

        self._settings_frame = QFrame()
        self._settings = settings_ui.Ui_Frame()
        self._settings.setupUi(self._settings_frame)

        self._settings.button_set.clicked.connect(self._on_push_set)
        self._settings.button_get.clicked.connect(self._on_push_get)

        self._settings.treeWidget.header().resizeSection(0, 200)

    def _on_push_set(self):
        cfg = self._conf.timings

        # CLOCK TIMINGS
        items = self._settings.treeWidget.topLevelItem(0)
        clks = self._gfa.get_clk_timings()
        # hor_clk = [i for i in vars(clks) if i.startswith("hor")]
        hor = items.child(0)
        clks.hor_acq = int(hor.child(0).text(1))
        clks.hor_acq_skip = int(hor.child(1).text(1))
        clks.hor_del = int(hor.child(2).text(1))
        clks.hor_del_skip = int(hor.child(3).text(1))
        clks.hor_overlap = int(hor.child(4).text(1))
        clks.hor_overlap_skip = int(hor.child(5).text(1))
        clks.hor_postrg = int(hor.child(6).text(1))
        clks.hor_postrg_skip = int(hor.child(7).text(1))
        clks.hor_prerg = int(hor.child(8).text(1))
        clks.hor_prerg_skip = int(hor.child(9).text(1))
        clks.hor_rg = int(hor.child(10).text(1))
        clks.hor_rg_skip = int(hor.child(11).text(1))
        clks.debug_phase = int(hor.child(12).text(1))
        vert = items.child(1)
        clks.vert_tdgr = int(vert.child(0).text(1))
        clks.vert_tdrg = int(vert.child(1).text(1))
        clks.vert_tdrt = int(vert.child(2).text(1))
        clks.vert_tdtr = int(vert.child(3).text(1))
        clks.vert_toi = int(vert.child(4).text(1))
        self._gfa.set_clk_timings()

        cfg.hor.acq = clks.hor_acq
        cfg.hor["del"] = clks.hor_del
        cfg.hor.postrg = clks.hor_postrg
        cfg.hor.prerg = clks.hor_prerg
        cfg.hor.rg = clks.hor_rg
        cfg.hor.overlap = clks.hor_overlap

        # GFA GEOM
        items = self._settings.treeWidget.topLevelItem(1)
        geom = self._gfa.get_geom_conf()
        geom.overscan_cols = int(items.child(0).text(1))
        geom.prescan_cols = int(items.child(1).text(1))

        items = self._settings.treeWidget.topLevelItem(1)
        if items.child(2).child(0).checkState(1) == 2:
            geom.amplifiers_eh_enable = True
        else:
            geom.amplifiers_eh_enable = False

        if items.child(2).child(1).checkState(1) == 2:
            geom.amplifiers_fg_enable = True
        else:
            geom.amplifiers_fg_enable = False

        geom.ccd_active_cols = int(items.child(3).text(1))
        geom.image_rows = int(items.child(4).text(1))

        if items.child(5).checkState(1) == 2:
            geom.image_shift_en = True
        else:
            geom.image_shift_en = False

        geom.storage_rows = int(items.child(6).text(1))

        if items.child(7).checkState(1) == 2:
            geom.storage_shift_en = True
        else:
            geom.storage_shift_en = False
        self._gfa.set_geom_conf()

        # DATA MANAGER
        items = self._settings.treeWidget.topLevelItem(2)
        delay = int(items.child(0).text(1))
        self._gfa.set_adc_delay(delay)
        self._conf.adc.delay = delay

    def _on_push_get(self):
        clks = self._gfa.get_clk_timings()
        items = self._settings.treeWidget.topLevelItem(0)
        hor = items.child(0)
        hor.child(0).setText(1, str(clks.hor_acq))
        hor.child(1).setText(1, str(clks.hor_acq_skip))
        hor.child(2).setText(1, str(clks.hor_del))
        hor.child(3).setText(1, str(clks.hor_del_skip))
        hor.child(4).setText(1, str(clks.hor_overlap))
        hor.child(5).setText(1, str(clks.hor_overlap_skip))
        hor.child(6).setText(1, str(clks.hor_postrg))
        hor.child(7).setText(1, str(clks.hor_postrg_skip))
        hor.child(8).setText(1, str(clks.hor_prerg))
        hor.child(9).setText(1, str(clks.hor_prerg_skip))
        hor.child(10).setText(1, str(clks.hor_rg))
        hor.child(11).setText(1, str(clks.hor_rg_skip))
        hor.child(12).setText(1, str(clks.debug_phase))
        vert = items.child(1)
        vert.child(0).setText(1, str(clks.vert_tdgr))
        vert.child(1).setText(1, str(clks.vert_tdrg))
        vert.child(2).setText(1, str(clks.vert_tdrt))
        vert.child(3).setText(1, str(clks.vert_tdtr))
        vert.child(4).setText(1, str(clks.vert_toi))

        items = self._settings.treeWidget.topLevelItem(1)
        geom = self._gfa.get_geom_conf()
        items.child(0).setText(1, str(geom.overscan_cols))
        items.child(1).setText(1, str(geom.prescan_cols))

        if geom.amplifiers_eh_enable:
            items.child(2).child(0).setCheckState(1, 2)
        else:
            items.child(2).child(0).setCheckState(1, 0)

        if geom.amplifiers_fg_enable:
            items.child(2).child(1).setCheckState(1, 2)
        else:
            items.child(2).child(1).setCheckState(1, 0)

        items.child(3).setText(1, str(geom.ccd_active_cols))
        items.child(4).setText(1, str(geom.image_rows))

        if geom.image_shift_en:
            items.child(5).setCheckState(1, 2)
        else:
            items.child(5).setCheckState(1, 0)

        items.child(6).setText(1, str(geom.storage_rows))

        if geom.storage_shift_en:
            items.child(7).setCheckState(1, 2)
        else:
            items.child(7).setCheckState(1, 0)

        items = self._settings.treeWidget.topLevelItem(2)
        items.child(0).setText(1, str(self._gfa.get_adc_delay()))

    def show(self):
        self._on_push_get()

        def expand(item):
            if isinstance(item, QTreeWidget):
                num_elem = item.topLevelItemCount()
            elif isinstance(item, QTreeWidgetItem):
                num_elem = item.childCount()
            else:
                raise Exception("This should never happen")

            for i in range(num_elem):
                if isinstance(item, QTreeWidget):
                    child = item.topLevelItem(i)
                    child.setExpanded(True)
                    if item.topLevelItemCount() > 0:
                        expand(child)
                elif isinstance(item, QTreeWidgetItem):
                    child = item.child(i)
                    child.setExpanded(True)
                    if item.childCount() > 0:
                        expand(child)
                else:
                    raise Exception("This should never happen")

        # By default expand the tree, issue #16
        expand(self._settings.treeWidget)

        self._settings_frame.show()
