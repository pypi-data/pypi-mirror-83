import logging
import traceback

from pyqt_tools import messages

import gfagui.signal as signal
from .gfa import GFAWrapper
from .gui import GUI
from .view import View, BlockWidget
from .logic import Logic

log = logging.getLogger(__name__)

# TODO: Check if is connected when executing widgets
# TODO: Allow to spawn a console
# TODO: At start check if it's already connected


class ConnectionManager:

    def __init__(self, logic, view, cfg, gfa):
        self._logic = logic
        self._connection = logic.connection
        self._view = view
        self._cfg = cfg
        self._gfa = gfa
        self._offset = logic.show_offset.offset

        self._btns = self._view.tools_panel.ctrl_buttons

        # 0 = first connect then configure, 2 = first unconfigure then disconnect, 1 = nothing
        self._do_all_order = 0

        # Configuration is only loaded the first time that the GFA is connected
        # XXX: This seems like a very bad designs
        self._configuration_loaded = False

    def connect_disconnect_switch(self):
        action = self._btns.get_connect_button_text()
        getattr(self, action.lower())()

    def configure_disconfigure_switch(self):
        action = self._btns.get_configure_button_text()
        getattr(self, action.lower())()

    def disconnect(self):
        try:
            self._connection.disconnect()
            self._btns.set_disconnect_view()
            self._do_all_order -= 1
        except Exception as e:
            traceback.print_exc()
            messages.show_fatal("{}".format(e), "Error when disconnecting")
            self._view.info.show_error("Error: {}".format(e))

    def connect(self):
        try:
            ip, port, aport = self._view.tools_panel.config.connection.get_current_connection_values()

            self._connection.connect(ip, port, aport)
            self._btns.set_connect_view()
            self._do_all_order += 1
            if not self._configuration_loaded:
                self._load_default_cfg()
                self._configuration_loaded = True

        except Exception as e:
            traceback.print_exc()
            messages.show_fatal("{}".format(e), "Error when connecting")
            self._view.info.show_error("Error: {}".format(e))

    def configure(self):
        try:
            with BlockWidget(self._view, "Configuring, please wait"):
                self._connection.configure(self._cfg)

            self._btns.set_configured_view()

            if self._cfg.discharge.auto_enable:
                duration = self._cfg.discharge.duration
                pixel = self._cfg.discharge.pixel
                reset = self._cfg.discharge.reset
                self._gfa.enable_discharge(duration, pixel, reset)
                self._view.tools_panel.status_info.discharge(True)

            if self._cfg.offsets.auto_enable:
                self._offset.write_offsets()
                self._view.tools_panel.status_info.offsets(True)

            if self._cfg.adc.auto_calibrate:
                self._gfa.calibrate_adc()
                self._view.tools_panel.status_info.calibrated(True)

            self._do_all_order += 1
        except Exception as e:
            traceback.print_exc()
            messages.show_fatal("{}".format(e), "Error when connecting")
            self._view.info.show_error("Error: {}".format(e))

    def unconfigure(self):
        try:
            with BlockWidget(self._view, "Unconfiguring, please wait"):
                self._connection.unconfigure()

            self._btns.set_unconfigure_view()
            self._do_all_order -= 1
        except Exception as e:
            traceback.print_exc()
            messages.show_fatal("{}".format(e), "Error when connecting")
            self._view.info.show_error("Error: {}".format(e))

    def do_all_switch(self):
        if self._do_all_order == 2:
            self.unconfigure()
            self.disconnect()
        elif self._do_all_order == 0:
            self.connect()
            self.configure()

    def _load_default_cfg(self):
        self._logic.load_default_cfg()


class GOD:

    def __init__(self, cfg):
        self._cfg = cfg

        self._gui = GUI()

        self._gfa = GFAWrapper()

        self._signal_manager = signal.Manager()

        self._signal_manager.configure_gfa_callbacks(self._gfa)

        # Slots are called in order, so we want to first connect the viewer slots and then the logic
        self._view_manager = View(self._gui.main_window, self._signal_manager)
        self._logic = Logic(self._gui.main_window, self._cfg, self._view_manager.tools_panel.status_info, self._gfa,
                            self._signal_manager)

        self._conn_manager = ConnectionManager(self._logic, self._view_manager, self._cfg, self._gfa)

        self._gui.main_window.button_configure.clicked.connect(self._configure_disconfigure_cb)
        self._gui.main_window.button_connect.clicked.connect(self._connect_disconnect_cb)
        self._gui.main_window.button_do_all.clicked.connect(self._do_all_cb)

    def _connect_disconnect_cb(self):
        self._conn_manager.connect_disconnect_switch()

    def _configure_disconfigure_cb(self):
        self._conn_manager.configure_disconfigure_switch()

    def _do_all_cb(self):
        self._conn_manager.do_all_switch()

    def show_main_window(self):
        # Load default values
        self._view_manager.tools_panel.config.load_values_from_cfg(self._cfg)

        self._gui.show()

    def close(self):
        self._logic.close()
