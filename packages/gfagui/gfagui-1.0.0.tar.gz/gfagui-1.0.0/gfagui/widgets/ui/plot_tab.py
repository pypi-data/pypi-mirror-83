from PyQt5 import QtCore, QtWidgets

from guiqwt.curve import PlotItemList
from guiqwt.plot import CurveDialog
from guiqwt.histogram import ContrastAdjustment
from guiqwt.plot import ImageWidget, PlotManager, CurveWidget


class Ui_PlotTab(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_PlotTab, self).__init__()

        self.setObjectName("Tab")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

        QtCore.QMetaObject.connectSlotsByName(self)

    def setupToolBar(self):
        toolbar = QtWidgets.QToolBar(self)
        toolbar.setOrientation(QtCore.Qt.Vertical)
        return toolbar

    def setupTable(self, table_widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(table_widget.sizePolicy().hasHeightForWidth())
        table_widget.setSizePolicy(sizePolicy)
        table_widget.setRowCount(11)
        table_widget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags)
        table_widget.setHorizontalHeaderItem(1, item)
        table_widget.horizontalHeader().setSectionResizeMode(1)
        table_widget.verticalHeader().setSectionResizeMode(1)

        self.setWindowTitle("Form")
        item = table_widget.horizontalHeaderItem(0)
        item.setText("NAME")
        item = table_widget.horizontalHeaderItem(1)
        item.setText("VALUE")

    def setupConfigTable(self):
        config_table = QtWidgets.QTableWidget(self)
        self.setupTable(config_table)
        return config_table

    def setupItemList(self):
        itemlist = PlotItemList(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        itemlist.setSizePolicy(sizePolicy)
        return itemlist

    def setupContrastWdiget(self):
        contrast = ContrastAdjustment(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        contrast.setSizePolicy(sizePolicy)
        return contrast

    def setupPlotManager(self, toolbar, contrast, plot, itemlist):
        manager = PlotManager(self)
        manager.add_plot(plot.get_plot())
        for panel in (itemlist, contrast):
            manager.add_panel(panel)

        manager.add_toolbar(toolbar, id(toolbar))
        manager.set_default_toolbar(toolbar)
        manager.add_toolbar(contrast.toolbar, id(contrast.toolbar))
        manager.add_separator_tool()
        manager.register_all_image_tools()
        return manager

    def setupLayouts(self, toolbar=None, plot=None, config_table=None, contrast=None):
        self.horizontal_widget_layout = QtWidgets.QHBoxLayout(self)
        vertical_image_layout = QtWidgets.QVBoxLayout()

        self.horizontal_widget_layout.addWidget(config_table)

        if toolbar:
            horizontal_image_layout = QtWidgets.QHBoxLayout()
            horizontal_image_layout.addWidget(plot)
            horizontal_image_layout.addWidget(toolbar)
            vertical_image_layout.addLayout(horizontal_image_layout)
        else:
            vertical_image_layout.addWidget(plot)

        vertical_image_layout.addWidget(contrast)

        self.horizontal_widget_layout.addLayout(vertical_image_layout)

class Ui_PlotImageWidget(Ui_PlotTab):
    def __init__(self):
        super(Ui_PlotImageWidget, self).__init__()

        toolbar = self.setupToolBar()
        itemlist = self.setupItemList()
        contrast = self.setupContrastWdiget()
        self.config_table = self.setupConfigTable()
        self.plot = self.setupPlotWidget()

        self.setupPlotManager(toolbar, contrast, self.plot, itemlist)
        self.setupLayouts(toolbar, self.plot, self.config_table, contrast)

    def setupPlotWidget(self):
        plot = ImageWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        plot.setSizePolicy(sizePolicy)
        return plot

class Ui_PlotCurveWidget(Ui_PlotTab):
    def __init__(self):
        super(Ui_PlotCurveWidget, self).__init__()

        self.plot = self.setupPlotWidget()

        # CurveWidget have their own toolbar
        #self.setupToolBar()

        self.config_table = self.setupConfigTable()
        self.itemlist = self.setupItemList()

        # CurveWidget have their own toolbar
        #self.setupPlotManager()

        self.setupLayouts(plot=self.plot, config_table=self.config_table)

    def setupPlotWidget(self):
        plot = CurveDialog(edit=False, toolbar=True, wintitle="Waveform",
                          options=dict(title="GFA Waveform output", ylabel="ADUs"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        plot.setSizePolicy(sizePolicy)
        plot.get_itemlist_panel().show()
        return plot


class Ui_DualPlotImageWidget(Ui_PlotTab):
    def __init__(self):
        super(Ui_DualPlotImageWidget, self).__init__()

        self.plots = None
        self.contrasts = None

        self.toolbars = (self.setupToolBar(), self.setupToolBar())

        self.itemlists = (self.setupItemList(), self.setupItemList())

        self.config_table = self.setupConfigTable()

        self.setupPlotWidget()
        self.setupContrastWdiget()

        self.managers = (self.setupPlotManager(self.toolbars[0], self.contrasts[0], self.plots[0], self.itemlists[0]),
                        self.setupPlotManager(self.toolbars[1], self.contrasts[1], self.plots[1], self.itemlists[1]))

        self.setupLayouts(config_table=self.config_table, plot=self.plot_widget, contrast=self.contrast_widget)

    def setupPlotWidget(self):
        self.plot_widget = QtWidgets.QWidget(self)
        self.plot_layout= QtWidgets.QHBoxLayout(self.plot_widget)
        self.plots = (ImageWidget(), ImageWidget())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.plots[0].setSizePolicy(sizePolicy)
        self.plots[1].setSizePolicy(sizePolicy)
        self.plot_layout.addWidget(self.plots[0])
        self.plot_layout.addWidget(self.toolbars[0])
        self.plot_layout.addWidget(self.plots[1])
        self.plot_layout.addWidget(self.toolbars[1])

    def setupContrastWdiget(self):
        parent = super(Ui_DualPlotImageWidget, self)

        self.contrast_widget = QtWidgets.QWidget(self)
        self.contrast_layout = QtWidgets.QHBoxLayout(self.contrast_widget)
        self.contrasts = (parent.setupContrastWdiget(), parent.setupContrastWdiget())
        self.contrast_layout.addWidget(self.contrasts[0])
        self.contrast_layout.addWidget(self.contrasts[1])


class Ui_TriplePlotImageWidget(Ui_PlotTab):
    def __init__(self):
        super(Ui_TriplePlotImageWidget, self).__init__()

        self.plots = None
        self.contrasts = None

        self.toolbars = (self.setupToolBar(), self.setupToolBar(), self.setupToolBar())

        self.itemlists = (self.setupItemList(), self.setupItemList(), self.setupItemList())

        self.config_table = self.setupConfigTable()

        self.setupPlotWidget()
        self.setupContrastWdiget()

        self.managers = (self.setupPlotManager(self.toolbars[0], self.contrasts[0], self.plots[0], self.itemlists[0]),
                        self.setupPlotManager(self.toolbars[1], self.contrasts[1], self.plots[1], self.itemlists[1]),
                        self.setupPlotManager(self.toolbars[2], self.contrasts[2], self.plots[2], self.itemlists[2]))

        self.setupLayouts(config_table=self.config_table, plot=self.plot_widget, contrast=self.contrast_widget)

    def setupPlotWidget(self):
        self.plot_widget = QtWidgets.QWidget(self)
        self.plot_layout= QtWidgets.QHBoxLayout(self.plot_widget)
        self.plots = (ImageWidget(), ImageWidget(), ImageWidget())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.plots[0].setSizePolicy(sizePolicy)
        self.plots[1].setSizePolicy(sizePolicy)
        self.plots[2].setSizePolicy(sizePolicy)
        self.plot_layout.addWidget(self.plots[0])
        self.plot_layout.addWidget(self.toolbars[0])
        self.plot_layout.addWidget(self.plots[1])
        self.plot_layout.addWidget(self.toolbars[1])
        self.plot_layout.addWidget(self.plots[2])
        self.plot_layout.addWidget(self.toolbars[2])

    def setupContrastWdiget(self):
        parent = super(Ui_TriplePlotImageWidget, self)

        self.contrast_widget = QtWidgets.QWidget(self)
        self.contrast_layout = QtWidgets.QHBoxLayout(self.contrast_widget)
        self.contrasts = (parent.setupContrastWdiget(), parent.setupContrastWdiget(), parent.setupContrastWdiget())
        self.contrast_layout.addWidget(self.contrasts[0])
        self.contrast_layout.addWidget(self.contrasts[1])
        self.contrast_layout.addWidget(self.contrasts[2])