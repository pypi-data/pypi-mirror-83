import logging

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from gfafunctionality.raws import RawImageMetadata
from pyqt_tools import messages

from .gfa import Test, Storage, Config
from .helper_functions import new_image, save_current_config_table
from .data_logger import ExposureDataLog
from .tests import Tests
from .widgets.adc import ADC
from .widgets.alarms import Alarms
from .widgets.ccd import CCD
from .widgets.dac import DAC
from .widgets.diagnostics import Diagnostics
from .widgets.discharge import Discharge
from .widgets.logs import Logs
from .widgets.monitor_sensors import MonitorSensors
from .widgets.offsets import Offset
from .widgets.pid import PID
from .widgets.pwm import PWM
from .widgets.settings import Settings
from .widgets.telemetry import Telemetry
from .widgets.ui.plot_tab import Ui_PlotImageWidget, Ui_TriplePlotImageWidget, Ui_PlotCurveWidget, Ui_DualPlotImageWidget
from .widgets.versions import Versions


log = logging.getLogger(__name__)


class _LogicConnection:

    def __init__(self, g):
        self._gfa = g

    def connect(self, ip, port, aport):
        # TODO: Maybe check if it's already connected
        self._gfa.connect(ip, port, aport)

        if not self._gfa.is_same_api():
            messages.show_message("API MISMATCH", "API mismatch", QMessageBox.Warning)
            log.warning("API mismatch")

    def disconnect(self):
        self._gfa.disconnect()

    def configure(self, config):
        self._gfa.configure()

        cfg = config.timings

        # Adc
        self._gfa.set_adc_delay(config.adc.delay)

        # Clocks
        clks = self._gfa.get_clk_timings()
        if cfg.hor.acq:
            clks.hor_acq = cfg.hor.acq
        if cfg.hor["del"]:
            clks.hor_del = cfg.hor["del"]
        if cfg.hor.postrg:
            clks.hor_postrg = cfg.hor.postrg
        if cfg.hor.prerg:
            clks.hor_prerg = cfg.hor.prerg
        if cfg.hor.rg:
            clks.hor_rg = cfg.hor.rg
        if cfg.hor.overlap:
            clks.hor_overlap = cfg.hor.overlap

        self._gfa.set_clk_timings()

    def unconfigure(self):
        self._gfa.unconfigure()


class _LogicExpose(QObject):

    def __init__(self, g, main_window):
        super(_LogicExpose, self).__init__()

        self._main_window = main_window
        self._gfa = g
        main_window.button_read.clicked.connect(self._expose_button)

    def _expose_button(self):
        w = self._main_window

        columns = w.columns.value()
        num_rows = w.active_rows.value() + w.storage_rows.value()
        overscan = w.overscan.value()
        prescan = w.prescan.value()
        expose_time = w.spin_exposeTime.value()
        gfa_id = w.gfa_id.currentText()
        ccd_serial = w.ccd_serial.text()
        metadata = RawImageMetadata(
            columns, w.storage_rows.value(), w.active_rows.value(), overscan, prescan, expose_time, gfa_id, ccd_serial)

        conf = Config(is_save=w.check_save.isChecked(),
                      is_clear=w.check_clear.isChecked(),
                      is_fake=1 if w.check_fake.isChecked() else 0,
                      out_dir=w.images_dir.text(),
                      pattern=w.expose_pattern.currentIndex(),
                      mode=w.expose_mode.currentIndex(),
                      storage=Storage(w.combo_storage.currentIndex()),
                      metadata=metadata,
                      test=Test(w.combo_test.currentIndex())
                      )

        if conf.test == Test.NONE:
            self.expose(conf)
        else:
            self._t = Tests(self, conf)
            self._t.run()

    def expose(self, cfg):
        self._gfa.set_config(cfg)
        self._gfa.expose()
        # self._ui._info.show_info("STARTING_EXPOSE")


class _LogicActionCalibrateADC(QObject):

    def __init__(self, g, action):
        super(_LogicActionCalibrateADC, self).__init__()

        self._gfa = g
        action.triggered.connect(self._calibrate_adc)

    def _calibrate_adc(self):
        self._gfa.calibrate_adc()


class _LogicActionClearBuffers(QObject):

    def __init__(self, g, action):
        super(_LogicActionClearBuffers, self).__init__()

        self._gfa = g
        action.triggered.connect(self._clear_buff)

    def _clear_buff(self):
        self._gfa.clear_buff()


class _LogicActionClearError(QObject):

    def __init__(self, g, action):
        super(_LogicActionClearError, self).__init__()

        self._gfa = g
        action.triggered.connect(self._clear_err)

    def _clear_err(self):
        self._gfa.clear_error()


class _LogicActionClearStack(QObject):

    def __init__(self, g, action):
        super(_LogicActionClearStack, self).__init__()

        self._gfa = g
        action.triggered.connect(self._clear_stack)

    def _clear_stack(self):
        self._gfa.clear_stack()


class _LogicActionDisableDrivers(QObject):

    def __init__(self, g, action):
        super(_LogicActionDisableDrivers, self).__init__()

        self._gfa = g
        action.triggered.connect(self._disable)

    def _disable(self):
        self._gfa.disable_drivers()


class _LogicActionEnableDrivers(QObject):

    def __init__(self, g, action):
        super(_LogicActionEnableDrivers, self).__init__()

        self._gfa = g
        action.triggered.connect(self._enable)

    def _enable(self):
        self._gfa.enable_drivers()


class _LogicActionPowerDown(QObject):

    def __init__(self, g, action):
        super(_LogicActionPowerDown, self).__init__()

        self._gfa = g
        action.triggered.connect(self._power_down)

    def _power_down(self):
        self._gfa.power_down()


class _LogicActionPowerUp(QObject):

    def __init__(self, g, action):
        super(_LogicActionPowerUp, self).__init__()

        self._gfa = g
        action.triggered.connect(self._power_up)

    def _power_up(self):
        self._gfa.power_up()


class _LogicShowADC(QObject):

    def __init__(self, g, action):
        super(_LogicShowADC, self).__init__()

        self._gfa = g
        self._adc = ADC(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._adc.show()


class _LogicShowAlarms(QObject):

    def __init__(self, g, action):
        super(_LogicShowAlarms, self).__init__()

        self._gfa = g
        self._alarms = Alarms(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._alarms.show()


class _LogicShowCCD(QObject):

    def __init__(self, g, action):
        super(_LogicShowCCD, self).__init__()

        self._gfa = g
        self._ccd = CCD(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._ccd.show()


class _LogicShowDAC(QObject):

    def __init__(self, g, action):
        super(_LogicShowDAC, self).__init__()

        self._gfa = g
        self._dac = DAC(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._dac.show()


class _LogicShowDiagnostics(QObject):

    def __init__(self, g, action):
        super(_LogicShowDiagnostics, self).__init__()

        self._gfa = g
        self._diag = Diagnostics(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._diag.show()


class _LogicTab(QObject):

    def __init__(self, tab, manager):
        super(_LogicTab, self).__init__()
        self._tab = tab
        self._tab.tabCloseRequested.connect(self._on_tab_close)
        self._reg = ExposureDataLog()

        manager.img_done.add_cb(self._expose_done)

    def add_tab(self, title, conf):
        if conf.mode == 0:
            tab_widget = Ui_PlotImageWidget()
        elif conf.mode == 1:
            tab_widget = Ui_TriplePlotImageWidget()
        elif conf.mode == 4:
            tab_widget = Ui_PlotCurveWidget()
        else:
            tab_widget = Ui_DualPlotImageWidget()

        self._tab.addTab(tab_widget, str(title))

        i = self._tab.indexOf(tab_widget)
        self._tab.setCurrentIndex(i)

        return tab_widget

    def close(self):
        self._reg.close()

    def _expose_done(self, d):
        cfg = d["config"]

        # Avoid plotting exposures of the CCD widget
        if cfg and cfg.test == Test.NONE and not cfg.show_plot:
            return

        im = d["image"]
        elapsed_time = d["elapsed_time"]

        if cfg.test == Test.NONE:
            if cfg.storage == Storage.read:
                new_tab = self.add_tab(im.image_id, cfg)
                new_image(new_tab, im, cfg)
                save_current_config_table(new_tab, cfg)
                self._reg.add_row(elapsed_time)

    @pyqtSlot(int)
    def _on_tab_close(self, index):
        widget = self._tab.widget(index)
        self._tab.removeTab(index)

        # Fixme: it will throw a lot of errors like RuntimeError: wrapped C/C++
        # object of type QwtPlotCanvas has been deleted
        widget.setParent(None)
        widget.deleteLater()


# TODO: We should do something better with these things
class _LogicShowDischarge(QObject):

    def __init__(self, g, action, config, status):
        super(_LogicShowDischarge, self).__init__()

        self._gfa = g
        self._discharge = Discharge(self._gfa, config, status)

        action.triggered.connect(self._show)

    def _show(self):
        self._discharge.show()


class _LogicShowLogs(QObject):

    def __init__(self, g, action):
        super(_LogicShowLogs, self).__init__()

        self._gfa = g
        self._logs = Logs(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._logs.show()


class _LogicShowMonitorSensors(QObject):

    def __init__(self, g, action):
        super(_LogicShowMonitorSensors, self).__init__()

        self._gfa = g
        self._monitor = MonitorSensors(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._monitor.show()


class _LogicShowOffset(QObject):

    def __init__(self, g, action, cfg):
        super(_LogicShowOffset, self).__init__()

        self._gfa = g
        self.offset = Offset(self._gfa, cfg)

        action.triggered.connect(self._show)

    def _show(self):
        self.offset.show()


class _LogicShowPID(QObject):

    def __init__(self, g, action, signal_manager, cfg):
        super(_LogicShowPID, self).__init__()

        self._cfg = cfg
        self._gfa = g
        self._pid = PID(self._gfa, signal_manager, cfg)

        action.triggered.connect(self._show)

    def _show(self):
        self._pid.show()

    def load_default_cfg(self):
        pid = self._cfg.pid
        self._gfa._gfa.pid.remote_set_max_duty_cycle(pid.max_duty)
        self._gfa._gfa.pid.remote_set_integral_error_limits(pid.max_integral_error, pid.min_integral_error)
        self._gfa._gfa.pid.remote_set_components(kp=pid.p, ki=pid.i, kd=pid.d)


class _LogicShowPWM(QObject):

    def __init__(self, g, action):
        super(_LogicShowPWM, self).__init__()

        self._gfa = g
        self._pwm = PWM(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._pwm.show()


class _LogicShowSettings(QObject):

    def __init__(self, g, action, cfg):
        super(_LogicShowSettings, self).__init__()

        self._gfa = g
        self._settings = Settings(self._gfa, cfg)

        action.triggered.connect(self._show)

    def _show(self):
        self._settings.show()


class _LogicShowTelemetry(QObject):

    def __init__(self, g, action):
        super(_LogicShowTelemetry, self).__init__()

        self._gfa = g
        self._telem = Telemetry(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._telem.show()


class _LogicShowVersions(QObject):

    def __init__(self, g, action):
        super(_LogicShowVersions, self).__init__()

        self._gfa = g
        self._ver = Versions(self._gfa)

        action.triggered.connect(self._show)

    def _show(self):
        self._ver.show()


class Logic:

    def __init__(self, main_window, config, status, gfa, signal_manager):
        self._main_window = main_window

        self._gfa = gfa

        self.connection = _LogicConnection(self._gfa)

        # Widgets
        self._expose = _LogicExpose(self._gfa, self._main_window)
        self.tab = _LogicTab(self._main_window.tab, signal_manager)
        self._action_adc = _LogicActionCalibrateADC(self._gfa, self._main_window.actionCalibrate_ADC)
        self._action_clear_buff = _LogicActionClearBuffers(self._gfa, self._main_window.actionClear_buffers)
        self._action_clear_error = _LogicActionClearError(self._gfa, self._main_window.actionClear_error_state)
        self._action_clear_stack = _LogicActionClearStack(self._gfa, self._main_window.actionClearStack)
        self._action_disable_drivers = _LogicActionDisableDrivers(self._gfa, self._main_window.actionDisable_drivers)
        self._action_enable_drivers = _LogicActionEnableDrivers(self._gfa, self._main_window.actionEnable_drivers)
        self._action_power_down = _LogicActionPowerDown(self._gfa, self._main_window.actionPower_down)
        self._action_power_up = _LogicActionPowerUp(self._gfa, self._main_window.actionPower_up)
        self._show_adc = _LogicShowADC(self._gfa, self._main_window.actionADC)
        self._show_alarms = _LogicShowAlarms(self._gfa, self._main_window.actionAlarms)
        self._show_ccd = _LogicShowCCD(self._gfa, self._main_window.actionCCD)
        self._show_dac = _LogicShowDAC(self._gfa, self._main_window.actionDAC)
        self._show_diag = _LogicShowDiagnostics(self._gfa, self._main_window.actionDiagnostics)
        self._show_discharge = _LogicShowDischarge(self._gfa, self._main_window.actionDischarge_config, config, status)
        self._show_logs = _LogicShowLogs(self._gfa, self._main_window.actionLogs)
        self._show_monitor = _LogicShowMonitorSensors(self._gfa, self._main_window.actionSensors_monitor)
        self.show_offset = _LogicShowOffset(self._gfa, self._main_window.actionOffset, config)
        self._show_pid = _LogicShowPID(self._gfa, self._main_window.actionPID, signal_manager, config)
        self._show_pwm = _LogicShowPWM(self._gfa, self._main_window.actionPWM)
        self._show_settings = _LogicShowSettings(self._gfa, self._main_window.actionSettings, config)
        self._show_telemetry = _LogicShowTelemetry(self._gfa, self._main_window.actionTelemetry)
        self._show_versions = _LogicShowVersions(self._gfa, self._main_window.actionVersions)

        # self._tests_logic = LogicTests(main_window.config_panel)

    def load_default_cfg(self):
        """
        This function is called after GFA is connected.
        """

        self._show_pid.load_default_cfg()

    def close(self):
        self._gfa.close()
        self.tab.close()
