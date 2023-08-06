from PyQt5.QtWidgets import QFrame

from gfaaccesslib.gfa import API_VERSION

from .base import Widget
from .ui import versions_ui


class Versions(Widget):

    def __init__(self, gfa):
        super(Versions, self).__init__()
        self._gfa = gfa

        self._versions_frame = QFrame()
        self._versions = versions_ui.Ui_Frame()
        self._versions.setupUi(self._versions_frame)

    def _reload(self):
        self._versions.api_version.setText(str(API_VERSION))

        ver = self._gfa._gfa.sys.remote_version().answer
        self._versions.firmware_version.setText(str(ver["firmware"]))
        self._versions.module_version.setText(str(ver["module"]))
        self._versions.modulelib_version.setText(str(ver["lib"]))
        self._versions.server_version.setText(str(ver["server"]))

    def show(self):
        self._reload()
        self._versions_frame.show()
