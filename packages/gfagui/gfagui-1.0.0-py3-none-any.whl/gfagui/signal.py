from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class _ManageImgStart(QObject):
    img_start = pyqtSignal(dict)

    def __init__(self):
        super(_ManageImgStart, self).__init__()

        self._cbs = []

        self.img_start.connect(self._dispatch_img_start)

    @pyqtSlot(dict)
    def _dispatch_img_start(self, d):
        for func in self._cbs:
            func(d)

    def emit(self, header, data):
        self.img_start.emit(data)

    def add_cb(self, cb):
        self._cbs.append(cb)


class _ManageImgDone(QObject):
    img_done = pyqtSignal(dict)

    def __init__(self):
        super(_ManageImgDone, self).__init__()

        self._cbs = []

        self.img_done.connect(self._dispatch_img_done)

    @pyqtSlot(dict)
    def _dispatch_img_done(self, d):
        for func in self._cbs:
            func(d)

    def emit(self, im, cfg, elapsed_time):
        d = {"image": im, "config": cfg, "elapsed_time": elapsed_time}

        self.img_done.emit(d)

    def add_cb(self, cb):
        self._cbs.append(cb)


class _ManageSensors(QObject):
    sensors = pyqtSignal(dict)

    def __init__(self):
        super(_ManageSensors, self).__init__()

        self._cbs = []

        self.sensors.connect(self._dispatch)

    @pyqtSlot(dict)
    def _dispatch(self, d):
        for func in self._cbs:
            func(d)

    def emit(self, d):
        self.sensors.emit(d)

    def add_cb(self, cb):
        self._cbs.append(cb)


class _ManageError(QObject):
    error = pyqtSignal(str)

    def __init__(self):
        super(_ManageError, self).__init__()

        self._cbs = []

        self.error.connect(self._dispatch)

    @pyqtSlot(str)
    def _dispatch(self, d):
        for func in self._cbs:
            func(d)

    def emit(self, d):
        self.error.emit(d)

    def add_cb(self, cb):
        self._cbs.append(cb)


class _ManagePID(QObject):
    pid = pyqtSignal(dict)

    def __init__(self):
        super(_ManagePID, self).__init__()

        self._cbs = []

        self.pid.connect(self._dispatch)

    @pyqtSlot(dict)
    def _dispatch(self, d):
        for func in self._cbs:
            func(d)

    def emit(self, d):
        self.pid.emit(d)

    def add_cb(self, cb):
        self._cbs.append(cb)


class Manager(QObject):

    def __init__(self):
        super(Manager, self).__init__()

        self.img_start = _ManageImgStart()
        self.img_done = _ManageImgDone()
        self.sensors = _ManageSensors()
        self.error = _ManageError()
        self.pid = _ManagePID()

    def configure_gfa_callbacks(self, gfa):
        gfa.configure_callbacks(self.img_start.emit, self.img_done.emit, self.sensors.emit, self.error.emit, self.pid.emit)
