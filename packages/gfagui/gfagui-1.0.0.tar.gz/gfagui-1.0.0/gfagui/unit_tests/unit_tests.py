import unittest

# Workarond for debian based systems
import os; os.environ.setdefault("QT_API", "pyqt5")

from PyQt5.QtWidgets import QApplication

from gui import GUI


class TestViewConfigurationConnection(unittest.TestCase):

    def setUp(self):
        from view import _ViewConfigurationConnection
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewConfigurationConnection(self.gui.main_window.connection)

    def test_allow(self):
        self.instance.allow_modify_connection_info()

    def test_disallow(self):
        self.instance.disallow_modify_connection_info()

    def test_get_vals(self):
        self.instance.get_current_connection_values()

    def test_load_cfg(self):
        class Cfg:
            server_ip = "127.0.0.1"
        self.instance.load_connection_values_from_cfg(Cfg())


class TestViewConfigurationGeometry(unittest.TestCase):

    def setUp(self):
        from view import _ViewConfigurationGeometry
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewConfigurationGeometry(self.gui.main_window.geometry)

    def test_load_cfg(self):
        class Cfg:
            storage_rows = 0
            active_rows = 0
            prescan = 0
            overscan = 0
            columns = 0
        self.instance.load_geometry_values_from_cfg(Cfg())


class TestViewConfigurationExpose(unittest.TestCase):

    def setUp(self):
        from view import _ViewConfigurationExpose
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewConfigurationExpose(self.gui.main_window.expose)

    def test_load_cfg(self):
        class Cfg:
            mode = 0
            time = 0
            fake_data = True
        self.instance.load_expose_values_from_cfg(Cfg())

    def test_fake_mode_change(self):
        self.instance._fake_changed(0)


class TestViewConfigurationPostExpose(unittest.TestCase):

    def setUp(self):
        from view import _ViewConfigurationPostExpose
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewConfigurationPostExpose(self.gui.main_window.post_expose)

    def test_load_cfg(self):
        class Cfg:
            images_dir = ""
        self.instance.load_post_expose_values_from_cfg(Cfg())

    def test_id_change(self):
        self.instance._gfa_id_changed(0)

    def test_save_changed(self):
        self.instance._save_changed(0)


class TestViewConfiguration(unittest.TestCase):

    def setUp(self):
        from view import _ViewConfiguration
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewConfiguration(self.gui.main_window.config_panel)

    def test_load_cfg(self):
        class PostExpose:
            images_dir = ""

        class Expose:
            mode = 0
            time = 0
            fake_data = True

        class Geometry:
            storage_rows = 0
            active_rows = 0
            prescan = 0
            overscan = 0
            columns = 0

        class Connection:
            server_ip = "127.0.0.1"

        class Cfg:
            connection = Connection()
            geometry = Geometry()
            expose = Expose()
            post_expose = PostExpose()

        self.instance.load_values_from_cfg(Cfg())


class TestViewStatusInfo(unittest.TestCase):

    def setUp(self):
        from view import _ViewStatusInfo
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewStatusInfo(self.gui.main_window.status_info)

    def test_configured(self):
        self.instance.configured(0)

    def test_calibrated(self):
        self.instance.calibrated(0)

    def test_offsets(self):
        self.instance.offsets(0)

    def test_discharge(self):
        self.instance.discharge(0)


class TestViewInformationBottom(unittest.TestCase):

    def setUp(self):
        from view import _ViewInformationBottom
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewInformationBottom(self.gui.main_window.label_info)

    def test_show_error(self):
        self.instance.show_error("")

    def test_show_warning(self):
        self.instance.show_warning("")

    def test_show_success(self):
        self.instance.show_success("")

    def test_show_info(self):
        self.instance.show_info("")


class TestViewCtrlButtons(unittest.TestCase):

    def setUp(self):
        from view import _ViewCtrlButtons, _ViewInformationBottom, _ViewConfigurationExpose, _ViewConfigurationConnection, _ViewStatusInfo, _ViewConfigurationPostExpose
        self.app = QApplication([])
        self.gui = GUI()
        w = self.gui.main_window
        info = _ViewInformationBottom(w.label_info)
        exp = _ViewConfigurationExpose(w.expose)
        con = _ViewConfigurationConnection(w.connection)
        status = _ViewStatusInfo(w.status_info)
        post = _ViewConfigurationPostExpose(w.post_expose)
        self.instance = _ViewCtrlButtons(w.control_buttons, info, con, status, exp, post)

    def test_get_configure_button_text(self):
        self.instance.get_configure_button_text()

    def test_get_connect_button_text(self):
        self.instance.get_connect_button_text()

    def test_set_unconfigure_view(self):
        self.instance.set_unconfigure_view()

    def test_set_configured_view(self):
        self.instance.set_configured_view()

    def test_set_disconnect_view(self):
        self.instance.set_connect_view()
        self.instance.set_connect_view()
        self.instance.set_disconnect_view()
        self.instance.set_connect_view()
        self.instance.set_disconnect_view()

    def test_set_connect_view(self):
        self.instance.set_connect_view()

    def test_index_changed(self):
        self.instance._test_index_changed(0)
        self.instance._test_index_changed(1)
        self.instance._test_index_changed(2)
        self.instance._test_index_changed(3)
        self.instance._test_index_changed(4)
        self.instance._test_index_changed(5)
        self.instance._test_index_changed(6)
        self.instance._test_index_changed(7)


class TestViewToolsPanel(unittest.TestCase):

    def setUp(self):
        from view import _ViewToolsPanel, _ViewInformationBottom
        self.app = QApplication([])
        self.gui = GUI()
        info = _ViewInformationBottom(self.gui.main_window.label_info)
        self.instance = _ViewToolsPanel(self.gui.main_window.tools_panel, info)

    def test_dummy(self):
        pass


class TestViewFPGATempLabel(unittest.TestCase):

    def setUp(self):
        from view import _ViewFPGATempLabel
        self.app = QApplication([])
        self.gui = GUI()
        self.instance = _ViewFPGATempLabel()

    def test_update(self):
        self.instance.update()

    def test_sensors_callback(self):
        data = {"temperature": 0}
        self.instance.sensors_callback(data)


class TestViewActionCalibrateADC(unittest.TestCase):

    def setUp(self):
        from view import _ViewActionCalibrateADC
        self.app = QApplication([])
        self.gui = GUI()

        class Dummy:

            def calibrated(self, bool):
                pass

        self.instance = _ViewActionCalibrateADC(self.gui.main_window.actionCalibrate_ADC, Dummy())

    def test_action_calibrate(self):
        self.instance._calibrate_adc()


class TestViewTab(unittest.TestCase):

    def setUp(self):
        from view import _ViewTab, _ViewInformationBottom
        self.app = QApplication([])
        self.gui = GUI()
        info = _ViewInformationBottom(self.gui.main_window.label_info)

        class Img:
            def add_cb(self, a):
                pass

        class Dummy:

            img_done = Img()

        self.instance = _ViewTab(info, Dummy())

    def test_show_info(self):
        from gfa import Test

        class Cfg:
            show_plot = False
            test = Test.NONE
            image_name = "A_1"
        c = Cfg()
        d = {"config": c}
        self.instance._show_info(d)

        c.test = Test.PSF
        d = {"config": c}
        self.instance._show_info(d)


class TestView(unittest.TestCase):

    def setUp(self):
        from view import View
        self.app = QApplication([])
        self.gui = GUI()

        class Img:
            def add_cb(self, a):
                pass

        class Dummy:
            img_done = Img()

        self.instance = View(self.gui.main_window, Dummy())

    def test_set_disabled(self):
        self.instance.setDisabled(False)


class TestBlockWidget(unittest.TestCase):

    def setUp(self):
        from view import View
        self.app = QApplication([])
        self.gui = GUI()

        class Img:
            def add_cb(self, a):
                pass

        class Dummy:
            img_done = Img()

        self.instance = View(self.gui.main_window, Dummy())

    def test_block(self):
        from view import BlockWidget
        with BlockWidget(self.instance, "Test"):
            pass


class ViewTestSuite(unittest.TestSuite):

    def __init__(self):
        super(ViewTestSuite, self).__init__()

        self.addTests(unittest.makeSuite(TestViewConfigurationConnection))
        self.addTests(unittest.makeSuite(TestViewConfigurationGeometry))
        self.addTests(unittest.makeSuite(TestViewConfigurationExpose))
        self.addTests(unittest.makeSuite(TestViewConfigurationPostExpose))
        self.addTests(unittest.makeSuite(TestViewConfiguration))
        self.addTests(unittest.makeSuite(TestViewStatusInfo))
        self.addTests(unittest.makeSuite(TestViewInformationBottom))
        self.addTests(unittest.makeSuite(TestViewCtrlButtons))
        self.addTests(unittest.makeSuite(TestViewToolsPanel))
        self.addTests(unittest.makeSuite(TestViewFPGATempLabel))
        self.addTests(unittest.makeSuite(TestViewActionCalibrateADC))
        self.addTest(unittest.makeSuite(TestViewTab))
        self.addTest(unittest.makeSuite(TestView))
        self.addTest(unittest.makeSuite(TestBlockWidget))


def run():
    test = unittest.main(__name__, failfast=True, exit=False, verbosity=3)
    return test
