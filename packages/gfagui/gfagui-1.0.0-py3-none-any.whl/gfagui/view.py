# Use callbacks with Actions for both controller and View
# We will need some sort of action completed callback

from PyQt5.QtCore import QObject, pyqtSlot, Qt, QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget

from .gfa import Test
from .helper_functions import memory_usage


class _ViewConfigurationConnection:

    def __init__(self, connection):
        self._conn = connection

    def find(self, name):
        return self._conn.findChild(QObject, name, Qt.FindDirectChildrenOnly)

    def load_connection_values_from_cfg(self, connection_cfg):
        ip = self.find("text_ip")
        ip.setText(connection_cfg.server_ip)

    def _set_enable_value_for_connection_info(self, val):
        port = self.find("spin_port")
        port.setDisabled(val)

        aport = self.find("spin_aport")
        aport.setDisabled(val)

        ip = self.find("text_ip")
        ip.setDisabled(val)

    def allow_modify_connection_info(self):
        self._set_enable_value_for_connection_info(True)

    def disallow_modify_connection_info(self):
        self._set_enable_value_for_connection_info(False)

    def get_current_connection_values(self):
        ip = self.find("text_ip")
        port = self.find("spin_port")
        aport = self.find("spin_aport")

        return ip.text(), port.value(), aport.value()


class _ViewConfigurationGeometry:

    def __init__(self, geometry):
        self._geom = geometry

    def find(self, name):
        return self._geom.findChild(QObject, name, Qt.FindDirectChildrenOnly)

    def load_geometry_values_from_cfg(self, geometry_cfg):
        storage_rows = self.find("storage_rows")
        storage_rows.setValue(geometry_cfg.storage_rows)

        active_rows = self.find("active_rows")
        active_rows.setValue(geometry_cfg.active_rows)

        prescan = self.find("prescan")
        prescan.setValue(geometry_cfg.prescan)

        overscan = self.find("overscan")
        overscan.setValue(geometry_cfg.overscan)

        columns = self.find("columns")
        columns.setValue(geometry_cfg.columns)


class _ViewConfigurationExpose(QObject):

    def __init__(self, expose):
        super(_ViewConfigurationExpose, self).__init__()

        self._expose = expose

        # Set some placeholders
        pattern = self.find("expose_pattern")
        pattern.setCurrentText("Pattern")

        mode = self.find("expose_mode")
        mode.setCurrentText("Data Mode")

        fake = self.find("check_fake")
        fake.stateChanged.connect(self._fake_changed)

    @pyqtSlot(int)
    def _fake_changed(self, new_state):
        self._set_enabled_pattern(new_state != 0)

    def _set_enabled_pattern(self, v):
        pattern = self.find("expose_pattern")
        pattern.setEnabled(v)

    def find(self, name):
        return self._expose.findChild(QObject, name, Qt.FindDirectChildrenOnly)

    def load_expose_values_from_cfg(self, expose_cfg):
        expose_mode = self.find("expose_mode")
        expose_mode.setCurrentIndex(expose_cfg.mode)

        expose_time = self.find("spin_exposeTime")
        expose_time.setValue(expose_cfg.time)

        fake_data = self.find("check_fake")
        fake_data.setChecked(expose_cfg.fake_data)

        self._set_enabled_pattern(expose_cfg.fake_data)


class _ViewConfigurationPostExpose(QObject):

    def __init__(self, post_expose):
        super(_ViewConfigurationPostExpose, self).__init__()
        self._post_expose = post_expose

        # Hide widgets that currently are not used, those widgets
        # will be re-showed when needed
        self._set_ccd_widgets_visibility(False)

        save = self.find("check_save")
        save.stateChanged.connect(self._save_changed)

        gfa_id = self.find("gfa_id")
        gfa_id.currentIndexChanged.connect(self._gfa_id_changed)

    @pyqtSlot(int)
    def _save_changed(self, new_state):
        self._set_ccd_widgets_visibility(new_state != 0)

    @pyqtSlot(int)
    def _gfa_id_changed(self, index):

        ccd_serial_map = {
            0: "NO-GFA",
            1: "13072-18-04",
            2: "13072-22-04",
            3: "13072-24-06",
            4: "13072-18-08",
            5: "13072-24-01",
            6: "16153-12-07",
            7: "16153-08-03",
            8: "16163-13-02",
            9: "13072-07-07",
            10: "13072-22-06",
            11: "13072-24-08",  # GFA#12
            12: "13072-18-07",  # GFA#13

        }

        ccd_serial = self.find("ccd_serial")
        ccd_serial.setText(ccd_serial_map[index])

    def _set_ccd_widgets_visibility(self, v):
        images_dir = self.find("images_dir")
        images_dir.setVisible(v)

        label_gfa_id = self.find("label_gfa_id")
        label_gfa_id.setVisible(v)

        gfa_id = self.find("gfa_id")
        gfa_id.setVisible(v)

        label_ccd_serial = self.find("label_ccd_serial")
        label_ccd_serial.setVisible(v)

        ccd_serial = self.find("ccd_serial")
        ccd_serial.setVisible(v)

    def find(self, name):
        return self._post_expose.findChild(QObject, name, Qt.FindDirectChildrenOnly)

    def load_post_expose_values_from_cfg(self, post_exp_cfg):
        images_dir = self.find("images_dir")
        images_dir.setText(post_exp_cfg.images_dir)


class _ViewConfiguration(QObject):

    def __init__(self, config_panel):
        super(_ViewConfiguration, self).__init__()

        self._config_panel = config_panel

        c = self.find("connection")
        self.connection = _ViewConfigurationConnection(c)

        g = self.find("geometry")
        self._geometry = _ViewConfigurationGeometry(g)

        e = self.find("expose")
        self.expose = _ViewConfigurationExpose(e)

        p = self.find("post_expose")
        self.post_expose = _ViewConfigurationPostExpose(p)

    def find(self, name):
        return self._config_panel.findChild(QObject, name, Qt.FindDirectChildrenOnly)

    def load_values_from_cfg(self, file_config):
        self.connection.load_connection_values_from_cfg(file_config.connection)
        self._geometry.load_geometry_values_from_cfg(file_config.geometry)
        self.expose.load_expose_values_from_cfg(file_config.expose)
        self.post_expose.load_post_expose_values_from_cfg(file_config.post_expose)


class _ViewStatusInfo:

    def __init__(self, status_info):
        self._status = status_info

    def configured(self, b):
        configured = self.find("configured_check")
        configured.setChecked(b)

    def calibrated(self, b):
        check = self.find("calibrated_check")
        check.setChecked(b)

    def offsets(self, b):
        check = self.find("offsets_check")
        check.setChecked(b)

    def discharge(self, b):
        # TODO: Somehow set the discharge checkbox of discharge tool to true
        check = self.find("discharge_check")
        check.setChecked(b)

    def find(self, name):
        return self._status.findChild(QObject, name, Qt.FindDirectChildrenOnly)


class _ViewCtrlButtons(QObject):

    def __init__(self, ctrl_buttons, info, conn_cfg, status, expose, post_expose):
        super(_ViewCtrlButtons, self).__init__()

        self._ctrl_buttons = ctrl_buttons
        self._info = info
        self._conn_cfg = conn_cfg
        self._status_info = status
        self._expose = expose
        self._post_expose = post_expose

        # 0 = first connect then configure, 2 = first unconfigure then disconnect
        self._do_all_order = 0

        test = self._expose.find("combo_test")
        test.currentIndexChanged.connect(self._test_index_changed)

        # Set default values
        self.set_disconnect_view()

    @pyqtSlot(int)
    def _test_index_changed(self, index):
        test_type = Test(index)

        exp_time = self._expose.find("spin_exposeTime")
        exp_time.setDisabled(False)

        check_save = self._post_expose.find("check_save")
        check_save.setDisabled(True)
        check_save.setChecked(True)

        stop_life = self.find("button_stop_life_test")
        stop_life.setDisabled(True)

        storage = self._expose.find("combo_storage")
        try:
            check_save.setChecked(self._saved_save)
            storage.setCurrentIndex(self._saved_storage)
        except AttributeError:
            self._saved_save = check_save.isChecked()
            self._saved_storage = storage.currentIndex()

        if test_type == Test.NONE:
            check_save.setDisabled(False)
            check_save.setChecked(self._saved_save)

            storage.setEnabled(True)
        else:
            storage.setCurrentIndex(0)
            storage.setEnabled(False)
            exp_time.setDisabled(True)

            if test_type == Test.BIAS:
                exp_time.setValue(0)
            elif test_type == Test.DC:
                exp_time.setValue(60)
            elif test_type == Test.FCTE:
                exp_time.setValue(7)
            elif test_type == Test.LIFE:
                exp_time.setEnabled(True)
                stop_life.setEnabled(True)
            else:
                # The next tests have a dynamic exp time: PTC, FLATS, DARKS, PSF, PDF_LOOP
                exp_time.setValue(0)

    def set_connect_view(self):
        self._info.show_success("CONNECTED")

        connect = self.find("button_connect")
        connect.setText("DISCONNECT")

        configure = self.find("button_configure")
        configure.setDisabled(False)

        self._conn_cfg.allow_modify_connection_info()

        do_all = self.find("button_do_all")
        do_all.setDisabled(True)
        do_all.setText("UNCONFIGURE\n+\nDISCONNECT")

        self._do_all_order += 1

    def set_disconnect_view(self):
        self._info.show_error("DISCONNECTED")

        connect = self.find("button_connect")
        connect.setText("CONNECT")

        configure = self.find("button_configure")
        configure.setDisabled(True)

        self._conn_cfg.disallow_modify_connection_info()

        if self._do_all_order > 0:
            self._do_all_order -= 1

        if self._do_all_order == 0:
            do_all = self.find("button_do_all")
            do_all.setDisabled(False)
        else:
            do_all = self.find("button_do_all")
            do_all.setDisabled(True)
            self._do_all_order = 0

    def set_configured_view(self):
        self._info.show_success("CONFIGURED")

        configure = self.find("button_configure")
        configure.setText("UNCONFIGURE")

        self._status_info.configured(True)

        self._do_all_order += 1

        do_all = self.find("button_do_all")
        do_all.setDisabled(False)

    def set_unconfigure_view(self):
        self._info.show_success("UNCONFIGURED")

        configure = self.find("button_configure")
        configure.setText("CONFIGURE")

        self._do_all_order -= 1

        do_all = self.find("button_do_all")
        do_all.setDisabled(True)
        do_all.setText("CONNECT\n+\nCONFIGURE")

    def find(self, name):
        return self._ctrl_buttons.findChild(QObject, name, Qt.FindDirectChildrenOnly)

    def get_connect_button_text(self):
        connect = self.find("button_connect")
        return connect.text()

    def get_configure_button_text(self):
        connect = self.find("button_configure")
        return connect.text()


class _ViewToolsPanel(QObject):

    def __init__(self, tools_panel, info):
        super(_ViewToolsPanel, self).__init__()

        self._tools_panel = tools_panel

        cfg = self.find("config_panel")
        self.config = _ViewConfiguration(cfg)

        status = self.find("status_info")
        self.status_info = _ViewStatusInfo(status)

        b = self.find("control_buttons")
        self.ctrl_buttons = _ViewCtrlButtons(b, info, self.config.connection, self.status_info,
                                             self.config.expose, self.config.post_expose)

    def find(self, name):
        return self._tools_panel.findChild(QObject, name, Qt.FindDirectChildrenOnly)


class _ViewInformationBottom:

    def __init__(self, info_widget):
        self._info = info_widget

    def _set_style(self, style):
        self._info.setStyleSheet(style)

    def _set_msg(self, msg):
        self._info.setText(msg)

    def show_error(self, msg):
        self._set_style("color: red;")
        self._set_msg(msg)

    def show_warning(self, msg):
        self._set_style("color: olive;")
        self._set_msg(msg)

    def show_success(self, msg):
        self._set_style("color: green;")
        self._set_msg(msg)

    def show_info(self, msg):
        self._set_style("color: blue;")
        self._set_msg(msg)


class _ViewFPGATempLabel(QObject):

    def __init__(self, signal_manager):
        super(_ViewFPGATempLabel, self).__init__()

        self.managed_widget = QLabel()
        self.managed_widget.setAlignment(Qt.AlignLeft)

        self._temperature = 0
        self.update()

        signal_manager.sensors.add_cb(self._sensors_callback)

    def _set_text(self, t):
        self.managed_widget.setText(t)

    def _sensors_callback(self, data):
        self._temperature = round(data["temperature"], 3)
        self.update()

    def update(self):
        fmt = "Temperature: {}. Memory usage: {}".format(
            self._temperature, memory_usage())
        self._set_text(fmt)


class _ViewActionCalibrateADC(QObject):

    def __init__(self, action, status):
        super(_ViewActionCalibrateADC, self).__init__()

        self._status_info = status

        action.triggered.connect(self._calibrate_adc)

    def _calibrate_adc(self):
        self._status_info.calibrated(True)


class _ViewTab:

    def __init__(self, info, signal_manager):
        self._info = info

        signal_manager.img_done.add_cb(self._show_info)

    def _show_info(self, d):
        cfg = d["config"]

        # Avoid plotting exposures of the CCD widget
        if cfg and cfg.test == Test.NONE and not cfg.show_plot:
            return

        # im = d["image"]
        # elapsed_time = d["elapsed_time"]

        if cfg.test != Test.NONE:
            im_name = cfg.image_name.split("_")
            test_name = im_name[0]
            test_number = im_name[-1]
            self._info.show_info("{} TEST {}".format(test_name, int(test_number)))
        else:
            self._info.show_success("EXPOSE DONE")


class _ShowImgStart:

    def __init__(self, info, signal_manager):

        self._info = info

        signal_manager.img_start.add_cb(self._show_img_start)

    def _show_img_start(self, d):
        self._info.show_info("STARTING EXPOSE")


# Manages main window visual elements
class View:

    def __init__(self, main_window, signal_manager):

        self.managed_widget = main_window.centralwidget

        # Prints information to the status bar
        self.info = _ViewInformationBottom(main_window.label_info)
        main_window.statusBar.addWidget(main_window.label_info)

        self.tools_panel = _ViewToolsPanel(main_window.tools_panel, self.info)
        self._tab = _ViewTab(self.info, signal_manager)

        self.fpga_temp_label = _ViewFPGATempLabel(signal_manager)
        main_window.statusBar.addPermanentWidget(self.fpga_temp_label.managed_widget)

        self._action_adc = _ViewActionCalibrateADC(main_window.actionCalibrate_ADC, self.tools_panel.status_info)

        self._show_img_start = _ShowImgStart(self.info, signal_manager)

    def setDisabled(self, b):
        self.managed_widget.setDisabled(b)


class BlockWidget:

    def __init__(self, w, m):
        self._widget = w
        self._message = m

    def __enter__(self):
        self._widget.info.show_info(self._message)
        self._widget.setDisabled(True)
        QCoreApplication.instance().processEvents()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._widget.setDisabled(False)
